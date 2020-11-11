import pygame as pg
from scratch import *
from comm_int import *


class lobby:
    def __init__(self):
        self.rooms = []

    def command(self, command):
        return command_int(self, command)

    def create_room(self, creator):
        self.rooms.append(game(creator))

class game:
    def __init__(self, creator, mapname = "map"):
        self.room_name = creator + "'s Room"
        self.mapname = mapname
        self.players = []
        self.provs = []

        for x in connect_csv('Data\\Maps\\' + mapname + '\\' + mapname + '.csv'):
            self.provs.append(province(x))

    def __str__(self):
        return

class province:
    def __init__(self, data):
        self.id = int(data[1])
        self.cont = str(data[6])
        self.bonus = int(data[7])
        self.con = list(map(int, data[8:-1]))
        self.HL = False
        self.owner = None
        self.units = None