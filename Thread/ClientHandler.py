import threading
import socket


class ClientHandler(threading.Thread):
    def __init__(self, client_socket: socket.socket):
        super().__init__()
        self.socket = client_socket

    def run(self):
        pass
