# This file contains code to run the [Client]
from re import match
import sys
import socket
from pathlib import Path
# Adding the parent directory to the path so the common package is found
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from common.protocol import Protocol, MSG_COMMAND, MSG_COMMAND_RESULT, MSG_ERROR


class SSHClient:
    def __init__(self, host='localhost', port=2222):
        self.host = host
        self.port = port

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
            print("Session error: {e}")
    
    
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