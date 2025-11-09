# This file contains code to run the [Server]
import socket
import sys
import threading

from common.protocol import Protocol


class SSHServer:
    def __init__(self, host='localhost', port=2222):
        self.host = host
        self.port = port

    def handle_session(self, client_socket):
        try:
            while self.running:
                msg_type, data = Protocol.receive_message(client_socket)
                if not msg_type or msg_type!="COMMAND":
                    break
                command = data['command'].strip()
                if not command:
                    continue
                try:
                    if command == "hi":
                        output = "hi"
                    else:
                        output = "not hi"
                    Protocol.send_message(client_socket, "COMMAND_RESULT", {'output': output})
                except Exception as e:
                    Protocol.send_message(client_socket, "COMMAND_RESULT", {'output': f"Error: {str(e)}"})

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