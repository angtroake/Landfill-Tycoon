import Map
from Constants import *
import random
#all built tiles
btx = []
bty = []
#surrounding tiles
surTilesX = []
surTilesY = []
surTilesV = []
def getBuiltTiles():
    global btx
    global bty
    btx.clear()
    bty.clear()
    i = 0
    #find all tiles where value = 20, 10, 11, 12 and gmap value != 00
    for cellY in range(0,MAP_HEIGHT+1):
        for cellX in range(0,MAP_WIDTH+1):
            if(int(Map.MAP[cellX][cellY]) >= 10 and int(Map.MAP[cellX][cellY]) <= 20 and Map.GMAP[cellX][cellY] != "00"):#and int(Map.MAP[cellX][cellY]) <= 20
                btx.append(cellX)
                bty.append(cellY)
    #print(str(bt[0*2+0]) + " " + str(bt[0*2+1]))
    return
def getSurroundingtiles(X,Y):
    global surTilesX
    global surTilesY
    global surTilesV
    surTilesX.clear()
    surTilesY.clear()
    surTilesV.clear()
    #returns tiles x,y and value north east south and west of x,y    #North
    surTilesX.append(X+1)
    surTilesY.append(Y)
    surTilesV.append(Map.MAP[surTilesX[0]][surTilesY[0]])
    #East
    surTilesX.append(X)
    surTilesY.append(Y+1)
    surTilesV.append(Map.MAP[surTilesX[1]][surTilesY[1]])
    #South
    surTilesX.append(X-1)
    surTilesY.append(Y)
    surTilesV.append(Map.MAP[surTilesX[2]][surTilesY[2]])
    #West
    surTilesX.append(X)
    surTilesY.append(Y-1)
    surTilesV.append(Map.MAP[surTilesX[3]][surTilesY[3]])
    return

def isadjacenttoroad(x,y):
    #returns true if a road is north east south or west of x,y
    getSurroundingtiles(x,y)
    for x in range(0,3):
        if(surTilesV[x] == "20"):
            return True
    return False

def istilegrowable(x,y):
    #returns true if tile can be grown
    if(not(Map.MAP[x][y] <= "20" and Map.MAP[x][y] >= "10")):
        return True
    return False

def growtile(x,y):
    print("growing tile" + str(x) + str(y))
    TileValue = Map.MAP[x][y]
    if(TileValue == "2"):
        Map.MAP[x][y] = "20"
    elif(TileValue == "1"):
        Map.MAP[x][y] = "10"

def grow():
    global btx
    global bty
    growableTilesX = []
    growableTilesY = []
    x = 0
    y = 0
    getBuiltTiles()
    #randomly select a tile from bTiles
    #print(len(btx))
    x = random.randint(0, len(btx)-1)
    print("built block being used to build off of")
    print(str((btx[x], bty[x])))
    getSurroundingtiles(btx[x], bty[x])
    #loop through sTiles
    for x in range(0,4):
        #print("is the square adjacent to a road " + str(isadjacenttoroad(surTilesX[x], surTilesY[x])) + " is the tile growable " + str(istilegrowable(surTilesX[x], surTilesY[x]))
        if( isadjacenttoroad(surTilesX[x], surTilesY[x]) and istilegrowable(surTilesX[x], surTilesY[x]) ):
            growableTilesX.append(surTilesX[x])
            growableTilesY.append(surTilesY[x])
    
    growabletileslen = len(growableTilesX)
    print("total buildable tiles " + str(len(growableTilesX)))
    if(growabletileslen == 0):
        None
    #Map.GMAP[btx[x]][bty[x]] = "00"
    #elif(growabletileslen == 1):
    #    growtile(growableTilesX[0],growableTilesY[0])
    elif(growabletileslen >= 1):
        #generate random int between 0 and growabletileslen-1
        y = random.randint(0, growabletileslen-1)
        growtile(growableTilesX[0],growableTilesY[0])
    
    


    



