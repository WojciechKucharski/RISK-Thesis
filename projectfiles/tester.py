from network import *
from _thread import *
import time
import random

class tester:
    def __init__(self):
        self.net = self.connect()
        self.nick = str(random.randint(1, 9999999))

    def connect(self):
        while True:  # try connect till success
            with open('Data\\ip.txt') as f:  # read ip from file
                x = f.readline()
            net = Network(x, 5555)
            if net.connected:
                return net
            else:
                print("Failed to connect")

    def test(self):
        self.net.send([self.nick, "room", "test"])


def createTester():
    x = tester()
    while True:
        x.test()

def testServer(N):
    for _ in range(N):
        start_new_thread(createTester, ())

testServer(900)

while True:
    x = tester()
    t1 = time.time()
    x.test()
    t2 = time.time() - t1

    print(t2)