
import socket
import threading

from transfer import send_file, receive_file

left, right = socket.socketpair()


def sender():
    try:
        send_file(left, "sample.txt")
    finally:
        left.close()


thread = threading.Thread(target=sender)
thread.start()

try:
    receive_file(right, destination_dir="downloads")
finally:
    right.close()
    thread.join()

print("Transfer test complete.")
