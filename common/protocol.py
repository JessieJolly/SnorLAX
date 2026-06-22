"""
Wire protocol for SnorLAX client-server communication.

Framing: each message is prefixed with a 4-byte big-endian unsigned int
indicating the byte length of the JSON payload that follows.
"""
import json
import socket
import struct

# Message type identifiers shared between client and server
MSG_COMMAND = "COMMAND"
MSG_COMMAND_RESULT = "COMMAND_RESULT"
MSG_ERROR = "ERROR"
MSG_KEY_REGISTER = "KEY_REGISTER"
MSG_KEY_REGISTER_RESULT = "KEY_REGISTER_RESULT"

# Encoding used for all JSON payloads on the wire
ENCODING = "utf-8"

# struct format for the 4-byte big-endian length prefix
_LENGTH_PREFIX_FMT = "!I"
_LENGTH_PREFIX_SIZE = struct.calcsize(_LENGTH_PREFIX_FMT)  # always 4


class Protocol:
    """Framed JSON protocol: [4-byte length][JSON payload]"""

    @staticmethod
    def send_message(sock: socket.socket, message_type: str, data: dict):
        """Serialize and send a typed message over the socket."""
        message = {
            "type": message_type,
            "data": data,
        }
        payload = json.dumps(message).encode(ENCODING)
        # Send length prefix then payload as two separate writes to avoid
        # allocating a combined buffer for potentially large payloads.
        sock.send(struct.pack(_LENGTH_PREFIX_FMT, len(payload)))
        sock.send(payload)

    @staticmethod
    def receive_message(sock: socket.socket):
        """
        Block until a complete framed message is received.

        Returns (message_type, data), or (None, None) if the connection closed.
        Loops on recv to handle partial reads from the OS TCP buffer.
        """
        raw_length = sock.recv(_LENGTH_PREFIX_SIZE)
        if not raw_length:
            return None, None

        (length,) = struct.unpack(_LENGTH_PREFIX_FMT, raw_length)

        payload = b""
        while len(payload) < length:
            chunk = sock.recv(length - len(payload))
            if not chunk:
                return None, None
            payload += chunk

        message = json.loads(payload.decode(ENCODING))
        return message["type"], message["data"]
