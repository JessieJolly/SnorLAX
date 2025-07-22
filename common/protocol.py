# This file contains code for describing the protocol to communicate with Server and Client
import json
import socket
import struct


class Protocol:
    """Simple Protocol for communication"""
    @staticmethod
    def send_message(sock: socket.socket, message_type, data):
        message = {
            'type':message_type,
            'data':data
        }
        encoded_json_data = json.dumps(message).encode('utf-8')
        sock.send(struct.pack('!I', len(encoded_json_data)))
        sock.send(encoded_json_data)

    @staticmethod
    def receive_message(sock: socket.socket):
        data_length = sock.recv(4)
        if not data_length:
            return None, None
        
        length = struct.unpack('!I', data_length)[0]

        json_data = b''
        while len(json_data) < length:
            chunk = sock.recv(length - len(json_data))
            if not chunk:
                return None, None
            json_data += chunk

        message = json.loads(json_data.decode('utf-8'))
        return message["type"], message["data"]
