"""
Utility for generating RSA SSH key pairs and persisting them to disk.
"""
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

# RSA key generation parameters
_PUBLIC_EXPONENT = 65537  # universally recommended; only 3 and 65537 are safe choices
_KEY_SIZE = 2048           # minimum recommended; use 4096 for higher-security environments


class KeyGenerator:
    @staticmethod
    def generate_ssh_keypair(private_key_path: str = "id_rsa", public_key_path: str = "id_rsa.pub"):
        """
        Generate an RSA SSH key pair and write both keys to disk.

        The private key is written in OpenSSH PEM format (unencrypted).
        The public key is written in OpenSSH single-line format, compatible
        with authorized_keys and known_hosts files.

        Returns:
            (private_bytes, public_bytes) — raw bytes of each serialized key.
        """
        private_key = rsa.generate_private_key(
            public_exponent=_PUBLIC_EXPONENT,
            key_size=_KEY_SIZE,
        )

        private_bytes = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.OpenSSH,
            # NoEncryption means no passphrase; swap for BestAvailableEncryption(b"pass") if needed
            encryption_algorithm=serialization.NoEncryption(),
        )

        # The public key is derived from the private key — no separate generation needed
        public_bytes = private_key.public_key().public_bytes(
            encoding=serialization.Encoding.OpenSSH,
            format=serialization.PublicFormat.OpenSSH,
        )

        with open(private_key_path, "wb") as f:
            f.write(private_bytes)

        with open(public_key_path, "wb") as f:
            f.write(public_bytes)

        print(f"Success! Keys saved to {private_key_path} and {public_key_path}")
        return private_bytes, public_bytes