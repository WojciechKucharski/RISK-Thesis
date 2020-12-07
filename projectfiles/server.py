import socket
from _thread import *
import pickle
from game import *
from users import *

maxUsers = 100
server = "" #read ip from sys
port = 5555
G = lobby() #create lobby
U = Users(maxUsers)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port)) #creating socket
except socket.error as e:
    print(str(e))

s.listen(maxUsers) #connections
print("Waiting for connection, Server Started")

def threaded_client(conn, addr): #connection thread
    conn.send(pickle.dumps(True)) #respond when first connected
    id = U.join(addr[0])
    while True:
        try:
            data = pickle.loads(conn.recv(2048)) #recive command from client
            if not data: #if something is wrong with data, break loop
                break
            else:
                pass
            conn.sendall(pickle.dumps(G.command(data))) #send respond to client
        except Exception as e: #if client disconnects, break loop
            print(e)
            break
    U.leave(addr[0])
    conn.close() #close connection

while True:
    conn, addr = s.accept()
    print("Connected to: ", addr)
    start_new_thread(threaded_client, (conn, addr))

