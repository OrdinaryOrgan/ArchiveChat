from socket import socket
from connection import *
from threading import Thread

class RawServer:
    def __init__(self, info) -> None:
        self.socket = socket()
        self.socket.bind(info)
        self.socket.listen(4)
        self.connections = []
        def __serve():
            while True:
                conn, info = self.socket.accept()
                new_conn = RawConnection(conn)
                print("Connected with {}".format(info), new_conn)
                self.connections.append(new_conn)
                new_conn(self.callback)
        self.callback = lambda *args:None
        self.thread = Thread(target=__serve)
        self.thread.setDaemon(True)
        self.thread.start()

    def get_connections(self):
        return self.connections

    def __call__(self, f):
        self.callback = f