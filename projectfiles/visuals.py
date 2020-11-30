from scratch import *

def visuals_update(self):
    self.reset() #reset of buttons
    s = self.myState #my state
    self.stats = "FPS: " + self.FPS + ", ping: " + self.ping #info about game performance

    lang = "EN"
    if self.langPL == 0: #choose lang. to display on button
        lang = "PL"

    # add button for changing lang. in right corner
    self.addButton(
        [(self.windowSize[0] - 50)/self.scale, 15 , 25, 25, lang, color["lime"], True, True, 1, "changeLang"])
    self.addButton([40, 10, 15, 15, self.stats, color2[0], False, True, 1, None]) #display FPS and ping in left corner
    ########################################################################################################################
    # STAGE -1
    if s == -1: #stage -1, user is in lobby
        self.formatMap() #clear map Image and provinces
        self.backscreen = color["gray"]
        self.addButton([100, 100, 800, 75, self.nick, color["white"], False, False, 5, None]) #display user's nickname
        self.addButton([100, 200, 800, 75, self.langPack[0][self.langPL], color["purple"], True, False, 4, "create"]) #add button "Create Room"
        rooms = self.command("roomlist")
        i = 0
        if rooms is not False:
            for x in rooms:
                if self.langPL == 1: #set room name accoring to lang. and room owner
                    X = self.langPack[21][1] + x
                else:
                    X = x + self.langPack[21][0]
                self.addButton([100, 300 + 75 * i, 800, 50, X, color["green"], True, False, 3, ["join", x]]) #display buttons with room names, user can join room thru them
                i += 1
    elif s in range(10):
        display_players(self) #displays players in room if user is in room
########################################################################################################################
    # STAGE 0
    if s == 0: #stage 0, room, waiting for start
        self.loadmap() #load image file and csv file about map
        if self.imHost:
            self.addButton(
                [self.mapsize[0] + 30, self.mapsize[1] + 30, 125, 35, self.langPack[2][self.langPL], color["yellow"], True, False, 2 - self.langPL,
                 "start"]) #if user is room owner, display START button that can start the game
        i = 0
        for x in self.gameSet: #display game setting, if user is room owner, make it clickable
            self.addButton(
                [self.mapsize[0] + 30, self.mapsize[1] + 30 - 40*(1+i), 125, 35, x, color["yellow"], self.imHost, False, 1,
                 ["gameSet2", i]])
            i += 1
########################################################################################################################
    # STAGE 1
    elif s == 1: #stage 1, observer, nothing user can do
        pass
########################################################################################################################
    # STAGE 2
    elif s == 2: #stage 2, adding new units,
        #add unclickable button, displaying number of units to add
        self.addButton([self.mapsize[0] + 30, self.mapsize[1] + 30, 125, 35, self.langPack[3][self.langPL] + ": " + str(self.newUnits), color["lime"], False, False, 2 - self.langPL, None])
########################################################################################################################
    # STAGE 3
    elif s == 3: #stage 3, choosing the attacker
        self.addButton(
            [self.mapsize[0] + 30, self.mapsize[1] + 30, 125, 35, self.langPack[5][self.langPL], color["lime"], False, False, 2 - self.langPL,
             None]) #display info: "attack"
        self.addButton(
            [self.mapsize[0] + 30 + 150, self.mapsize[1] + 30, 125, 35, self.langPack[4][self.langPL], color["lime"], True, False, 2 - self.langPL,
             "skipAttack"]) #add button that can skip from attacking to fortyfing
########################################################################################################################
    # STAGE 4
    elif s == 4: #stage 4, attacker is choosen, now user have to choose victim or go back to stage 3
        self.addButton(
            [self.mapsize[0] + 30, self.mapsize[1] + 30, 125, 35, self.langPack[5][self.langPL], color["lime"], False, False, 2 - self.langPL,
             None]) #display info: "attack"
########################################################################################################################
    # STAGE 5
    elif s == 5: #stage 5, attacker and victim is choosen, now user chooses tacitc
        self.addButton(
            [self.mapsize[0] + 30, self.mapsize[1] + 30, 125, 35, self.langPack[6][self.langPL], color["lime"], False, False, 2 - self.langPL,
             None]) #display info: "tacic"
        #add buttons about tactic, E - ESCAPE, B - BLITZ, R - ROLL
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
    elif s == 6: #stage 6, choosing how many units take back from taken province
        self.addButton(
            [self.mapsize[0] + 30, self.mapsize[1] + 30, 125, 35, self.langPack[10][self.langPL], color["lime"], False, False, 2 - self.langPL,
             None]) #display info: "move"
        self.renderNumbers(self.HL2) #renders buttons with number, from 0 to self.HL2.units - 1
########################################################################################################################
    # STAGE 7
    elif s == 7: #stage 7, user chooses from where to take units to fortify other province
        self.addButton(
            [self.mapsize[0] + 30, self.mapsize[1] + 30, 125, 35, self.langPack[11][self.langPL], color["lime"], False, False, 2 - self.langPL,
             None]) #display info: "fortify"
        self.addButton(
            [self.mapsize[0] + 30 + 150, self.mapsize[1] + 30, 125, 35, self.langPack[4][self.langPL], color["lime"], True, False, 2 - self.langPL,
             "skipFortify"]) #add button to skip from fortyfing to next turn
########################################################################################################################
    # STAGE 8
    elif s == 8: #stage 8, source of units is choosen, now user chooses desitination
        self.addButton(
            [self.mapsize[0] + 30, self.mapsize[1] + 30, 125, 35, self.langPack[11][self.langPL], color["lime"], False, False, 2 - self.langPL,
             None]) #display info: "FORTIFY"
########################################################################################################################
    # STAGE 9
    elif s == 9: #stage 9, choosing how many units moove from HL to HL2
        self.addButton(
            [self.mapsize[0] + 30, self.mapsize[1] + 30, 125, 35, self.langPack[10][self.langPL], color["lime"], False, False, 2 - self.langPL,
             None]) #display info: "move"
        self.renderNumbers(self.HL) #renders buttons with number, from 0 to self.HL.units - 1
########################################################################################################################

def display_players(self): #display players
    txt = self.turnTime #who have turn now and how much time he has
    self.addButton([self.mapsize[0] + 30, 30, 125, 35, txt, color2[0], False, True, 1, None]) #display info from above
    i = 1
    for x in self.players_list:
        self.addButton([self.mapsize[0] + 30, 30 + 50 * i, 125, 35, x, color2[i-1], False, False, 2, None]) #display player name with color
        if self.imHost:
            if self.nick != x:
                self.addButton([self.mapsize[0] + 160, 30 + 50 * i, 50, 35, self.langPack[1][self.langPL], color2[i - 1], True, False, 1, ["kick", x]])
                #add "kick" button side to the nick if user is room owner
        i += 1
