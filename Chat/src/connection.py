from socket import socket
from threading import Thread

def connect_to(info) -> socket:
    conn = socket()
    conn.connect(info)
    return conn

class RawConnection:
    def __init__(self, conn : socket, id = 'Guest') -> None:
        self.id = id
        self.socket = conn
        self.callback = lambda *args:None
        self.closed = False
        def __recv(_conn):
            try:
                read_bytes = bytes()
                end_len = -1
                while True:
                    s = _conn.socket.recv(1024)
                    for i in range(len(s)):
                        read_bytes = read_bytes + s[i].to_bytes(1, 'little')
                        if len(read_bytes) == 4:
                            end_len = int.from_bytes(read_bytes, 'little')
                        elif end_len != -1 and len(read_bytes) == end_len + 4:
                            try:
                                _conn.callback(_conn, read_bytes[4:])
                            except Exception as e:
                                print('Error in callback:', e)
                            read_bytes = bytes()
                            end_len = -1
            except Exception as e:
                print(e)
                self.socket.close()
                self.closed = True
        self.thread = Thread(target=__recv, args=(self,))
        self.thread.setDaemon(True)
        self.thread.start()
        
    def is_closed(self):
        return self.closed
    
    def send(self, msg : bytes):
        self.socket.sendall(len(msg).to_bytes(4, 'little'))
        self.socket.sendall(msg)

    def __call__(self, f):
        self.callback = f
        return f

