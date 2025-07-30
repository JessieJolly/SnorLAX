# This file contains code to run the [Server]
import socket
import sys
import threading


class SSHServer:
    def __init__(self, host='localhost', port=2222):
        self.host = host
        self.port = port

    def start(self):
        """Starting Server"""
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            server_socket.bind((self.host, self.port))
            server_socket.listen(5)
            server_socket.settimeout(1.0)
            print(f"Server listening on {self.host}:{self.port}")

            while True:
                try: 
                    client_socket, address = server_socket.accept()
                    client_thread = threading.Thread(
                        args=(client_socket, address)
                    )
                    client_thread.daemon = True
                    client_thread.start()
                except socket.timeout:
                    continue
        except KeyboardInterrupt:
            print("Server shutting down---")
        finally:
            server_socket.close()
    
def main():
    server = SSHServer()
    server.start()
    
if __name__ == "__main__":
    main()