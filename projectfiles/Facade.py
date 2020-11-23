import pygame as pg
from scratch import *
import math
from visuals import visuals_update

import time
########################################################################################################################
class Facade:
    screen  = None
    nres    = []
    players_list = []
    provs   = []
    butts   = []
    images  = []
    nick = []

    def __init__(self, screen, net):
        Facade.nres = (1280-160, 720-90)
        Facade.screen = screen
        self.net = net
        self.backscreen = color["black"]

    def update(self, nick):
        Facade.nick = nick
        visuals_update(self)

    @property
    def nick(self):
        return Facade.nick

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

    @property
    def myState(self):
        if self.inLobby:
            return -1
        else:
            return self.command("myState")

    @property
    def scale(self):
        w, h = pg.display.get_surface().get_size()
        if w/h >= 16.0/9.0:
            return h/Facade.nres[1]
        else:
            return w/Facade.nres[0]

    @property
    def obj(self):
        s = self.myState
        if s == -1:
            return Facade.butts
        else:
            return Facade.images + Facade.butts + Facade.provs

    @property
    def players_list(self):
        Facade.players_list = self.command("player_list")
        return Facade.players_list

    def formatMap(self):
        Facade.provs = []
        Facade.images = []

    def addButton(self, recipe):
        Facade.butts.append(button(recipe))

    def addProvince(self, recipe):
        Facade.provs.append(province(recipe))

    def addImage(self, path):
        Facade.images.append(image(path))

    def command(self, input):
        comm = [Facade.nick, "room"]
        if type(input) is list:
            for x in input:
                comm.append(x)
        else:
            comm.append(input)
        return self.net.send(comm)

    def reset(self):
        self.backscreen = color["beige"]
        Facade.butts = []
        Facade.players_list = []

    def click(self):
        comm = None
        for x in Facade.butts:
            if x.isOver:
                if x.comm is not None:
                    comm = x.comm
        if comm is not None:
            self.command(comm)
        else:
            comm = ["provClick", None]
            for x in Facade.provs:
                if x.isOver:
                    comm = ["provClick", x.id]
            self.command(comm)

    def renderNumbers(self, NO):
        if Facade.provs[NO].units == 1:
            self.command(["number", 0])
        else:
            for x in range(Facade.provs[NO].units):
                self.addButton(
                    [15 + 30*x, self.mapsize[1] + 15, 25, 25, str(x), color["lime"], True, False, 2,
                    ["number", x]])

    def show(self):
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

    def download_prov_info(self):
        Facade.players_list = self.command("player_list")
        for x in Facade.provs:
            response = self.command(["prov", x.id])
            x.owner = response[0]
            x.units = response[1]

    def update_provs(self):
        Facade.players_list = self.command("player_list")

        for x in Facade.provs:
            response = self.command(["prov", x.id])
            x.owner = response[0]
            x.units = response[1]
            x.clickable = False
            x.HL = False

        s = self.myState
        HL = self.command("HL")
        HL2 = self.command("HL2")

        if HL2 is not None:
            if Facade.provs[HL2].owner == self.nick or s != 1:
                Facade.provs[HL2].HL = True
        if HL is not None:
            Facade.provs[HL].HL = True
        if s in [0, 1, 5, 6]:
            pass
        elif s in [2, 3, 7, 8]:
            for x in Facade.provs:
                if x.owner == self.nick:
                    x.clickable = True
        elif s == 4:
            if HL is not None:
                for x in Facade.provs[HL].con:
                    if Facade.provs[x].owner != self.nick:
                        Facade.provs[x].clickable = True
        elif s == 9:
            pass
        else:
            pass



########################################################################################################################

class button(Facade):
    def __init__(self, recipe): #X, Y, dx, dy, text, color = (128, 128, 128), clickable = True, textonly = False, font_amp = 1, comm = None
        self.X = recipe[0]
        self.Y = recipe[1]
        self.dx = recipe[2]
        self.dy = recipe[3]
        self.text = recipe[4]
        self.color = recipe[5]
        self.clickable = recipe[6]
        self.textonly = recipe[7]
        self.font_amp = recipe[8]
        self.comm_c = recipe[9]

    @property
    def comm(self):
        if self.clickable:
            return self.comm_c
        else:
            return None

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
        self.clickable = True

        self.owner = None
        self.units = None

    def getColor(self):
        if self.owner in Facade.players_list:
            return color2[Facade.players_list.index(self.owner)]
        else:
            return color["gray"]

    @property
    def comm(self):
        if self.clickable and self.visible:
            return self.id
        else:
            return None

    @property
    def isOver(self):
        if self.clickable is False:
            return False
        if self.visible is False:
            return False
        pos = pg.mouse.get_pos()
        dx = abs(pos[0] - self.X*self.scale)
        dy = abs(pos[1] - self.Y*self.scale)
        dist = math.sqrt(dx**2+dy**2)
        if dist <= 20*self.scale:
            return True
        else:
            return False

    @property
    def visible(self):
        if self.owner == Facade.nick:
            return True
        for x in self.con:
            if Facade.provs[x].owner == Facade.nick:
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
        if self.visible:
            self.show2()

    def show2(self):
        border = color["black"]
        if self.HL:
            border = color["beige"]
        if self.isOver:
            border = color["white"]
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
        return False


