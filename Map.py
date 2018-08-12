from collections import namedtuple
import csv
from Constants import *
import pygame
import ImageUtil
import json
import copy

scrollX = 0
scrollY = 0

Zoom = 1

font = None

MAP = None
PATHMAP = None

TileData = None
TILES = {}

buildMode = 0

testTruckEnd = [None, None]


pollution = 0

def loadMap():
    with open("maps/map1/Map.csv") as csvmap:
        reader = csv.reader(csvmap)
        global MAP
        MAP = list(reader)
        MAP[0][0] = '0'
    


def loadGMap():
    with open("maps/map1/growth.csv") as csvmap:
        reader = csv.reader(csvmap)
        global GMAP
        GMAP = list(reader)
        GMAP[0][0] = '99'


def loadPathFindingMap():
    global PATHMAP
    global MAP    
    PATHMAP = copy.deepcopy(MAP)

    for x in range(0, len(PATHMAP)):
        for y in range(0, len(PATHMAP)):
            if(PATHMAP[x][y] == '20'):
                PATHMAP[x][y] = '1'
            else:
                PATHMAP[x][y] = '0'
            
    print(PATHMAP)



def loadTileData():
    global TileData
    global TILES
    with open("maps/tile.json") as jsonFile:
        TileData = json.load(jsonFile)
        for tile in TileData:
            TILES[TileData[tile]["name"]] = str(TileData[tile]["id"])
        


def getTileImage(x,y):
    global MAP
    global TileData
    val = MAP[x][y]
    if(val in TileData):
        return ImageUtil.get_image(TileData[val]["image-name"])
    else:
        return ImageUtil.get_image("temp")


def getScreenPositionOfCoord(x,y):
    global Zoom
    global scrollX
    global scrollY

    posX = ((x * TILE_WIDTH / 2) + (y * TILE_WIDTH / 2) - scrollX)*Zoom
    posY = ((y * TILE_HEIGHT / 2) - (x * TILE_HEIGHT / 2) - scrollY)*Zoom

    return((posX,posY))


def mousePosToCoord(x,y):
    global Zoom
    global scrollX
    global scrollY

    mouseY = int(((y+scrollY)/TILE_HEIGHT) + ((x+scrollX) / TILE_WIDTH))
    mouseX = -int((-(x+scrollX)/TILE_WIDTH) + ((y+scrollY) / TILE_HEIGHT))

    hoverPosX = ((mouseX * TILE_WIDTH*Zoom / 2) + (mouseY * TILE_WIDTH*Zoom / 2) - scrollX)*Zoom
    hoverPosY = ((mouseY * TILE_HEIGHT*Zoom / 2) - (mouseX * TILE_HEIGHT*Zoom / 2) - scrollY)*Zoom

    x2d = ((hoverPosX+scrollX)-2*(hoverPosY+scrollY))/TILE_WIDTH
    y2d = ((hoverPosY+scrollY)/TILE_HEIGHT + (hoverPosX+scrollX)/TILE_WIDTH)
    return [int(x2d), int(y2d)]



