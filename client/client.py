# This file contains code to run the [Client]
from re import match
import sys
import socket
from pathlib import Path
# Adding the parent directory to the path so the common package is found
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from common.protocol import Protocol, MSG_COMMAND, MSG_COMMAND_RESULT, MSG_ERROR, MSG_KEY_REGISTER, MSG_KEY_REGISTER_RESULT
from common.keygen import KeyGenerator


class SSHClient:
    def __init__(self, host='localhost', port=2222):
        self.host = host
        self.port = port
        self.private_key = None
        self.public_key = None

    def start_session(self, sock):
        print("---Started session with Server---")
        print("---Type 'exit' to quit session---")

        # while loop for session
        try:
            while True:
                command = input("$ ").strip()
                if command == "":
                    continue
                if command.lower() == "exit":
                    break
                if command.lower() == "generate key" or command.lower() == "genkey":
                    if not self.private_key and not self.public_key:
                        private_key, public_key = KeyGenerator.generate_ssh_keypair()
                        self.private_key = private_key
                        self.public_key = public_key
                        continue
                    else:
                        print("Key already generated, are you sure you want to generate a new one? (y/n)")
                        confirm = input()
                        if confirm.lower() == "y":
                            private_key, public_key = KeyGenerator.generate_ssh_keypair()
                            self.private_key = private_key
                            self.public_key = public_key
                            continue
                        else:
                            continue
                if command.lower() == "show key" or command.lower() == "showkey":
                    if self.private_key and self.public_key:
                        print(f"Private key: {self.private_key}")
                        print(f"Public key: {self.public_key}")
                        continue
                    else:
                        print("No key generated, please generate a key first")
                        continue
                if command.lower() in ("sendkey", "send key"):
                    if not self.public_key:
                        print("No key generated. Run 'genkey' first.")
                        continue
                    Protocol.send_message(sock, MSG_KEY_REGISTER, {"public_key": self.public_key.decode()})
                    msg_type, data = Protocol.receive_message(sock)
                    if msg_type == MSG_KEY_REGISTER_RESULT and data.get("success"):
                        print("Public key registered on server.")
                    else:
                        print("Failed to register key.")
                    continue
                Protocol.send_message(sock, MSG_COMMAND, {"command": command})
                message_type, data = Protocol.receive_message(sock)
                if message_type == MSG_COMMAND_RESULT:
                    print(data.get("output", ""))
                elif message_type == MSG_ERROR:
                    print(f"Error: {data.get('error', '')}")
                else:
                    break
        except KeyboardInterrupt:
            print("Session interrupted!")
        except Exception as e:
            print(f"Session error: {e}")
    
    
def main():
    client = SSHClient()
    print("---Starting session with server---")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((client.host, client.port))
    except Exception as e:
        print(f"Error connecting to server: {e}")
        return
    client.start_session(sock)
    
if __name__ == "__main__":
    main()