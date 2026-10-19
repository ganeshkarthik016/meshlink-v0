
import socket

from protocol import FILE_INFO, FILE_DATA, send_packet
from file_metadata import get_file_metadata, encode_metadata

CHUNK_SIZE = 4096
PORT = 5001

host_ip = input("Enter receiver's IP address: ")
file_path = input("Enter file path: ")

metadata = get_file_metadata(file_path)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
    client.connect((host_ip, PORT))
    print("Connected to receiver.")

    # Send metadata first.
    send_packet(client, FILE_INFO, encode_metadata(metadata))

    # Send the file in chunks.
    with open(file_path, "rb") as file:
        while True:
            chunk = file.read(CHUNK_SIZE)

            if not chunk:
                break

            send_packet(client, FILE_DATA, chunk)

print("File sent.")
