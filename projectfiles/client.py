import pygame as pg
from pygame.locals import *
from network import Network
from Facade import *

class client:
    def __init__(self):
        self.pgInit() #init py game environment
        self.nick = self.getNick #get nick saved in file
        self.net = self.connect() #connect to server with socker
        self.screen = pg.display.set_mode((800, 450), pg.RESIZABLE) #create Window
        self.game = Facade(self.screen, self.net) #create Facade object

    @property
    def getNick(self): #getNick from file
        try:
            with open('Data\\nick.txt') as f: #open file
                nick = f.readline() #get nick
                f.close()
            return nick
        except Exception as e:
            return ">nick<" #if something gone wrong, return default nick

    def saveNick(self): #save nick to file
        with open('Data\\nick.txt', "w") as f:
            f.writelines(self.nick)
            f.close()

    @property
    def room_name(self): #get room name from server using method "command" from facade object
        name = self.game.command("whereIam") #send signal
        if name is False:
            return "lobby"
        else:
            return name

    def run(self):
        self.game.update(self.nick) #update objects and variables in Facade object
        self.game.show() #display all objects in game
        return self.eventHandler() #handle if event occurred

    def eventHandler(self):
        for event in pg.event.get(): #handle all events
            if event.type == pg.QUIT: #if [x] was clicked, break main loop and leave from room in server
                self.game.command("leave") #leave room
                return False #break loop

            elif event.type == pg.VIDEORESIZE: #handle resizing Window
                if event.w < 854:
                    event.w = 854
                if event.h < 480:
                    event.h = 480
                self.screen = pg.display.set_mode((event.w, event.h), pg.RESIZABLE)
                pg.display.update()

            if event.type == pg.MOUSEBUTTONDOWN: #handle mouse click
                if len(self.nick) > 0:
                    self.game.click()
                return True

            if self.room_name == "lobby": #if user in lobby
                if event.type == pg.KEYDOWN: #checking for keys pressed
                    if event.key == pg.K_BACKSPACE:
                        self.nick = self.nick[:-1] #updating user nickname
                    elif event.key == pg.K_RETURN or event.key == pg.K_ESCAPE:
                        pass
                    else:
                        if len(self.nick) <= 10:
                            self.nick += event.unicode
                    self.saveNick() #saving nickname
        return True

    def connect(self):
        while True: #try connect till success
            with open('Data\\ip.txt') as f: #read ip from file
                x = f.readline()
            net = Network(x, 5555)
            if net.connected: #try to connect
                print("Connected to: ", x)
                return net #if connected, return Network object
            else:
                print("Failed to connect")

    def pgInit(self):
        pg.init() #library
        pg.display.set_caption("The Game of RISK! - Client ")  #window name
        icon = pg.image.load('Data\\Icon\\logo.png')  #loading icon
        pg.display.set_icon(icon)  #setting icon
        pg.mixer.music.load("Data\\Sound\\bg.wav") #load music file
        pg.mixer.music.set_volume(0.01) #volume low
        pg.mixer.music.play(-1) #playing music in loop