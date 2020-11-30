from client import *
from scratch import *
try:
    game = client() #try to create client object
except Exception as e:
    print(e)

running = True
while running:
    if True:
        running = game.run() #run client object till it returns False, which means that user clicked [X]
    else: #except Exception as e:
        game = client()
        print(e)
        printError(e)



