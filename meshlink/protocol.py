
import struct

HEADER_FORMAT = "!BI"
HEADER_SIZE = struct.calcsize(HEADER_FORMAT)

CHAT = 1
FILE_INFO = 2
FILE_DATA = 3


def send_packet(sock, packet_type, payload):
    header = struct.pack(HEADER_FORMAT, packet_type, len(payload))
    sock.sendall(header + payload)


def receive_exact(sock, size):
    data = bytearray()

    while len(data) < size:
        chunk = sock.recv(size - len(data))

        if not chunk:
            raise ConnectionError("Connection closed unexpectedly")

        data.extend(chunk)

    return bytes(data)


def receive_packet(sock):
    header = receive_exact(sock, HEADER_SIZE)
    packet_type, payload_size = struct.unpack(HEADER_FORMAT, header)

    payload = receive_exact(sock, payload_size)

    return packet_type, payload
