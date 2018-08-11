import pygame
import ImageUtil
from Constants import *

icons = []


def initUI():
    global icons
    loadImages()
    icons.append(("menu-pause", 0, (0,0)))
    icons.append(("menu-city", 1, (UI_ICON_SIZE*1, 0)))
    icons.append(("menu-build-road", 2, (UI_ICON_SIZE*2, 0)))

def loadImages():
    ImageUtil.create_image("menu-pause", "res/menu/menu-pause.png", False)
    ImageUtil.create_image("menu-city", "res/menu/menu-city.png", False)
    ImageUtil.create_image("menu-build-road", "res/menu/menu-build-road.png", False)
    



def render(screen):
    global icons
    for i in icons:
        if(i != None):
            screen.blit(ImageUtil.get_image(i[0]), (i[2][0], i[2][1]))