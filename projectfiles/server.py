import socket
from _thread import *
import pickle
from game import *

server = "25.95.17.180"
port = 5555

G = lobby()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    print(str(e))

s.listen(10)
print("Waiting for connection, Server Started")

def threaded_client(conn):

    conn.send(pickle.dumps(True))

    while True:

        try:

            data = pickle.loads(conn.recv(2048))
            if not data:
                break
            else:
                pass
            conn.sendall(pickle.dumps(G.command(data)))

        except Exception as e:
            print(e)
            break

    print("Lost connection")
    conn.close()

while True:
    conn, addr = s.accept()
    print("Connected to: ", addr)
    start_new_thread(threaded_client, (conn,))

