import pygame
import ImageUtil
from Constants import *
import Map
import Build

icons = []


isMenuCompanyOpen = False


def initUI(functionPause):
    global icons
    loadImages()

    # (imagename, id, (xpos, ypos), onClickFunction, isToggleable, isToggled, function parameter)

    icons.append(["menu-pause", 0, (0,0), functionPause, True, False, None])
    icons.append(["menu-city", 1, (UI_ICON_SIZE*1, 0), openMenu, False, False, 1])
    icons.append(["menu-company",2,  (UI_ICON_SIZE*2, 0), openMenu, False, False, 2])
    icons.append(["menu-build-road", 3, (UI_ICON_SIZE*3, 0), setBuildMode, True, False, BUILD_MODE_ROAD])
    icons.append(["menu-build-landfill", 4, (UI_ICON_SIZE*4, 0), setBuildMode, True, False, BUILD_MODE_LANDFILL])
    icons.append(["menu-trucks", 5, (UI_ICON_SIZE*5, 0), openMenu, False, True, 5])
    

def loadImages():
    ImageUtil.create_image("menu-pause", "res/menu/menu-pause.png", False)
    ImageUtil.create_image("menu-city", "res/menu/menu-city.png", False)
    ImageUtil.create_image("menu-build-road", "res/menu/menu-build-road.png", False)
    ImageUtil.create_image("menu-company", "res/menu/menu-company.png", False)
    ImageUtil.create_image("menu-build-landfill", "res/menu/menu-landfill.png", False)
    ImageUtil.create_image("menu-trucks", "res/menu/menu-truck.png", False)
    
    



def render(screen):
    global icons
    for i in icons:
        if(i != None):
            screen.blit(ImageUtil.get_image(i[0]), (i[2][0], i[2][1]))
            if(i[4] == True):
                if(i[5] == True):
                    rect = pygame.Surface((UI_ICON_SIZE,UI_ICON_SIZE))
                    rect.set_alpha(100)
                    rect.fill((0,0,0))
                    screen.blit(rect, (i[2][0], i[2][1]))



def mouseClick(x,y):
    for i in icons:
        if(x > i[2][0] and x < i[2][0] + UI_ICON_SIZE):
            if(y > i[2][1] and y < i[2][1] + UI_ICON_SIZE):
                if(i[4] == True):
                    i[5] = not i[5]

                if(i[3] == openMenu or i[3] == setBuildMode):
                    i[3](i[6])
                    return True

                i[3]()
                return True
    return False



def setBuildMode(modeID):
    if(modeID == Map.buildMode):
        Map.buildMode = 0
        Build.buildMode = 0
    else:
        Map.buildMode = modeID
        Build.buildMode = modeID


def openMenu(index):
    if(index == 2):
        None