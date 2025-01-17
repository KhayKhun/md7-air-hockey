import socket

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sever = ""
        self.port = 5555
        self.addr = (self.sever, self.port)
        self.connect()

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv
        except:
            pass