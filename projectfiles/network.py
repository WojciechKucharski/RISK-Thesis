import socket
import pickle

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "25.95.17.180"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.debug = True
        self.p = self.connect()

    def connect(self):
        try:
            if self.debug:
                print(self.addr)
                self.client.connect(self.addr)
                r = pickle.loads(self.client.recv(2048))
                print("Recived:")
                print(len(pickle.dumps(r)), 'bytes')
                return r
            else:
                self.client.connect(self.addr)
                return pickle.loads(self.client.recv(2048))
        except socket.error as e:
            print(e)

    def send(self, data):
        try:
            if self.debug:
                print("Sent:")
                print(len(pickle.dumps(data)), 'bytes')
                self.client.send(pickle.dumps(data))
                r = pickle.loads(self.client.recv(2048))
                print("Recived:")
                print(len(pickle.dumps(r)), 'bytes')
                return r
            else:
                self.client.send(pickle.dumps(data))
                return pickle.loads(self.client.recv(2048))
        except socket.error as e:
            print(e)
