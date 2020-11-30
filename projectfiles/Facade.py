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
        self.FPS_ = 0

        self.langPack = connect_csv('Data\\Lang\\lang.csv')
        self.langPL = 0
        print(self.langPack)
        self.mapsize = (0, 0)
        self.mapname = None
        self.myState = -1
        self.imHost = None
        self.HL = None
        self.HL2 = None
        self.newUnits = None
        self.turnTime = None
        self.ping = None
        self.players_list = []
        self.fow = True
        self.stats = None

        self.UT = 0

        self.sound = [(pg.mixer.Sound("Data\\Sound\\cl.wav")), pg.mixer.Sound("Data\\Sound\\ex.wav"),
                      pg.mixer.Sound("Data\\Sound\\ar.wav")]
        for x in self.sound:
            x.set_volume(0.05)

    def play_sound(self, no):
        pg.mixer.Sound.play(self.sound[no-1])
        if no == 3:
            N = self.sound[no - 1].get_length()
            self.sound[no - 1].fadeout(int(N * 150))

    def update(self, nick):
        Facade.nick = nick
        self.updateGameInfo()
        visuals_update(self)

    def updateGameInfo(self):
        if not self.updateTime:
            return True

        b = time.time()
        self.myState = self.command("myState")
        b = time.time() - b
        self.ping = str(math.floor(1000 * b))

        if self.myState == -1:
            return True

        response = self.command("gameInfo")
        self.mapname = response[0]
        self.imHost = response[2]
        self.HL = response[3]
        self.HL2 = response[4]
        self.newUnits = response[5]
        self.turnTime = response[6]
        Facade.players_list = response[7]
        self.players_list = response[7]
        self.fow = response[8]
        if self.myState != response[1] and response[1] == 2:
            self.play_sound(3)

        if len(Facade.provs) > 0:
            response = self.command("provinces")
            i = 0
            for x in response:
                Facade.provs[i].units = x[0]
                Facade.provs[i].owner = x[1]
                i+=1

        if self.myState == 0:
            self.gameSet = self.command("gameSet")
            print(self.gameSet)
            for x in range(2):
                self.gameSet[x] = self.langPack[12+x][self.langPL] + ": " + self.langPack[20 - int(self.gameSet[x])][self.langPL]
            for x in range(5):
                self.gameSet[x+2] = self.langPack[14+x][self.langPL] + ": " + str(self.gameSet[x+2])
            self.loadmap()

        if self.myState != -1:
            self.update_provs()

    @property
    def windowSize(self):
        w, h = pg.display.get_surface().get_size()
        return [w, h]

    @property
    def FPS(self):
        F = time.time() - self.FPS_
        self.FPS_ = time.time()
        return str(math.floor(1/F))

    @property
    def updateTime(self):
        return True
        x = time.time() - self.UT
        y = 0
        if self.myState in [-1, 0]:
            pass
        if self.myState == 1:
            y = 1
        else:
            y = 0.2
        if x > y:
            self.UT = time.time()
            return True
        else:
            return False
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
        self.play_sound(1)
        comm = None
        for x in Facade.butts:
            if x.isOver:
                if x.comm is not None:
                    comm = x.comm
        if comm is not None:
            res = self.command(comm)
            if comm == ["Tactic", "R"]:
                self.rolls(res)
            elif comm == ["Tactic", "B"]:
                self.play_sound(2)
            elif comm[0] == "number":
                if comm[1] != 0:
                    self.play_sound(3)
            elif comm == "changeLang":
                if self.langPL == 0:
                    self.langPL = 1
                else:
                    self.langPL = 0
        else:
            comm = ["provClick", None]
            for x in Facade.provs:
                if x.isOver:
                    comm = ["provClick", x.id]
            self.command(comm)

    def loadmap(self):
        self.formatMap()
        self.addImage('Data\\Maps\\' + self.mapname + '\\' + self.mapname + '.jpg')
        self.mapsize = list(self.images[0].img.get_size())
        for x in connect_csv('Data\\Maps\\' + self.mapname + '\\' + self.mapname + '.csv'):
            self.addProvince(x)

    def rolls(self, roll):
        A = len(roll[0])
        D = len(roll[1])
        i = 0
        for x in roll[0]:
            self.addButton(
                [self.mapsize[0] + 30, self.mapsize[1] - 220 + 30*i, 25, 25, str(x), Facade.provs[self.HL].getColor(), False, False,
                2.5, None])
            i+=1
        i = 0
        for x in roll[1]:
            self.addButton(
                [self.mapsize[0] + 65, self.mapsize[1] - 220 + 30 * i, 25, 25, str(x), Facade.provs[self.HL2].getColor(), False,
                    False, 2.5, None])
            i += 1

        self.show()
        time.sleep(1)
        for x in range(min(len(roll[0]), len(roll[1]))):
            if roll[0][x] > roll[1][x]:
                Facade.butts[x-D-A].X += 15
                Facade.butts[x-D].X += 500
            else:
                Facade.butts[x-D - A].X += 500
                Facade.butts[x-D].X -= 15
            self.show()
            self.play_sound(2)
            time.sleep(1)
        time.sleep(1)

    def renderNumbers(self, NO):
        if Facade.provs[NO].units == 1:
            self.command(["number", 0])
        else:
            for x in range(Facade.provs[NO].units):
                dx = 20
                dy = 2
                a = x % 35
                b = x // 35
                self.addButton(
                    [15 + (dx+dy) * a, self.mapsize[1] + 15 + (dx+dy) * b, dx, dx, str(x), color["lime"], True, False, 1,
                    ["number", x]])

    def update_provs(self):

        for x in Facade.provs:
            x.clickable = False
            x.HL = False
            x.av = not self.fow
            if x.owner in self.players_list:
                x.col = color2[self.players_list.index(x.owner)]
            else:
                x.col = None

        s = self.myState
        HL = self.HL
        HL2 = self.HL2

        if HL2 is not None:
            if Facade.provs[HL2].owner == self.nick or s != 1:
                Facade.provs[HL2].HL = True
        if HL is not None:
            Facade.provs[HL].HL = True
        if s in [0, 1, 5, 6]:
            pass
        elif s in [2, 3, 7]:
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
        elif s == 8:
            if HL is not None:
                for x in self.connected([HL]):
                    if Facade.provs[x].owner == self.nick:
                        Facade.provs[x].clickable = True
        else:
            pass

    def connected(self, id):
        new = False
        for x in id:
            for y in Facade.provs[x].con:
                if Facade.provs[int(y)].owner == self.nick:
                    if y in id:
                        pass
                    else:
                        new = True
                        id.append(y)
        if new:
            return self.connected(id)
        else:
            return id

    def drawtext(self, screen, X, Y, text, fontsize, color=(0, 0, 0)):
        font = pg.font.Font("Data\\Font\\arial.ttf", math.floor(fontsize * 1))
        TextSurf = font.render(text, True, color)
        TextRect = TextSurf.get_rect()
        TextRect.center = (X, Y)
        screen.blit(TextSurf, TextRect)

    def show(self):
        self.screen.fill(self.backscreen)
        for x in self.obj:
            x.show()
        pg.display.update()

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
        self.col = None
        self.av = False

        self.owner = None
        self.units = None

    def getColor(self):
        if self.col == None:
            return color["gray"]
        else:
            return self.col

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
        if self.av:
            return True
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


