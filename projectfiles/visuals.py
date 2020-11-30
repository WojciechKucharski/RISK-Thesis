from scratch import *

def visuals_update(self):
    self.reset() #reset of buttons
    s = self.myState #my state
    self.stats = "FPS: " + self.FPS + ", ping: " + self.ping #info about game performance
    lang = "EN"
    if self.langPL == 0:
        lang = "PL"
    self.addButton(
        [(self.windowSize[0] - 50)/self.scale, 15 , 25, 25, lang, color["lime"], True, True, 1, "changeLang"])
    self.addButton([40, 10, 15, 15, self.stats, color2[0], False, True, 1, None])
    ########################################################################################################################
    # STAGE -1
    if s == -1:
        self.formatMap()
        self.backscreen = color["gray"]
        self.addButton([100, 100, 800, 75, self.nick, color["white"], False, False, 5, None])
        self.addButton([100, 200, 800, 75, self.langPack[0][self.langPL], color["purple"], True, False, 4, "create"])
        rooms = self.command("roomlist")
        i = 0
        if rooms is not False:
            for x in rooms:
                if self.langPL == 1:
                    X = self.langPack[21][1] + x
                else:
                    X = x + self.langPack[21][0]
                self.addButton([100, 300 + 75 * i, 800, 50, X, color["green"], True, False, 3, ["join", x]])
                i += 1
    elif s in range(10):
        display_players(self)
########################################################################################################################
    # STAGE 0
    if s == 0:
        self.loadmap()
        if self.imHost:
            self.addButton(
                [self.mapsize[0] + 30, self.mapsize[1] + 30, 125, 35, self.langPack[2][self.langPL], color["yellow"], True, False, 2 - self.langPL,
                 "start"])
        i = 0
        for x in self.gameSet:
            self.addButton(
                [self.mapsize[0] + 30, self.mapsize[1] + 30 - 40*(1+i), 125, 35, x, color["yellow"], self.imHost, False, 1,
                 ["gameSet2", i]])
            i += 1
########################################################################################################################
    # STAGE 1
    elif s == 1:
        pass
########################################################################################################################
    # STAGE 2
    elif s == 2:
        self.addButton([self.mapsize[0] + 30, self.mapsize[1] + 30, 125, 35, self.langPack[3][self.langPL] + ": " + str(self.newUnits), color["lime"], False, False, 2 - self.langPL, None])
########################################################################################################################
    # STAGE 3
    elif s == 3:
        self.addButton(
            [self.mapsize[0] + 30, self.mapsize[1] + 30, 125, 35, self.langPack[5][self.langPL], color["lime"], False, False, 2 - self.langPL,
             None])
        self.addButton(
            [self.mapsize[0] + 30 + 150, self.mapsize[1] + 30, 125, 35, self.langPack[4][self.langPL], color["lime"], True, False, 2 - self.langPL,
             "skipAttack"])
########################################################################################################################
    # STAGE 4
    elif s == 4:
        self.addButton(
            [self.mapsize[0] + 30, self.mapsize[1] + 30, 125, 35, self.langPack[5][self.langPL], color["lime"], False, False, 2 - self.langPL,
             None])
########################################################################################################################
    # STAGE 5
    elif s == 5:
        self.addButton(
            [self.mapsize[0] + 30, self.mapsize[1] + 30, 125, 35, self.langPack[6][self.langPL], color["lime"], False, False, 2 - self.langPL,
             None])
        self.addButton(
            [self.mapsize[0] + 30, self.mapsize[1] - 30, 125, 35, self.langPack[7][self.langPL], color["lime"], True, False, 2 - self.langPL,
             ["Tactic", "E"]])
        self.addButton(
            [self.mapsize[0] + 30, self.mapsize[1] - 75, 125, 35, self.langPack[8][self.langPL], color["lime"], True, False, 2 - self.langPL,
             ["Tactic", "B"]])
        self.addButton(
            [self.mapsize[0] + 30, self.mapsize[1] - 120, 125, 35, self.langPack[9][self.langPL], color["lime"], True, False, 2 - self.langPL,
             ["Tactic", "R"]])
########################################################################################################################
    # STAGE 6
    elif s == 6:
        self.addButton(
            [self.mapsize[0] + 30, self.mapsize[1] + 30, 125, 35, self.langPack[10][self.langPL], color["lime"], False, False, 2 - self.langPL,
             None])
        self.renderNumbers(self.HL2)
########################################################################################################################
    # STAGE 7
    elif s == 7:
        self.addButton(
            [self.mapsize[0] + 30, self.mapsize[1] + 30, 125, 35, self.langPack[11][self.langPL], color["lime"], False, False, 2 - self.langPL,
             None])
        self.addButton(
            [self.mapsize[0] + 30 + 150, self.mapsize[1] + 30, 125, 35, self.langPack[4][self.langPL], color["lime"], True, False, 2 - self.langPL,
             "skipFortify"])
########################################################################################################################
    # STAGE 8
    elif s == 8:
        self.addButton(
            [self.mapsize[0] + 30, self.mapsize[1] + 30, 125, 35, self.langPack[11][self.langPL], color["lime"], False, False, 2 - self.langPL,
             None])
########################################################################################################################
    # STAGE 9
    elif s == 9:
        self.addButton(
            [self.mapsize[0] + 30, self.mapsize[1] + 30, 125, 35, self.langPack[10][self.langPL], color["lime"], False, False, 2 - self.langPL,
             None])
        self.renderNumbers(self.HL)
########################################################################################################################

def display_players(self):
    txt = self.turnTime
    self.addButton([self.mapsize[0] + 30, 30, 125, 35, txt, color2[0], False, True, 1, None])
    i = 1
    for x in self.players_list:
        self.addButton([self.mapsize[0] + 30, 30 + 50 * i, 125, 35, x, color2[i-1], False, False, 2, None])
        if self.imHost:
            if self.nick != x:
                self.addButton([self.mapsize[0] + 160, 30 + 50 * i, 50, 35, self.langPack[1][self.langPL], color2[i - 1], True, False, 1, ["kick", x]])
        i += 1
