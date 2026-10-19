
import hashlib
import json
import os


def get_file_metadata(file_path):
    file_size = os.path.getsize(file_path)
    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:
        while True:
            chunk = file.read(4096)

            if not chunk:
                break

            sha256.update(chunk)

    return {
        "filename": os.path.basename(file_path),
        "size": file_size,
        "sha256": sha256.hexdigest(),
    }


def encode_metadata(metadata):
    return json.dumps(metadata).encode("utf-8")


def decode_metadata(payload):
    return json.loads(payload.decode("utf-8"))
