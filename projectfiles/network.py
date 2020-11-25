import socket
import pickle

class Network:
    def __init__(self, ip, port = 5555): #try to create Network object using ip and port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = ip
        self.port = port
        self.addr = (self.server, self.port)
        self.connected = self.connect() #connect

    def connect(self):
        try:
            self.client.connect(self.addr) #send first command to server
            return pickle.loads(self.client.recv(2048)) #return first server respond
        except socket.error as e:
            return False #return False if connecting failed

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data)) #send command to server
            return pickle.loads(self.client.recv(2048)) #recive respond from server
        except socket.error as e:
            print(e)
