import Map
from Constants import *
import random
#city generated tiles prefixed with 2
#x and y of selected tile
global seltilei
global seltileX
global seltileY
surTiles = [None] * 100
def getSurroundingtiles(X,Y):
        surTiles = [None] * 100
        #North
        surTiles[0]  = X+1
        surTiles[1]  = Y
        surTiles[2]  = Map.GMAP[surTiles[0]][surTiles[1]]
        #East
        surTiles[10] = X
        surTiles[11] = Y+1
        surTiles[12]  = Map.GMAP[surTiles[10]][surTiles[11]]
        #South
        surTiles[20] = X-1
        surTiles[21] = Y
        surTiles[22]  = Map.GMAP[surTiles[20]][surTiles[21]]
        #West
        surTiles[30] = X
        surTiles[31] = Y-1
        surTiles[32]  = Map.GMAP[surTiles[30]][surTiles[31]]
        return surTiles
def maptest():
    btilesX = []
    btilesY = []
    #x and y of all tiles surrounding selected built tile  
    surtilesX = []
    surtilesY = []
    surtilesV = []
    surtiles = [None] * 100
    surtilesInvalid = 0
    #find all built tiles and put into an array
    for cellY in range(0,MAP_HEIGHT+1):
        for cellX in range(0,MAP_WIDTH+1):
            if(Map.GMAP[cellX][cellY] == "0"):
                btilesX.append(cellX)
                btilesY.append(cellY)

    #randomly pick a tile from array
    seltilei = random.randint(0, len(btilesX)-1)
    seltileX = btilesX[seltilei]
    seltileY = btilesY[seltilei]
    #add surrounding 4 tiles to list
    surtiles = getSurroundingtiles(seltileX,seltileY)
    ##print("Selected tile:" + str(seltileX) + "," + str(seltileY))
    ##print(" 1:" + str(surtiles[2]) + " 2:" + str(surtiles[12]) +" 3:" + str(surtiles[22]) +" 4:" + str(surtiles[32]))
    #check if all the surrounding tiles are currently built on and if they are set the selected tile to 00
    for i in range(0,3):
        if(surtiles[i*10+2] == "0" or surtiles[i*10+2] == "00" or surtiles[i*10+2] == "99"):
            surtilesInvalid+=1
    if(surtilesInvalid==3):
        Map.GMAP[seltileX][seltileY] = "00"
    else:
        newtile = random.randint(0, 3)
        newtileX = newtile*10+0
        newtileY = newtile*10+1
        if(surtiles[newtile*10+2] != "00" and surtiles[newtile*10+2] !="0" and surtiles[newtile*10+2] !="99"):
            if(Map.MAP[surtiles[newtileX]][surtiles[newtileY]] == "1"):
                Map.MAP[surtiles[newtileX]][surtiles[newtileY]] = "10"
                Map.GMAP[surtiles[newtileX]][surtiles[newtileY]] = "0"
            elif(Map.MAP[surtiles[newtileX]][surtiles[newtileY]] == "2"):
                Map.MAP[surtiles[newtileX]][surtiles[newtileY]] = "2"
                Map.GMAP[surtiles[newtileX]][surtiles[newtileY]] = "0"
            else:
                Map.MAP[surtiles[newtileX]][surtiles[newtileY]] = "3"
                Map.GMAP[surtiles[newtileX]][surtiles[newtileY]] = "0"
    surtilesInvalid = 0
    #put all tiles avalible to be built on into array

    #if len(array) == 0
    #set selected tile in GMAP = 00
    #else
    #select random tile from valid tile array
    #set tile to 0 in gmap and 3 in MAP

    #roll dice to determine which of free tiles to build on dice roll weighted to favor higher priority squares
    #create array of all the free tiles add 5x 4x 3x 2x 1x as many values to the array depentant on priority
    #random.choice(array)