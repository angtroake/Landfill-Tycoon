import Map
from Constants import *
import random
#x and y of selected tile
global seltilei
global seltileX
global seltileY

def maptest():
    btilesX = []
    btilesY = []
    #x and y of all tiles surrounding selected built tile  
    surtilesX = []
    surtilesY = []
    surtilesV = []
    #find all built tiles and put into an array
    for cellY in range(0,MAP_HEIGHT+1):
        for cellX in range(0,MAP_WIDTH+1):
            if(Map.GMAP[cellX][cellY] == "0"):
                btilesX.append(cellX)
                btilesY.append(cellY)

    #randomly pick a tile from array
    seltilei = random.randint(0, len(btilesX))
    seltileX = btilesX[seltilei]
    seltileY = btilesY[seltilei]
    #add surrounding 8 tiles to list
    #north
    surtilesX.append(seltileX)
    surtilesY.append(seltileY + 1)
    surtilesV.append(Map.GMAP[surtilesX[0]][surtilesY[0]])
    #east
    surtilesX.append(seltileX + 1)
    surtilesY.append(seltileY) 
    surtilesV.append(Map.GMAP[surtilesX[1]][surtilesY[1]])
    #south
    surtilesX.append(seltileX)
    surtilesY.append(seltileY - 1)
    surtilesV.append(Map.GMAP[surtilesX[2]][surtilesY[2]])
    #west
    surtilesX.append(seltileX -1)
    surtilesY.append(seltileY)
    surtilesV.append(Map.GMAP[surtilesX[3]][surtilesY[3]])

    print("Selected tile:" + str(seltileX) + "," + str(seltileY))
    #roll dice to determine which of free tiles to build on dice roll weighted to favor higher priority squares
    #create array of all the free tiles add 5x 4x 3x 2x 1x as many values to the array depentant on priority
    #random.choice(array)