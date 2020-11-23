from client import *
try:
    game = client()
except Exception as e:
    print(e)
    input()
x = True
while x:
    try:
        x = game.run()
    except Exception as e:
        print(e)
        input()
    pass
input()