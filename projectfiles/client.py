import pygame as pg
from pygame.locals import *
from network import Network
from Facade import *

class client:
    def __init__(self):
        self.pgInit()
        self.nick = "Nick"
        self.net = self.connect()
        self.screen = pg.display.set_mode((800, 450), pg.RESIZABLE)
        self.game = Facade(self.screen, self.net)

    @property
    def room_name(self):
        name = self.command("whereIam")
        if name is False:
            return "lobby"
        else:
            return name

    @property
    def inLobby(self):
        if self.room_name == "lobby":
            return True
        else:
            return False

    def run(self):
        self.update()
        self.game.show()
        return self.event_Handler()

########################################################################################################################

    def update(self):
        self.game.update(self.nick, self.inLobby, self.room_name)

    def command(self, input):
        return self.game.command(input)

    def connect(self):
        while True:
            net = Network("25.95.17.180", 5555)
            if net.connected:
                return net
            else:
                print("Failed to connect")

    def event_Handler(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.command("leave")
                return False

            elif event.type == pg.VIDEORESIZE:
                if event.w < 854:
                    event.w = 854
                if event.h < 480:
                    event.h = 480
                self.screen = pg.display.set_mode((event.w, event.h), pg.RESIZABLE)
                pg.display.update()

            if event.type == pg.MOUSEBUTTONDOWN:
                self.game.click()

            if self.inLobby:
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_BACKSPACE:
                        self.nick = self.nick[:-1]
                    elif event.key == pg.K_RETURN or event.key == pg.K_ESCAPE:
                        pass
                    else:
                        if len(self.nick) <= 10:
                            self.nick += event.unicode
        return True

    def pgInit(self):
        pg.init()
        pg.display.set_caption("The Game of RISK! - Client ")  # window name
        icon = pg.image.load('Data\\Icon\\logo.png')  # loading icon
        pg.display.set_icon(icon)  # setting icon
        pg.mixer.music.load("Data\\Sound\\bg.wav")  # playing music in loop