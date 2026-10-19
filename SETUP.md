# Meshlink Setup Guide

This guide explains how to install and run Meshlink on Linux and Windows.

## Requirements

- Python 3.10 or newer
- Git
- Network connectivity between the two computers
- Firewall permission for TCP port `5000` on the host

## 1. Clone the Repository

```bash
git clone https://github.com/ganeshkarthik016/meshlink-v0.git
cd meshlink-v0
```

## 2. Linux Setup

Create a virtual environment:

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

Install Meshlink:

```bash
python -m pip install -e .
```

Verify the installation:

```bash
meshlink --version
```

## 3. Windows Setup

Open PowerShell or Command Prompt in the cloned project directory.

### Create a virtual environment

```powershell
py -m venv .venv
```

### Activate in PowerShell

```powershell
.venv\Scripts\Activate.ps1
```

### Activate in Command Prompt

```bat
.venv\Scripts\activate.bat
```

### Install Meshlink

With the virtual environment activated, run:

```powershell
python -m pip install -e .
```

Verify the installation:

```powershell
meshlink --version
```

If PowerShell blocks the activation script, use Command Prompt or run the environment's Python executable directly:

```powershell
.venv\Scripts\python.exe -m pip install -e .
```

## 4. Start the Host

On the computer accepting the connection, activate its virtual environment and run:

```bash
meshlink host
```

The host listens on TCP port `5000`.

Keep the application running while the other peer connects.

## 5. Connect From Another Computer

Install Meshlink on the second computer using the same instructions.

Run:

```bash
meshlink connect HOST_IP
```

Replace `HOST_IP` with the host computer's reachable IP address.

### Finding the host IP

On Linux:

```bash
hostname -I
```

On Windows:

```powershell
ipconfig
```

Choose the IP address belonging to the network through which the other computer can reach the host.

## 6. Chat and File Transfer

Type a message and press Enter to send it.

To send a file:

```text
/send /path/to/file.txt
```

Use a valid file path on the sending computer. On Windows, an example path is:

```text
/send C:\Users\YourName\Documents\example.txt
```

The receiving peer saves the file in a `downloads` directory relative to the application's current working directory.

To close the chat:

```text
/quit
```

## Networking and Troubleshooting

### Connection refused

- Check that the host is running.
- Verify the host IP address.
- Ensure TCP port `5000` is available and the host is listening.

### Connection timeout

- Check whether a firewall blocks incoming connections.
- Confirm that the client can reach the host.
- Check whether the Wi-Fi network isolates connected devices.

### Firewall configuration

The host must permit inbound TCP connections on port `5000`.

On Ubuntu with UFW, an administrator can allow the port:

```bash
sudo ufw allow 5000/tcp
```

Only allow the connection on networks where you trust the other devices. Remove the rule when it is no longer required.

### Different networks

Meshlink currently has no built-in NAT traversal or relay server. Connections across different networks may require a suitable VPN or additional network configuration.

Do not expose this prototype directly to the public internet without appropriate security protections.

### Command not found

Ensure the virtual environment is activated and Meshlink is installed from the repository root:

```bash
python -m pip install -e .
```

## Security Notes

- Connect only to peers you trust.
- File integrity verification does not authenticate the sender.
- The current version does not provide end-to-end encryption.
- Avoid transferring sensitive files over untrusted networks.

## Current Scope

This guide covers the current one-to-one prototype. Multi-peer rooms, peer discovery, multi-hop forwarding, and resumable downloads are not yet implemented.
