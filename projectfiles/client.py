import pygame as pg
from pygame.locals import *
from network import Network
from Facade import *

class client:
    def __init__(self):
        self.pgInit()
        self.screen = pg.display.set_mode((800, 450), pg.RESIZABLE)
        self.net = Network()
        self.game = Facade(self.screen)
        self.room_name = "lobby"
        self.inLobby = True
        self.nick = "Nick"

        self.game.loadmap("map")

    def run(self):

        if self.inLobby:
            self.game.setlobby(self.nick)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                return False

            elif event.type == pg.VIDEORESIZE:
                if event.w < 854:
                    event.w = 854
                if event.h < 480:
                    event.h = 480
                self.screen = pg.display.set_mode((event.w, event.h), pg.RESIZABLE)
                pg.display.update()

            if self.inLobby:
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_BACKSPACE:
                        self.nick = self.nick[:-1]
                    elif event.key == pg.K_RETURN or event.key == pg.K_ESCAPE:
                        pass
                    else:
                        if len(self.nick) <= 10:
                            self.nick += event.unicode


            if event.type == pg.MOUSEBUTTONDOWN:
                self.game.click()

            self.game.show()

        return True

    def pgInit(self):
        pg.init()
        pg.display.set_caption("The Game of RISK! - Client ")  # window name
        icon = pg.image.load('Data\\Icon\\logo.png')  # loading icon
        pg.display.set_icon(icon)  # setting icon
        pg.mixer.music.load("Data\\Sound\\bg.wav")  # playing music in loop

