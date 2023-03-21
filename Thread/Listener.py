import threading
import socket
from Thread.ClientHandler import ClientHandler

class Listener(threading.Thread):
    def __init__(self):
        super().__init__()
        self.host = 'localhost'
        self.port = 1215

    def run(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self.host, self.port))

        server_socket.listen()
        print("Listen Start")

        # 접속대기 반복
        while True:
            # 접속 대기
            client_soc, addr = server_socket.accept()
            print("Connected Client")
            client = ClientHandler(client_soc)
            client.daemon = True
            client.start()

        server_socket.close()
