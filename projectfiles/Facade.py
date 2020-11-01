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

    def __init__(self, screen):
        Facade.nres = (1280-160, 720-90)
        Facade.screen = screen
        self.backscreen = color["beige"]


    def loadmap(self, mapname):
        self.mapname = mapname
        Facade.images.append(image('Data\\Maps\\' + mapname + '\\' + mapname + '.jpg'))
        self.mapsize = list(self.images[0].img.get_size())
        for x in connect_csv('Data\\Maps\\' + mapname + '\\' + mapname + '.csv'):
            Facade.provs.append(province(x))
        self.butts.append(button(self.mapsize[0]+25, 25, 75, 25, "Button", color["green"]))

    def drag(self):
        pos = pg.mouse.get_pos()

    def click(self):
        pos = pg.mouse.get_pos()

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
    def __init__(self, X, Y, dx, dy, text, color = (128, 128, 128)): #button object init, if no color given, GRAY
        self.X = X #left corner X
        self.Y = Y #left corner Y
        self.dx = dx #width
        self.dy = dy #height
        self.text = text
        self.color = color

    @property
    def isOver(self): #function that tells if mouse is over this object
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
        pg.draw.rect(Facade.screen, self.color, (self.X*self.scale, self.Y*self.scale, self.dx*self.scale, self.dy*self.scale), 0) #background rectangle
        pg.draw.rect(Facade.screen, border, (self.X*self.scale, self.Y*self.scale, self.dx*self.scale, self.dy*self.scale), 3) #border
        self.drawtext(Facade.screen, self.X*self.scale + self.dx*self.scale/2, self.Y*self.scale + self.dy*self.scale/2, str(self.text), 12*self.scale, (0, 0, 0)) #text

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
    def isOver(self):
        pos = pg.mouse.get_pos()
        dx = abs(pos[0] - self.X*self.scale)
        dy = abs(pos[1] - self.Y*self.scale)
        dist = math.sqrt(dx**2+dy**2)
        if dist <= 20*self.scale:
            return True
        else:
            return False

    def show(self):
        pg.draw.circle(Facade.screen,
                       self.getColor(),
                       (int(self.X*self.scale), int(self.Y*self.scale)),
                       int(19*self.scale), 0)
        pg.draw.circle(Facade.screen, color["black"],
                       (int(self.X*self.scale),
                        int(self.Y*self.scale)), int(20*self.scale),
                       int(3*self.scale))
        self.drawtext(Facade.screen,
                 int(self.X*self.scale), int(self.Y*self.scale),
                 str(self.units), 12*self.scale)

        if self.HL is not False:
            pg.draw.circle(Facade.screen, self.HL, (int(self.X * self.scale), int(self.Y * self.scale)), int(22*self.scale), int(5*self.scale))

        if self.isOver:
            pg.draw.circle(Facade.screen, color["white"], (int(self.X * self.scale), int(self.Y * self.scale)), int(22*self.scale), int(5*self.scale))
