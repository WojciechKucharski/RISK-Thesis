import pygame as pg
from scratch import *
from comm_int import *
import random

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
        self.creator = creator
        self.mapname = mapname
        self.players = []
        self.provs = []
        for x in connect_csv('Data\\Maps\\' + self.mapname + '\\' + self.mapname + '.csv'):
            self.provs.append(province(x))
            self.provs[-1].units = 0
        self.addplayer(creator)

        self.turn = creator
        self.game_started = False

        self.HL = None
        self.HL2 = None
        self.turn_time = 0

        self.player_state = 0
        self.new_units = 0

    @property
    def n_players(self):
        return len(self.players)

    @property
    def add_new_units(self):
        return 3

    def imHost(self, nick):
        if nick == self.creator:
            return True
        else:
            return False

    def myTurn(self, nick):
        if nick == self.turn:
            return True
        else:
            return False

    def startGame(self, nick):

        for x in self.players:
            adding = 0
            while adding < 20:
                R = random.randint(0, len(self.provs)-1)
                print(R)
                if self.provs[R].owner == None:
                    self.provs[R].owner = x
                    self.provs[R].units = 3
                    adding += 1

        if self.imHost(nick):
            self.game_started = True
            self.next_turn()
        else:
            return False

    def provClick(self, nick, id):
        if nick != self.turn:
            return False

        if self.player_state == 1:
            pass

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
                    self.HL = None
                    self.player_state = 3
                else:
                    self.HL2 = id
                    self.player_state = 5


    def next_turn(self):
        i = self.players.index(self.turn)
        i+=1
        if i >= self.n_players:
            i = 0
        self.turn = self.players[i]
        self.player_state = 2
        self.new_units = self.add_new_units

    def addplayer(self, nick):
        self.players.append(nick)

    def rmplayer(self, nick):
        if self.creator == nick:
            if len(self.players) > 1:
                self.creator = self.players[1]
        if self.turn == nick:
            if len(self.players) > 1:
                self.turn = self.players[1]
        self.players.remove(nick)

    def myState(self, nick):
        if self.game_started == False:
            return 0
        elif self.myTurn(nick) is False:
            return 1
        elif self.myTurn(nick) and self.new_units > 0:
            return 2
        else:
            return self.player_state

class province:
    def __init__(self, data):
        self.id = int(data[1])
        self.cont = str(data[6])
        self.bonus = int(data[7])
        self.con = list(map(int, data[8:-1]))
        self.HL = False
        self.owner = None
        self.units = None