import pygame as pg
from scratch import *

class game:
    def __init__(self, mapname, maxplayers=8, roomname="game", password=""):
        self.mapname = mapname
        self.players = []
        self.provs = []

        for x in connect_csv('Data\\Maps\\' + mapname + '\\' + mapname + '.csv'):
            self.provs.append(province(x))

class province:
    def __init__(self, data):
        self.id = int(data[1])
        self.cont = str(data[6])
        self.bonus = int(data[7])
        self.con = list(map(int, data[8:-1]))
        self.HL = False

        self.owner = None
        self.units = None