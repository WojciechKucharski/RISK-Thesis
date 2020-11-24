from scratch import *
from comm_int import *
import random
import time
import math

class lobby:
    def __init__(self):
        self.rooms = []

    def command(self, command):
        return command_int(self, command)

    def create_room(self, creator):
        self.rooms.append(game(creator))

    def index(self, room_name):
        i = 0
        for x in self.rooms:
            if x.creator == room_name:
                return i
            else:
                i+=1

    def whereIam(self, nick):
        if len(self.rooms) == 0:
            return "lobby"
        else:
            for x in self.rooms:
                if nick in x.players:
                    return x.creator
            return "lobby"

    def clear_rooms(self):
        for x in self.rooms:
            if len(x.players) == 0:
                self.rooms.remove(x)

class game:
    def __init__(self, creator, mapname = "map"):
        self.room_name = creator + "'s Room"
        self.turn_time = 0
        self.maxTT = 150
        self.creator = creator
        self.mapname = mapname
        self.players = []
        self.provs = []
        self.game_started = False
        self.HL = None
        self.HL2 = None
        self.turn_time = 0
        for x in connect_csv('Data\\Maps\\' + self.mapname + '\\' + self.mapname + '.csv'):
            self.provs.append(province(x))
            self.provs[-1].units = 0
        self.addplayer(creator)

        self.turn = creator

        self.player_state = 0
        self.new_units = 0

    def gameInfo(self, nick):
        res = []
        res.append(self.mapname)
        res.append(self.myState(nick))
        res.append(self.imHost(nick))
        res.append(self.HL)
        res.append(self.HL2)
        res.append(self.new_units)
        res.append(self.gettime)
        res.append(self.players)
        return res
    @property
    def provinces(self):
        res = []
        for x in self.provs:
            res.append([x.units, x.owner])
        return res
    @property
    def gettime(self):
        if self.game_started is False:
            return "Waiting..."
        else:
            R = time.time() - self.turn_time
            if R > self.maxTT:
                self.next_turn()
            return "Turn time: " + str(math.floor(self.maxTT - R))

    @property
    def n_players(self):
        return len(self.players)

    @property
    def mProv(self):
        my_provinces = []
        for x in self.provs:
            if x.owner == self.turn:
                my_provinces.append(int(x.id))
        return my_provinces

    @property
    def add_new_units(self):
        new = 0
        cont = []
        cont_own = []
        new += math.ceil(len(self.mProv)/3)
        for x in self.provs:
            if x.cont in cont:
                pass
            else:
                cont.append(x.cont)
                cont_own.append(0)
            if x.owner == self.turn:
                if cont_own[cont.index(x.cont)] != -1:
                    cont_own[cont.index(x.cont)] = x.bonus
            else:
                cont_own[cont.index(x.cont)] = -1

        for x in cont_own:
            if x < 0:
                x = 0
            new += x
        return new

    def imHost(self, nick):
        if nick == self.creator:
            return True
        else:
            return False

    def myState(self, nick):
        if self.game_started == False:
            return 0
        elif self.myTurn(nick) is False:
            return 1
        elif self.myTurn(nick) and self.new_units > 0:
            return 2
        else:
            return self.player_state

    def myTurn(self, nick):
        if nick == self.turn:
            return True
        else:
            return False

    def skipAttack(self, nick):
        if nick == self.turn:
            self.HL = None
            self.HL2 = None
            self.player_state = 7

    def skipFortify(self, nick):
        if nick == self.turn:
            self.HL = None
            self.HL2 = None
            self.next_turn()

    def startGame(self, nick):

        for x in self.players:
            adding = 0
            while adding < 1:
                R = random.randint(0, len(self.provs)-1)
                if self.provs[R].owner == None:
                    self.provs[R].owner = x
                    self.provs[R].units = 3
                    adding += 1

        if self.imHost(nick):
            self.game_started = True
            self.next_turn()
        else:
            return False

    def Tactic(self, nick, T):
        if nick != self.turn:
            return False
        else:
            if T == "E":
                self.HL = None
                self.HL2 = None
                self.player_state = 3
            elif T =="R":
                self.fight()
            elif T == "B":
                while self.player_state not in [3, 6]:
                    self.fight()
            print("###########")
            print(self.HL, self.HL2)

    def fight(self):
            print("fajt")
            off = []
            deff = []
            off_n = min(3, self.provs[self.HL].units - 1)
            deff_n = min(2, self.provs[self.HL2].units)
            for _ in range(off_n):
                off.append(random.randint(1, 6))
            for _ in range(deff_n):
                deff.append(random.randint(1, 6))
            off.sort(reverse=True)
            deff.sort(reverse=True)

            for x in range(min(off_n, deff_n)):
                if off[x] > deff[x]:
                    self.provs[self.HL2].units -= 1
                else:
                    self.provs[self.HL].units -= 1

            if self.provs[self.HL].units == 1:
                self.HL = None
                self.HL2 = None
                self.player_state = 3

            elif self.provs[self.HL2].units == 0:
                self.provs[self.HL2].units = self.provs[self.HL].units - 1
                self.provs[self.HL2].owner = self.provs[self.HL].owner
                self.provs[self.HL].units = 1
                self.player_state = 6

                print("###########")
                print(self.HL, self.HL2)

    def number(self, nick, no):
        if nick != self.turn:
            return False
        else:
            if self.player_state == 5:
                self.HL = None
                self.HL2 = None
                self.player_state = 3
            elif self.player_state == 9:
                if no == 0:
                    self.HL = None
                    self.HL2 = None
                    self.player_state = 7
                elif no < self.provs[self.HL].units:
                    self.provs[self.HL].units -= no
                    self.provs[self.HL2].units += no
                    self.HL = None
                    self.HL2 = None
                    self.next_turn()
                else:
                    return False
            elif self.player_state == 6:
                if no < self.provs[self.HL2].units:
                    self.provs[self.HL].units += no
                    self.provs[self.HL2].units -= no
                    self.HL = None
                    self.HL2 = None
                    self.player_state = 3
                else:
                    return False

    def provClick(self, nick, id):
        if nick != self.turn:
            return False

        if self.myState(nick) == 1:
            return False

        if id is None:
            if self.player_state in [4, 8, 9]:
                if self.player_state == 4:
                    self.player_state = 3
                    self.HL = None
                    self.HL2 = None
                elif self.player_state == 8:
                    self.player_state = 7
                    self.HL = None
                    self.HL2 = None
                elif self.player_state == 9:
                    self.player_state = 8
                    self.HL2 = None
                return False
            else:
                return False


        elif self.player_state == 2:
            if self.provs[id].owner == nick and self.new_units > 0:
                self.provs[id].units += 1
                self.new_units -= 1
            if self.new_units == 0:
                self.player_state = 3

        elif self.player_state == 3:
            if self.provs[id].owner == nick:
                if self.provs[id].units > 1:
                    self.HL = id
                    self.player_state = 4

        elif self.player_state == 4:
            if self.provs[id].owner != nick:
                if self.provs[id].units == 0:
                    self.provs[id].owner = nick
                    self.provs[id].units = self.provs[self.HL].units - 1
                    self.provs[self.HL].units = 1
                    self.HL2 = id
                    self.player_state = 6
                else:
                    self.HL2 = id
                    self.player_state = 5

        elif self.player_state == 7:
            if self.provs[id].owner == nick:
                if self.provs[id].units > 1:
                    self.HL = id
                    self.player_state = 8

        elif self.player_state == 8:
            if self.provs[id].owner == nick:
                if self.HL != id:
                    self.HL2 = id
                    self.player_state = 9


    def next_turn(self):
        self.HL = None
        self.HL2 = None
        i = self.players.index(self.turn)
        i+=1
        if i >= self.n_players:
            i = 0
        self.turn = self.players[i]
        self.player_state = 2
        self.new_units = self.add_new_units
        self.turn_time = time.time()

    def addplayer(self, nick):
        if self.game_started is False:
           self.players.append(nick)

    def rmplayer(self, nick):
        if self.creator == nick:
            if len(self.players) > 1:
                self.creator = self.players[1]
        if self.turn == nick:
            if len(self.players) > 1:
                self.next_turn()
        self.players.remove(nick)

class province:
    def __init__(self, data):
        self.id = int(data[1])
        self.cont = str(data[6])
        self.bonus = int(data[7])
        self.con = list(map(int, data[8:-1]))
        self.HL = False
        self.owner = None
        self.units = None