def render(screen):
    global scrollX
    global scrollY
    global Zoom
    global buildMode
    global font

    if(font == None):
        font = pygame.font.Font(None, 30)
    #font = pygame.font.Font(None, 30)
    #--------------------------------  TILE RENDERING   -------------------------------------

    for cellY in range(0,MAP_HEIGHT+1):
        for cellX in range(0,MAP_WIDTH+1):
            cellX = MAP_WIDTH-cellX
            posX = ((cellX * TILE_WIDTH / 2) + (cellY * TILE_WIDTH / 2) - scrollX)*Zoom
            posY = ((cellY * TILE_HEIGHT / 2) - (cellX * TILE_HEIGHT / 2) - scrollY)*Zoom

            if(posX  > -80 and posX < screen.get_width() + 50 and posY > -50 and posY < screen.get_height() + 50):
                color = (100,100,100)
                image = getTileImage(cellX, cellY)
                #renders tile to screen
                if(testTruckEnd[0] == None):
                    if(cellX == testTruckEnd[0] and cellY == testTruckEnd[1]):
                        image = ImageUtil.get_image("temp")

                if(image.get_height()!=TILE_HEIGHT):
                    screen.blit(pygame.transform.scale(image, (int(TILE_WIDTH*Zoom), int(image.get_height()*Zoom))), (posX, (posY-image.get_height()+TILE_HEIGHT/2)*Zoom))
                else:
                    screen.blit(pygame.transform.scale(image, (int(TILE_WIDTH*Zoom), int(TILE_HEIGHT*Zoom))), (posX, posY-TILE_HEIGHT*Zoom/2))
                #render build priority
                #bupr = font.render(str(GMAP[cellX][cellY]), True, (0, 0, 0))
                #screen.blit(bupr, (posX-16,posY-16))
                
                #if in build mode enables the grid
                if(buildMode != 0):
                    pygame.draw.line(screen, color, (posX,posY), (posX + TILE_WIDTH*Zoom/2, posY - TILE_HEIGHT*Zoom/2))
                    pygame.draw.line(screen, color, (posX+TILE_WIDTH*Zoom/2, posY-TILE_HEIGHT*Zoom/2), (posX+TILE_WIDTH*Zoom,posY))
                    pygame.draw.line(screen, color, (posX+TILE_WIDTH*Zoom,posY), (posX+TILE_WIDTH*Zoom/2,posY+TILE_HEIGHT*Zoom/2))
                    pygame.draw.line(screen, color, (posX+TILE_WIDTH*Zoom/2,posY+TILE_HEIGHT*Zoom/2),(posX,posY))

    #-------------------------------------------------------------------------------------------



    #------------------------- MOUSE TILE HOVER ------------------------------------------------

    mousePos = pygame.mouse.get_pos()

    mouseY = int(((mousePos[1]+scrollY)/TILE_HEIGHT) + ((mousePos[0]+scrollX) / TILE_WIDTH))
    mouseX = -int((-(mousePos[0]+scrollX)/TILE_WIDTH) + ((mousePos[1]+scrollY) / TILE_HEIGHT))

    hoverPosX = ((mouseX * TILE_WIDTH*Zoom / 2) + (mouseY * TILE_WIDTH*Zoom / 2) - scrollX)*Zoom
    hoverPosY = ((mouseY * TILE_HEIGHT*Zoom / 2) - (mouseX * TILE_HEIGHT*Zoom / 2) - scrollY)*Zoom

    if(buildMode != 0):
        pygame.draw.line(screen, (0,0,255), (hoverPosX,hoverPosY), (hoverPosX + TILE_WIDTH*Zoom/2, hoverPosY - TILE_HEIGHT*Zoom/2))
        pygame.draw.line(screen, (0,0,255), (hoverPosX+TILE_WIDTH*Zoom/2, hoverPosY-TILE_HEIGHT*Zoom/2), (hoverPosX+TILE_WIDTH*Zoom,hoverPosY))
        pygame.draw.line(screen, (0,0,255), (hoverPosX+TILE_WIDTH*Zoom,hoverPosY), (hoverPosX+TILE_WIDTH*Zoom/2,hoverPosY+TILE_HEIGHT*Zoom/2))
        pygame.draw.line(screen, (0,0,255), (hoverPosX+TILE_WIDTH*Zoom/2,hoverPosY+TILE_HEIGHT*Zoom/2),(hoverPosX,hoverPosY))

        mouseCoord = mousePosToCoord(hoverPosX, hoverPosY)
        textpos = font.render("X:" + str(mouseCoord[0]) + "  Y:" + str(mouseCoord[1]), True, (0, 0, 0))
        screen.blit(textpos, (50,200))

    #---------------------------------------------------------------------------------------------

#TODO Adjust render limit when testing finished
#TODO FIX CURSOR ON ZOOM     

