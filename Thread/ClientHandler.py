import threading
import socket
import struct
from Protocol import *

class ClientHandler(threading.Thread):
    def __init__(self, client_socket: socket.socket):
        super().__init__()
        self.socket = client_socket

    def run(self):
        while True:
            try:
                data: bytes = self.socket.recv(1024)
                if not data:
                    print("EOF")
                    break

                self.process(bytes)

            except ConnectionError as e:
                print("Connection Error")
                print(e)

    def process(self, data: bytes):
        protocol, body = struct.unpack('bs', data)
        print("Protocol: %d" % protocol)
        print("Body: %s" % repr(body))

        if protocol == EProtocol.INFO:
            print("INFO")
        elif protocol == EProtocol.URL:
            print("URL")
