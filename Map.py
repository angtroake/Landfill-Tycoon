from collections import namedtuple
import csv
from Constants import *
import pygame
import ImageUtil
import json
import copy
import PathFinding
from scipy import ndimage
import numpy as np
from skimage import measure
import datetime

scrollX = 0
scrollY = 0

Zoom = 1

font = None

MAP = None
PATHMAP = None
GMAP = None

ORIGINAL_MAP = None
ORIGINAL_GMAP = None

#DICT    {[x,y]: groupid}
LandfillTiles = {}

#                       0          1               2               3            4
#DICT        {id: [amountfill, maxamount, (centerX, centerY), #incinerators, #recycle]}
Landfillgroups = {}

LandfillAdded = False

TileData = None
#          name: id
TILES = {}
TILEOBJECTS = {}    # DICT    id: [cost-to-delete]

buildMode = 0


Pollution = 0

def loadMap():
    with open("maps/map1/Map.csv") as csvmap:
        reader = csv.reader(csvmap)
        global MAP
        global ORIGINAL_MAP
        MAP = list(reader)
        MAP[0][0] = '0'
        ORIGINAL_MAP = copy.deepcopy(MAP)
    


def loadGMap():
    with open("maps/map1/growth.csv") as csvmap:
        reader = csv.reader(csvmap)
        global GMAP
        global ORIGINAL_GMAP
        GMAP = list(reader)
        GMAP[0][0] = '99'
        ORIGINAL_GMAP = copy.deepcopy(GMAP)


def loadPathFindingMap():
    global PATHMAP
    global MAP    
    PATHMAP = copy.deepcopy(MAP)
    finalMap = copy.deepcopy(MAP)

    for x in range(0, len(PATHMAP)):
        for y in range(0, len(PATHMAP)):
            if(PATHMAP[x][y] == '20'):
                PATHMAP[x][y] = '1'
                finalMap[y][x] = '1'
            else:
                PATHMAP[x][y] = '0'
                finalMap[y][x] = '0'

    PATHMAP = finalMap
            



def loadTileData():
    global TileData
    global TILES
    global TILEOBJECTS
    with open("maps/tile.json") as jsonFile:
        TileData = json.load(jsonFile)
        for tile in TileData:
            TILES[TileData[tile]["name"]] = str(TileData[tile]["id"])
            TILEOBJECTS[str(TileData[tile]["id"])] = [TileData[tile]["cost-to-delete"]]
        


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

    return([posX,posY])


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



def setTile(x, y, tileId):
    global MAP
    global PATHMAP
    global LandfillTiles
    global LandfillAdded
    MAP[x][y] = str(tileId)
    if(str(tileId) == '20' or str(tileId) == '22'):
        PATHMAP[y][x] = '1'
    elif(str(tileId) == '23'):
        LandfillTiles[(x,y)] = None
        LandfillAdded = True
        PATHMAP[y][x] = '2'
    else:
        PATHMAP[y][x] = '0'

def getTile(x, y):
    global MAP
    return MAP[x][y]



