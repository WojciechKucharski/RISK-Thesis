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
            if net.connected:  # try to connect
                print("Connected to: ", x)
                return net  # if connected, return Network object
            else:
                print("Failed to connect")

    def test(self):
        self.net.send([self.nick, "room", "roomlist"])


def createTester(freq = 100):
    print("created tester")
    x = tester()
    t1 = time.time()
    while True:
        t2 = time.time()
        if t2 - t1 > 1/freq:
            t1 = t2
            x.test()

def testServer(N = 5, freq = 10):
    for _ in range(N):
        start_new_thread(createTester (freq, ))

testServer(2, 10)

while True:
    pass