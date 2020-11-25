from scratch import *

def visuals_update(self):
    self.reset()
    s = self.myState
    if s == -1:
        setlobby(self)
    elif s in range(10):
        if s == 0:
            loadmap(self)
        display_players(self)
        self.update_provs()

    if s == 0:
        loadmap(self)
        if self.imHost:
            self.addButton(
                [self.mapsize[0] + 30, self.mapsize[1] + 30, 125, 35, "START", color["yellow"], True, False, 2,
                 "start"])
        info = self.command("gameSet")
        i = 0
        for x in info:
            self.addButton(
                [self.mapsize[0] + 30, self.mapsize[1] + 30 - 40*(1+i), 125, 35, x, color["yellow"], self.imHost, False, 1,
                 ["gameSet2", i]])
            i += 1
    elif s == 1:
        pass
    elif s == 2:
        new = self.newUnits
        self.addButton(
            [self.mapsize[0] + 30, self.mapsize[1] + 30, 125, 35, "ADD: " + str(new), color["lime"], False, False, 2,
             None])
    elif s == 3:
        self.addButton(
            [self.mapsize[0] + 30, self.mapsize[1] + 30, 125, 35, "ATTACK", color["lime"], False, False, 2,
             None])
        self.addButton(
            [self.mapsize[0] + 30 + 150, self.mapsize[1] + 30, 125, 35, "SKIP", color["lime"], True, False, 2,
             "skipAttack"])
    elif s == 4:
        self.addButton(
            [self.mapsize[0] + 30, self.mapsize[1] + 30, 125, 35, "ATTACK", color["lime"], False, False, 2,
             None])
    elif s == 5:
        self.addButton(
            [self.mapsize[0] + 30, self.mapsize[1] + 30, 125, 35, "TACTIC", color["lime"], False, False, 2,
             None])
        self.addButton(
            [self.mapsize[0] + 30, self.mapsize[1] - 30, 125, 35, "ESCAPE", color["lime"], True, False, 2,
             ["Tactic", "E"]])
        self.addButton(
            [self.mapsize[0] + 30, self.mapsize[1] - 75, 125, 35, "BLITZ", color["lime"], True, False, 2,
             ["Tactic", "B"]])
        self.addButton(
            [self.mapsize[0] + 30, self.mapsize[1] - 120, 125, 35, "ROLL", color["lime"], True, False, 2,
             ["Tactic", "R"]])
    elif s == 6:
        self.addButton(
            [self.mapsize[0] + 30, self.mapsize[1] + 30, 125, 35, "MOVE", color["lime"], False, False, 2,
             None])
        self.renderNumbers(self.HL2)
    elif s == 7:
        self.addButton(
            [self.mapsize[0] + 30, self.mapsize[1] + 30, 125, 35, "FORTIFY", color["lime"], False, False, 2,
             None])
        self.addButton(
            [self.mapsize[0] + 30 + 150, self.mapsize[1] + 30, 125, 35, "SKIP", color["lime"], True, False, 2,
             "skipFortify"])
    elif s == 8:
        self.addButton(
            [self.mapsize[0] + 30, self.mapsize[1] + 30, 125, 35, "FORTIFY", color["lime"], False, False, 2,
             None])
    elif s == 9:
        self.addButton(
            [self.mapsize[0] + 30, self.mapsize[1] + 30, 125, 35, "MOVE", color["lime"], False, False, 2,
             None])
        self.renderNumbers(self.HL)

def display_players(self):

    self.addButton([40, 10, 15, 15, self.stats, color2[0], False, True, 1, None])
    txt = self.turnTime
    self.addButton([self.mapsize[0] + 30, 30, 125, 35, txt, color2[0], False, True, 1, None])
    i = 1
    for x in self.players_list:
        self.addButton([self.mapsize[0] + 30, 30 + 50 * i, 125, 35, x, color2[i-1], False, False, 2, None])
        i += 1

def loadmap(self):
    self.formatMap()
    self.addImage('Data\\Maps\\' + self.mapname + '\\' + self.mapname + '.jpg')
    self.mapsize = list(self.images[0].img.get_size())
    for x in connect_csv('Data\\Maps\\' + self.mapname + '\\' + self.mapname + '.csv'):
        self.addProvince(x)

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