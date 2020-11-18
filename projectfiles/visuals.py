from scratch import *

def visuals_update(self):

    self.reset()
    s = self.myState
    if s == -1:
        setlobby(self)
    elif s == 0:
        loadmap(self)

def setlobby(self):

    self.backscreen = color["gray"]
    self.addButton([100, 100, 800, 75, self.nick, color["white"], False, False, 5, None])
    self.addButton([100, 200, 800, 75, "Create Room", color["purple"], True, False, 4, "create"])

    rooms = self.command("roomlist")
    i = 0
    if rooms is not False:
        for x in rooms:
            self.addButton([100, 300 + 75 * i, 800, 50, x, color["green"], True, False, 3, ["join", x[:-7]]])
            i+=1

def loadmap(self):

    self.mapname = self.command("mapname")
    self.addImage('Data\\Maps\\' + self.mapname + '\\' + self.mapname + '.jpg')
    self.mapsize = list(self.images[0].img.get_size())

    for x in connect_csv('Data\\Maps\\' + self.mapname + '\\' + self.mapname + '.csv'):
        self.addProvince(x)

    i = 0
    for x in self.players_list:
        self.addButton([self.mapsize[0] + 30, 30 + 50 * i, 125, 35, x, color2[i], False, False, 2, None])
        i += 1

    self.update_provs()

