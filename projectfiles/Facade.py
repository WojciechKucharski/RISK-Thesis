import pygame as pg
from scratch import *
import math


class Facade:
    screen  = None
    nres    = []
    players = []
    provs   = []
    butts   = []
    images  = []
    net = []

    nick = []
    inLobby = []
    room_name = []

    def __init__(self, screen, net):
        Facade.nres = (1280-160, 720-90)
        Facade.screen = screen
        Facade.net = net

    def update_provs(self):
        for x in Facade.provs:
            response = self.command(x.comm)
            x.owner = response[0]
            x.units = response[1]

    def update(self, nick, inLobby, room_name):
        Facade.nick = nick
        Facade.inLobby = inLobby
        Facade.room_name = room_name

    def command(self, input):
        comm = [Facade.nick, Facade.room_name]
        if type(input) is list:
            for x in input:
                comm.append(x)
        else:
            comm.append(input)

        return Facade.net.send(comm)

    def loadmap(self):
        self.reset()
        self.mapname = self.command("mapname")
        Facade.images.append(image('Data\\Maps\\' + self.mapname + '\\' + self.mapname + '.jpg'))
        self.mapsize = list(self.images[0].img.get_size())
        for x in connect_csv('Data\\Maps\\' + self.mapname + '\\' + self.mapname + '.csv'):
            Facade.provs.append(province(x))
        Facade.butts.append(button(self.mapsize[0]+25, 25, 75, 25, "Button", color["green"]))


    def setlobby(self, nick):
        self.reset()
        self.backscreen = color["gray"]
        Facade.butts.append(button(100, 100, 800, 75, nick, color["white"], False, False, 5))
        Facade.butts.append(button(100, 200, 800, 75, "Create Room", color["purple"], True, False, 4, "create"))
        rooms = self.command("roomlist")

        i = 0
        if rooms is not False:
            for x in rooms:
                self.butts.append(button(100, 300 + 75 * i, 800, 50, x, color["green"], True, False, 3, x))
                i+=1


    def reset(self):
        self.backscreen = color["beige"]
        Facade.players = []
        Facade.provs = []
        Facade.butts = []
        Facade.images = []

    def drag(self):
        pass

    def click(self):
        for x in Facade.provs + Facade.butts:
            if x.isOver:
                if x.comm is not None:
                    return x.comm

        return None

    @property
    def scale(self):
        w, h = pg.display.get_surface().get_size()
        if w/h >= 16.0/9.0:
            return h/Facade.nres[1]
        else:
            return w/Facade.nres[0]
    @property
    def obj(self):
        return Facade.images + Facade.players + Facade.provs + Facade.butts

    def show(self):
        self.update_provs()
        self.screen.fill(self.backscreen)
        for x in self.obj:
            x.show()
        pg.display.update()

    def drawtext(self, screen, X, Y, text, fontsize, color=(0, 0, 0)):
        font = pg.font.Font("Data\\Font\\arial.ttf", math.floor(fontsize * 1))
        TextSurf = font.render(text, True, color)
        TextRect = TextSurf.get_rect()
        TextRect.center = (X, Y)
        screen.blit(TextSurf, TextRect)

########################################################################################################################

class image(Facade):
    def __init__(self, path):
        self.img = pg.image.load(path)
        self.size = list(self.img.get_size())

    def show(self):
        temp_img = self.img.copy()
        temp_img = pg.transform.scale(temp_img, (int(self.scale * self.size[0]), int(self.scale * self.size[1])))
        Facade.screen.blit(temp_img, (0, 0))

    @property
    def isOver(self):
        pos = pg.mouse.get_pos()
        return False

########################################################################################################################

class button(Facade):
    def __init__(self, X, Y, dx, dy, text, color = (128, 128, 128), clickable = True, textonly = False, font_amp = 1, comm = None): #button object init, if no color given, GRAY
        self.X = X #left corner X
        self.Y = Y #left corner Y
        self.dx = dx #width
        self.dy = dy #height
        self.text = text
        self.color = color
        self.clickable = clickable
        self.textonly = textonly
        self.font_amp = font_amp
        self.comm = comm


    @property
    def isOver(self): #function that tells if mouse is over this object
        if self.clickable is False:
            return False
        pos = pg.mouse.get_pos()
        if pos[0] <=(self.X*self.scale + self.dx*self.scale) and pos[0] >= (self.X*self.scale):
            if pos[1] <= (self.Y*self.scale + self.dy*self.scale) and pos[1] >= (self.Y*self.scale):
                return True
        return False

    def show(self): #drawing button
        if self.isOver:
            border = color["white"]
        else:
            border = color["black"]
        if self.textonly:
            pass
        else:
            pg.draw.rect(Facade.screen, self.color, (self.X*self.scale, self.Y*self.scale, self.dx*self.scale, self.dy*self.scale), 0) #background rectangle
            pg.draw.rect(Facade.screen, border, (self.X*self.scale, self.Y*self.scale, self.dx*self.scale, self.dy*self.scale), 3) #border
        self.drawtext(Facade.screen, self.X*self.scale + self.dx*self.scale/2, self.Y*self.scale + self.dy*self.scale/2, str(self.text), int(self.font_amp*12*self.scale), (0, 0, 0)) #text

########################################################################################################################

class province(Facade):
    def __init__(self, data):
        self.name = str(data[0])
        self.id = int(data[1])
        self.X = int(data[2])
        self.Y = int(data[3])
        self.cont = str(data[6])
        self.bonus = int(data[7])
        self.con = list(map(int, data[8:-1]))
        self.HL = False

        self.owner = None
        self.units = None

    def getColor(self):
        if self.owner == None:
            return color["gray"]
        return color["green"]

    @property
    def comm(self):
        return ["prov", self.id]

    @property
    def isOver(self):
        pos = pg.mouse.get_pos()
        dx = abs(pos[0] - self.X*self.scale)
        dy = abs(pos[1] - self.Y*self.scale)
        dist = math.sqrt(dx**2+dy**2)
        if dist <= 20*self.scale:
            return True
        else:
            return False

    @property
    def unitsDIS(self):
        if self.units == None:
            return "?"
        else:
            return str(self.units)

    def show(self):
        if self.isOver:
            border = color["white"]
        else:
            border = color["black"]
        pg.draw.circle(Facade.screen,
                       self.getColor(),
                       (int(self.X*self.scale), int(self.Y*self.scale)),
                       int(19*self.scale), 0)
        pg.draw.circle(Facade.screen, border,
                       (int(self.X*self.scale),
                        int(self.Y*self.scale)), int(20*self.scale),
                       int(3*self.scale))
        self.drawtext(Facade.screen,
                 int(self.X*self.scale), int(self.Y*self.scale),
                 str(self.unitsDIS), 12*self.scale)

