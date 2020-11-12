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


class game:
    def __init__(self, creator, mapname = "map"):
        self.room_name = creator + "'s Room"
        self.creator = creator
        self.mapname = mapname
        self.players = []
        self.provs = []
        for x in connect_csv('Data\\Maps\\' + self.mapname + '\\' + self.mapname + '.csv'):
            self.provs.append(province(x))
        self.addplayer(creator)

    def addplayer(self, nick):
        self.players.append(nick)
        adding = True
        while adding:
            R = random.randint(0, len(self.provs))
            if self.provs[R].owner == None:
                self.provs[R].owner = nick
                self.provs[R].units = 3
                adding = False





class province:
    def __init__(self, data):
        self.id = int(data[1])
        self.cont = str(data[6])
        self.bonus = int(data[7])
        self.con = list(map(int, data[8:-1]))
        self.HL = False
        self.owner = None
        self.units = None