from network import *
from _thread import *
import time
import random

class tester:
    def __init__(self):
        self.net = self.connect()
        self.nick = str(random.randint(999, 999999999))

    def connect(self):
        while True:  # try connect till success
            with open('Data\\ip.txt') as f:  # read ip from file
                x = f.readline()
            net = Network(x, 5555)
            if net.connected:  # try to connect
                print("Connected to: ", x)
                return net  # if connected, return Network object
            else:
                print("Failed to connect")

    def command(self):
        self.net.send([self.nick, "room", "roomlist"])


def createTester(freq):
    print("created tester")
    x = tester()
    while True:
        x.command()

def testServer(N, freq):
    for _ in range(N):
        start_new_thread(createTester (freq, ))

testServer(95, 1)

while True:
    pass