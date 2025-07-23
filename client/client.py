# This file contains code to run the [Client]
import sys

from common.protocol import Protocol


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
                if command.lower() == "exit":
                    break
                Protocol.send_message(sock, "COMMAND", {'command':command})
                message_type, data = Protocol.receive_message(sock)
                if message_type == "COMMAND_RESULT":
                    print(data.get('output', ''))
                elif message_type == "ERROR":
                    print(f"Error: {data.get('error', '')}")
                else:
                    break
        except KeyboardInterrupt:
            print("Session interrupted!")
        except Exception as e:
            print("Session error: {e}")
    
    
def main():
    if(len(sys.argv)) < 2:
        print("Usage: python <command> <username>")
        print("Commands:")
        print("1. keygen - generates new key pair for user")
        print("2. register - registers public key of user")
        print("3. connect - tries to connect to server using key")

    client = SSHClient()

    
if __name__ == "__main__":
    main()