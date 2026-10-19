
import socket
import hashlib
import os

from protocol import FILE_INFO, FILE_DATA, receive_packet
from file_metadata import decode_metadata

HOST = "0.0.0.0"
PORT = 5001
CHUNK_SIZE = 4096


def receive_file(conn):
    packet_type, payload = receive_packet(conn)

    if packet_type != FILE_INFO:
        raise ValueError("Expected FILE_INFO packet")

    metadata = decode_metadata(payload)

    filename = os.path.basename(metadata["filename"])
    expected_size = metadata["size"]
    expected_hash = metadata["sha256"]

    # Never allow the remote filename to choose an arbitrary path.
    destination = "received_" + filename

    print("Receiving:", filename)
    print("Expected size:", expected_size, "bytes")

    sha256 = hashlib.sha256()
    total_bytes = 0

    with open(destination, "wb") as file:
        while total_bytes < expected_size:
            packet_type, payload = receive_packet(conn)

            if packet_type != FILE_DATA:
                raise ValueError("Expected FILE_DATA packet")

            if not payload:
                raise ConnectionError("Transfer ended before all bytes arrived")

            if total_bytes + len(payload) > expected_size:
                raise ValueError("Received more data than expected")

            file.write(payload)
            sha256.update(payload)
            total_bytes += len(payload)

    if sha256.hexdigest() != expected_hash:
        raise ValueError("File integrity check failed")

    print("Received:", destination)
    print("Bytes:", total_bytes)
    print("SHA-256 verified successfully!")


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(1)

    print(f"Waiting for sender on port {PORT}...")

    conn, addr = server.accept()

    with conn:
        print("Connected to:", addr)
        receive_file(conn)
