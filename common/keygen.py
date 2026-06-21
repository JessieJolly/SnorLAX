from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import os

class KeyGenerator:
    @staticmethod
    def generate_ssh_keypair(private_key_path: str = "id_rsa", public_key_path: str = "id_rsa.pub"):
        """Generate an SSH keypair."""
        # 1. Generate the RSA Private Key
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048, # 2048 is standard, use 4096 for higher security
        )

        # 2. Serialize the Private Key into OpenSSH format
        private_bytes = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.OpenSSH,
            # In a real app, you might use BestAvailableEncryption(b"your_password")
            encryption_algorithm=serialization.NoEncryption() 
        )

        # 3. Extract the Public Key from the Private Key
        public_key = private_key.public_key()

        # 4. Serialize the Public Key into OpenSSH format
        public_bytes = public_key.public_bytes(
            encoding=serialization.Encoding.OpenSSH,
            format=serialization.PublicFormat.OpenSSH
        )

        # 5. Save the keys to files
        with open(private_key_path, 'wb') as f:
            f.write(private_bytes)
            
        with open(public_key_path, 'wb') as f:
            f.write(public_bytes)

        print(f"Success! Keys saved to {private_key_path} and {public_key_path}")
        return private_bytes, public_bytes