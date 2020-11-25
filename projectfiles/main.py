from client import *
try:
    game = client()
except Exception as e:
    print(e)

running = True
while running:
    try:
        running = game.run()
    except Exception as e:
        print(e)



