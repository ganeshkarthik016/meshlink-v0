
import socket
import threading
import os

from protocol import CHAT, FILE_INFO, send_packet, receive_packet
from transfer import send_file, receive_file
from file_metadata import decode_metadata

PORT = 5000

send_lock = threading.Lock()
DOWNLOAD_DIR = "downloads"


def receive_messages(sock):
    try:
        while True:
            packet_type, payload = receive_packet(sock)

            if packet_type == CHAT:
                message = payload.decode("utf-8")
                print(f"\nFriend: {message}")

            elif packet_type == FILE_INFO:
                metadata = decode_metadata(payload)

                try:
                    path = receive_file(
                        sock, DOWNLOAD_DIR, metadata=metadata
                    )
                    print(f"\nFile received: {path}")
                except (OSError, ConnectionError, ValueError) as exc:
                    print(f"\nFile receive failed: {exc}")

            else:
                print(f"\nUnknown packet type: {packet_type}")

    except (ConnectionError, OSError) as exc:
        print(f"\nHost disconnected: {exc}")
    except Exception as exc:
        print(f"\nReceive error: {exc}")


HOST = input("Enter host IP (127.0.0.1 for same computer): ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

print("Connected! Type a message, /send <file_path>, or /quit.")

thread = threading.Thread(
    target=receive_messages,
    args=(client,),
    daemon=True,
)
thread.start()

try:
    while True:
        command = input("You: ").strip()

        if command == "/quit":
            break

        if command.startswith("/send "):
            file_path = command[len("/send "):].strip()

            if not os.path.isfile(file_path):
                print("File not found:", file_path)
                continue

            try:
                send_file(client, file_path, send_lock)
            except (OSError, ConnectionError, ValueError) as exc:
                print("File send failed:", exc)

            continue

        if command:
            with send_lock:
                send_packet(
                    client,
                    CHAT,
                    command.encode("utf-8"),
                )

finally:
    client.close()
    print("Chat closed.")
