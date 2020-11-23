from client import *

game = client()
x = True
while x:
    try:
        x = game.run()
    except Exception as e:
        print(e)
        input()
    pass
input()