def isHouseTile(x,y, original = False):
    global ORIGINAL_MAP
    if(original == False):
        tile = getTile(x,y)
    else:
        tile = ORIGINAL_MAP[x][y]
        
    if(int(tile) >= 10 and int(tile) <= 19):
        return True
    return False



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

                if(image.get_height()!=TILE_HEIGHT):
                    
                    screen.blit(pygame.transform.scale(image, (int(TILE_WIDTH*Zoom), int(image.get_height()*Zoom))), (posX, (posY-image.get_height()+TILE_HEIGHT/2)*Zoom))
                else:
                    screen.blit(pygame.transform.scale(image, (int(TILE_WIDTH*Zoom), int(TILE_HEIGHT*Zoom))), (posX, posY-TILE_HEIGHT*Zoom/2))


                #render build priority
                #bupr = font.render(str(GMAP[cellX][cellY]), True, (0, 0, 0))
                #screen.blit(bupr, (posX+32,posY-16))
                
                #if in build mode enables the grid
                if(buildMode != 0):
                    pygame.draw.line(screen, color, (posX,posY), (posX + TILE_WIDTH*Zoom/2, posY - TILE_HEIGHT*Zoom/2))
                    pygame.draw.line(screen, color, (posX+TILE_WIDTH*Zoom/2, posY-TILE_HEIGHT*Zoom/2), (posX+TILE_WIDTH*Zoom,posY))
                    pygame.draw.line(screen, color, (posX+TILE_WIDTH*Zoom,posY), (posX+TILE_WIDTH*Zoom/2,posY+TILE_HEIGHT*Zoom/2))
                    pygame.draw.line(screen, color, (posX+TILE_WIDTH*Zoom/2,posY+TILE_HEIGHT*Zoom/2),(posX,posY))
                

                #render vehicle on tile if there is one
                vehicle = PathFinding.tileHasVehicle(cellX, cellY)
                if(vehicle != False):
                    PathFinding.renderVehicle(vehicle, screen)



    #-------- MOUSE TILE HOVER ----

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
        screen.blit(textpos, (5,70))
    

    #RENDER TEXT FOR LANDFILLS
    for Landfill in Landfillgroups:
        pos = getScreenPositionOfCoord(Landfillgroups[Landfill][2][0], Landfillgroups[Landfill][2][1])
        textLandfill = font.render("Landfill", True, (255,255,255))
        textAmountFill = font.render(str(Landfillgroups[Landfill][0]) + "/" + str(Landfillgroups[Landfill][1]), True, (255,255,255))
        screen.blit(textLandfill, (pos[0], pos[1]-40))
        screen.blit(textAmountFill, (pos[0], pos[1]))

    


    #-----------------------------------------               END      RENDER           ----------------------------------------------------


lastLandfillTick = None


def tick():
    global LandfillTiles
    global Landfillgroups
    global LandfillAdded
    global lastLandfillTick
    if(LandfillAdded):
        print("Land FIll Added")
        landfillLogic2()
        LandfillAdded = False
    
    currentTime = datetime.datetime.now()
    if(lastLandfillTick == None):
        lastLandfillTick = currentTime
        return

    for g in Landfillgroups:
        group = Landfillgroups[g]
        if((currentTime - lastLandfillTick).total_seconds() >= LANDFILL_TICK_SECONDS):
            if(group[0] >= group[4]*RECYCLE_REMOVE_AMOUNT):
                group[0] -=  group[4]*RECYCLE_REMOVE_AMOUNT
            else:
                group[0] = 0
            
            if(group[0] >= group[3]*FIRE_REMOVE_AMOUNT):
                group[0] -= group[3]*FIRE_REMOVE_AMOUNT
            else:
                group[0] = 0
    
    if((currentTime - lastLandfillTick).total_seconds() >= LANDFILL_TICK_SECONDS):
        lastLandfillTick = currentTime

    



#DICT   LandfillTiles    {[x,y]: groupid}
#DICT        {id: [amountfill, maxamount, (centerX, centerY)]}


def landfillLogic2():
    global MAP
    global LandfillTiles
    global Landfillgroups

    tempMap = copy.deepcopy(MAP)
    for x in range(0, MAP_WIDTH):
        for y in range(0, MAP_HEIGHT):
            if tempMap[x][y] != '23':
                tempMap[x][y] = '0'

    array = np.array(tempMap)
    img_labled = measure.label(array, connectivity=1)

    idx = [np.where(img_labled == label) for label in np.unique(img_labled) if label]


    groups = []
    newgroup = []

    for lols in idx:
        for i in range(0, len(lols[0])):
            newgroup.append((lols[0][i], lols[1][i]))
        groups.append(newgroup)
        newgroup = []
    
    
    for group in groups:
        groupid = None
        minX = None
        minY = None
        maxX = None
        maxY = None
        for tile in group:
            if(LandfillTiles[tile] != None):
                groupid = LandfillTiles[tile]
                break
        minX = group[0][0]
        minY = group[0][1]
        maxX = group[len(group)-1][0]
        maxY = group[len(group)-1][1]
        
        if(groupid != None):
            for tile in group:
                LandfillTiles[tile] = groupid
            Landfillgroups[groupid][1] = len(group)*GARBAGE_PER_LANDFILL_TILE
            Landfillgroups[groupid][2] = (minX + (maxX-minX)/2, minY + (maxY-minY)/2)
            
        else:
            groupid = len(Landfillgroups)
            for tile in group:
                LandfillTiles[tile] = groupid
            Landfillgroups[groupid] = [0,len(group)*GARBAGE_PER_LANDFILL_TILE, (minX + (maxX-minX)/2, minY + (maxY-minY)/2), 0, 0]

            

