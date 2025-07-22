# This file contains code to run the [Client]
import sys


class SSHClient:
     def __init__(self):
          pass
    
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