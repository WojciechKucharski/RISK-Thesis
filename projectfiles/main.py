import pygame as pg
from pygame.locals import *
from network import Network
from Facade import *
############################################################################
pg.init()
pg.display.set_caption("The Game of RISK! - Client ")  # window name
icon = pg.image.load('Data\\Icon\\logo.png')  # loading icon
pg.display.set_icon(icon)  # setting icon
pg.mixer.music.load("Data\\Sound\\bg.wav")  # playing music in loop
nres = (1280-160*2, 720-90*2)
screen = pg.display.set_mode(nres, pg.RESIZABLE)
############################################################################


net = Network()
run = True

f = Facade(nres, screen)
f.butts.append(button(400,100,200,200,"TEST"))

while run:

    for event in pg.event.get():

        f.drag()

        if event.type == pg.QUIT:

            run = False
        elif event.type == pg.VIDEORESIZE:
            if event.w < 854:
                event.w = 854
            if event.h < 480:
                event.h = 480
            screen = pg.display.set_mode((event.w, event.h), pg.RESIZABLE)
            pg.display.update()

        if event.type == pg.KEYDOWN:

            if event.key == pg.K_BACKSPACE:
                print("BS")
            elif event.key == pg.K_RETURN:
                print("ENTER")
            else:
                print(event.unicode)

        if event.type == pg.MOUSEBUTTONDOWN:
            f.click()

        f.show()

