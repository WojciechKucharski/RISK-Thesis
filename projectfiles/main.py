from client import *
from scratch import *
try:
    game = client() #try to create client object
except Exception as e:
    print(e)
    printError(e) #print error to file

running = True
while running:
    try:
        running = game.run() #run client object till it returns False, which means that user clicked [X]
    except Exception as e:
        game = client() #restart program if fatal error accurred
        print(e)
        printError(e) #print error to file



