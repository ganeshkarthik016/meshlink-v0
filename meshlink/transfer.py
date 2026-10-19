
import hashlib
import os

from protocol import (
    FILE_INFO,
    FILE_DATA,
    send_packet,
    receive_packet,
)
from file_metadata import (
    get_file_metadata,
    encode_metadata,
    decode_metadata,
)

CHUNK_SIZE = 4096


def send_file(sock, file_path, send_lock=None):
    metadata = get_file_metadata(file_path)
    expected_size = metadata["size"]

    # Keep metadata and all file chunks together on the connection.
    if send_lock is not None:
        send_lock.acquire()

    try:
        send_packet(sock, FILE_INFO, encode_metadata(metadata))

        sent_bytes = 0

        with open(file_path, "rb") as file:
            while True:
                chunk = file.read(CHUNK_SIZE)

                if not chunk:
                    break

                send_packet(sock, FILE_DATA, chunk)
                sent_bytes += len(chunk)

        if sent_bytes != expected_size:
            raise RuntimeError("File changed while being sent")

    finally:
        if send_lock is not None:
            send_lock.release()

    print(f"Sent {sent_bytes} bytes from {file_path}")


def receive_file(sock, destination_dir=".", metadata=None):
    if metadata is None:
        packet_type, payload = receive_packet(sock)

        if packet_type != FILE_INFO:
            raise ValueError("Expected FILE_INFO packet")

        metadata = decode_metadata(payload)


    filename = metadata["filename"]
    expected_size = metadata["size"]
    expected_hash = metadata["sha256"]

    # Prevent the remote filename from choosing an arbitrary path.
    filename = os.path.basename(filename)

    if not filename:
        raise ValueError("Invalid filename")

    if not isinstance(expected_size, int) or expected_size < 0:
        raise ValueError("Invalid file size")

    if not isinstance(expected_hash, str) or len(expected_hash) != 64:
        raise ValueError("Invalid SHA-256 hash")

    os.makedirs(destination_dir, exist_ok=True)
    destination = os.path.join(destination_dir, "received_" + filename)

    sha256 = hashlib.sha256()
    received_bytes = 0

    with open(destination, "wb") as file:
        while received_bytes < expected_size:
            packet_type, payload = receive_packet(sock)

            if packet_type != FILE_DATA:
                raise ValueError("Expected FILE_DATA packet")

            if not payload:
                raise ConnectionError("File transfer ended early")

            if len(payload) > CHUNK_SIZE:
                raise ValueError("File chunk is too large")

            if received_bytes + len(payload) > expected_size:
                raise ValueError("Received more bytes than expected")

            file.write(payload)
            sha256.update(payload)
            received_bytes += len(payload)

    received_hash = sha256.hexdigest()

    if received_hash != expected_hash:
        os.remove(destination)
        raise ValueError("File integrity check failed")

    print(f"Received file: {destination}")
    print(f"Received bytes: {received_bytes}")
    print("SHA-256 verified successfully!")

    return destination
