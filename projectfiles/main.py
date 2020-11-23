from client import *
try:
    game = client()
except Exception as e:
    print(e)

while game.run():
    pass

