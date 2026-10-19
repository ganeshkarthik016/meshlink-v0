
import os
import socket
import tempfile
import threading
import unittest

from transfer import send_file, receive_file


class TestFileTransfer(unittest.TestCase):
    def test_file_transfer(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            source_path = os.path.join(temp_dir, "sample.txt")
            download_dir = os.path.join(temp_dir, "downloads")

            content = b"Hello from Meshlink!\nTesting file transfer.\n"

            with open(source_path, "wb") as file:
                file.write(content)

            left, right = socket.socketpair()
            errors = []

            def sender():
                try:
                    send_file(left, source_path)
                except Exception as exc:
                    errors.append(exc)
                finally:
                    left.close()

            thread = threading.Thread(target=sender)
            thread.start()

            try:
                received_path = receive_file(
                    right,
                    destination_dir=download_dir,
                )
            finally:
                right.close()
                thread.join(timeout=5)

            self.assertFalse(thread.is_alive())
            self.assertEqual(errors, [])

            with open(received_path, "rb") as file:
                received_content = file.read()

            self.assertEqual(received_content, content)


if __name__ == "__main__":
    unittest.main()
