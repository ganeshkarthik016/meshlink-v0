# Meshlink

**Meshlink** is a command-line peer-to-peer chat and file-sharing application built with Python and TCP sockets. It allows two computers to communicate directly over a network, exchange messages, and transfer files without relying on a central messaging server.

---

## Features

- **One-to-one, bidirectional chat**
- **Direct TCP socket communication**
- **File transfer using chunked data transmission**
- **SHA-256 file integrity verification**
- **Command-line interface** for hosting and connecting
- **Automated test** for file transfer

---

## Tech Stack

- **Language:** Python
- **Networking:** TCP sockets
- **Concurrency:** Python threading
- **Protocol:** Custom packet-based communication
- **Integrity Verification:** SHA-256
- **Packaging:** Python `pyproject.toml`

---

## How It Works

1. One peer starts Meshlink in host mode.
2. Another peer connects using the host's reachable IP address.
3. Both peers can exchange messages.
4. Either peer can send a file directly to the other.
5. The receiver verifies the transferred file using its SHA-256 hash.

---

## Quick Start

Install Python 3.10 or newer, then follow the platform-specific instructions in `SETUP.md`.

### 1. Start the Host

```bash
meshlink host
```
