"""
Loads and manages the server's authorized public keys registry.
"""
from pathlib import Path

_DEFAULT_PATH = Path(__file__).resolve().parent.parent / "server" / "authorized_keys"


class AuthorizedKeys:
    def __init__(self, path: Path = _DEFAULT_PATH):
        self.path = path
        self._keys: list[bytes] = []
        self.load()

    def load(self):
        """Read authorized_keys from disk; each non-empty, non-comment line is one public key."""
        if not self.path.exists():
            self._keys = []
            return
        lines = self.path.read_text().splitlines()
        self._keys = [
            line.encode()
            for line in lines
            if line.strip() and not line.startswith("#")
        ]

    def is_authorized(self, public_key_bytes: bytes) -> bool:
        """Return True if the given OpenSSH public key bytes are in the registry."""
        candidate = public_key_bytes.strip()
        return candidate in [k.strip() for k in self._keys]

    def add_key(self, public_key_bytes: bytes):
        """Append a key to the registry file (enrollment helper)."""
        with open(self.path, "ab") as f:
            f.write(public_key_bytes.strip() + b"\n")
        self.load()
