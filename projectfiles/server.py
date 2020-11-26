import socket
from _thread import *
import pickle
from game import *

server = "" #read ip from sys
port = 5555
G = lobby() #create lobby
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port)) #creating socket
except socket.error as e:
    print(str(e))

s.listen(10) #connections
print("Waiting for connection, Server Started")

def threaded_client(conn): #connection thread
    conn.send(pickle.dumps(True)) #respond when first connected
    while True:
        if True:
            data = pickle.loads(conn.recv(2048)) #recive command from client
            if not data:
                break
            else:
                pass
            conn.sendall(pickle.dumps(G.command(data))) #send respond to client
        else: #except Exception as e: #if client disconnects, break loop
            print(e)
            break
    print("Lost connection")
    conn.close() #close connection

while True:
    conn, addr = s.accept()
    print("Connected to: ", addr)
    start_new_thread(threaded_client, (conn,))

