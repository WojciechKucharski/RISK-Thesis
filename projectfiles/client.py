import pygame as pg
from pygame.locals import *
from network import Network
from Facade import *

class client:
    def __init__(self):
        pg.init()
        pg.display.set_caption("The Game of RISK! - Client ")  # window name
        icon = pg.image.load('Data\\Icon\\logo.png')  # loading icon
        pg.display.set_icon(icon)  # setting icon
        pg.mixer.music.load("Data\\Sound\\bg.wav")  # playing music in loop
        self.screen = pg.display.set_mode((800, 450), pg.RESIZABLE)
        self.net = Network()
        self.game = Facade(self.screen)
        self.game.loadmap("map")

    def run(self):
        print(self.net.send("Hello There!"))
        for event in pg.event.get():

            self.game.drag()

            if event.type == pg.QUIT:
                return False

            elif event.type == pg.VIDEORESIZE:
                if event.w < 854:
                    event.w = 854
                if event.h < 480:
                    event.h = 480
                self.screen = pg.display.set_mode((event.w, event.h), pg.RESIZABLE)
                pg.display.update()

            if event.type == pg.KEYDOWN:

                if event.key == pg.K_BACKSPACE:
                    print("BS")
                elif event.key == pg.K_RETURN:
                    print(self.game.provs[0].name)
                else:
                    print(event.unicode)

            if event.type == pg.MOUSEBUTTONDOWN:
                self.game.click()
            self.game.show()

        return True