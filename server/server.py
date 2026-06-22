# This file contains code to run the [Server]
import socket
import sys
import threading
from pathlib import Path
# Adding the parent directory to the path so the common package is found
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from common.protocol import Protocol, MSG_COMMAND, MSG_COMMAND_RESULT, MSG_KEY_REGISTER, MSG_KEY_REGISTER_RESULT
from common.authorized_keys import AuthorizedKeys


class SSHServer:
    def __init__(self, host='localhost', port=2222):
        self.host = host
        self.port = port
        self.authorized_keys = AuthorizedKeys()
        print(f"Loaded {len(self.authorized_keys._keys)} authorized key(s)")

    def handle_session(self, client_socket):
        try:
            msg_type, data = Protocol.receive_message(client_socket)
            if msg_type == MSG_KEY_REGISTER:
                pub_key = data.get("public_key", "").encode()
                if pub_key:
                    self.authorized_keys.add_key(pub_key)
                    Protocol.send_message(client_socket, MSG_KEY_REGISTER_RESULT, {"success": True})
                    print(f"Registered new public key.")
                else:
                    Protocol.send_message(client_socket, MSG_KEY_REGISTER_RESULT, {"success": False})
                return

            while self.running:
                if not msg_type or msg_type != MSG_COMMAND:
                    break
                command = data['command'].strip()
                if not command:
                    msg_type, data = Protocol.receive_message(client_socket)
                    continue
                try:
                    if command == "hi":
                        output = "hi"
                    else:
                        output = "not hi"
                    Protocol.send_message(client_socket, MSG_COMMAND_RESULT, {"output": output})
                except Exception as e:
                    Protocol.send_message(client_socket, MSG_COMMAND_RESULT, {"output": f"Error: {str(e)}"})
                msg_type, data = Protocol.receive_message(client_socket)

        except Exception as e:
            print(f"System exception on receive: {str(e)}")

    def start(self):
        """Starting Server"""
        self.running = True
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            server_socket.bind((self.host, self.port))
            server_socket.listen(5)
            server_socket.settimeout(1.0)
            print(f"Server listening on {self.host}:{self.port}")

            while self.running:
                try: 
                    client_socket, address = server_socket.accept()
                    client_thread = threading.Thread(
                        target=self.handle_session,
                        args=(client_socket,)
                    )
                    client_thread.daemon = True
                    client_thread.start()
                except socket.timeout:
                    continue
        except KeyboardInterrupt:
            print("\nServer shutting down...")
            self.running = False
        finally:
            server_socket.close()
    
def main():
    server = SSHServer()
    server.start()
    
if __name__ == "__main__":
    main()