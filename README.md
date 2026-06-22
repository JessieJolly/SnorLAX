# SnorLAX

A lightweight Python client-server application that provides an SSH-like remote command session over TCP. The client connects to the server, sends commands interactively, and prints the server's responses. RSA SSH key pair generation is handled on the client side, with public key registration supported via the `sendkey` command.

## Project structure

```
SnorLAX/
├── client/
│   └── client.py           # Interactive client session with built-in key management
├── server/
│   ├── server.py           # Multi-threaded TCP server
│   └── authorized_keys     # Registry of trusted client public keys (not tracked by git)
├── common/
│   ├── protocol.py         # Shared message framing and serialization
│   ├── keygen.py           # RSA SSH key pair generation utility
│   └── authorized_keys.py  # Authorized keys loader and manager
└── requirements.txt
```

## Requirements

- Python 3.8+
- Dependencies listed in `requirements.txt`

## Setup

Create and activate a virtual environment (recommended):

```bash
python -m venv venv
source venv/bin/activate   # macOS/Linux
# venv\Scripts\activate    # Windows
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run commands from the project root so the `common` package resolves correctly.

## Usage

### Start the server

```bash
python server/server.py
```

The server listens on `localhost:2222` by default.

### Start the client

In a separate terminal:

```bash
python client/client.py
```

You will see a `$` prompt. Type commands and press Enter; the server's output is printed below.

### Client-side commands

| Command                   | Description                                                         |
|---------------------------|---------------------------------------------------------------------|
| `genkey` / `generate key` | Generate an RSA 2048-bit SSH key pair and save to disk              |
| `showkey` / `show key`    | Print the currently held private and public key to stdout           |
| `sendkey` / `send key`    | Send the current public key to the server for registration          |
| `exit`                    | End the session (Ctrl+C also works)                                 |

Generated keys are written to `id_rsa` (private) and `id_rsa.pub` (public) in the working directory. If a key pair already exists in memory, the client prompts for confirmation before regenerating.

### Key enrollment flow

To register a client with the server:

1. Run `genkey` to generate a key pair
2. Run `sendkey` to push the public key to the server
3. The server appends it to `server/authorized_keys` and confirms success
4. Reconnect — the key is now in the registry for future authentication

> Note: `sendkey` ends the current session. Reconnect after registering.

### Example session

```
---Starting session with server---
---Started session with Server---
---Type 'exit' to quit session---
$ hi
hi
$ genkey
Success! Keys saved to id_rsa and id_rsa.pub
$ showkey
Private key: -----BEGIN OPENSSH PRIVATE KEY-----
...
Public key: ssh-rsa AAAAB3NzaC1yc2E...
$ sendkey
Public key registered on server.
$ exit
```

## Protocol

Client and server communicate using length-prefixed JSON messages defined in `common/protocol.py`.

Each message is sent as:

1. A 4-byte big-endian unsigned integer (message length)
2. A UTF-8 JSON payload: `{"type": "<MESSAGE_TYPE>", "data": {...}}`

| Message type          | Direction        | Purpose                               |
|-----------------------|------------------|---------------------------------------|
| `COMMAND`             | Client -> Server | Carries a shell-style command         |
| `COMMAND_RESULT`      | Server -> Client | Carries command output                |
| `ERROR`               | Server -> Client | Carries an error description          |
| `KEY_REGISTER`        | Client -> Server | Sends a public key for registration   |
| `KEY_REGISTER_RESULT` | Server -> Client | Confirms or rejects key registration  |

## Configuration

Both client and server accept optional `host` and `port` arguments via their constructors (`SSHClient`, `SSHServer`). Defaults are `localhost` and `2222`.

## License

No license file is included yet. Add one if you plan to distribute this project.
