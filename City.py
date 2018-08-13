import Map
from Constants import *
import random
import datetime

gmapLeft = {}



AmoutOfTrash = 0
Population = 1000

#POPULATION * FERTILEAMOUNT(8.2)(constant) / 100
BirthRate = None

#POPULATION * POLUTION / 100 / 9(constant)
DeathRate = None
PopChangePerSecond = None

LastPopChange = None

LastPopMilestone = 1000

GrowthPossible = True


#city generated tiles prefixed with 2
#x and y of selected tile
global seltilei
global seltileX
global seltileY
surTiles = [None] * 100




def init():
    global gmapLeft
    GMAP = Map.GMAP
    for x in range(0, len(GMAP)):
        for y in range(0, len(GMAP)):
            if(Map.getTile(x,y) == Map.TILES["grass"] or Map.getTile(x,y) == Map.TILES["road-to-be"]):
                val = GMAP[x][y]
                if(val in gmapLeft):
                    gmapLeft[val].append((x,y))
                else:
                    gmapLeft[val] = [(x,y)]
    
    print("0: " + str(len(gmapLeft['0'])))
    print("1: " + str(len(gmapLeft['1'])))
    print("2: " + str(len(gmapLeft['2'])))
    print("3: " + str(len(gmapLeft['3'])))
    print("4: " + str(len(gmapLeft['4'])))
    print("5: " + str(len(gmapLeft['5'])))
            



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

def doesSurroundHaveRoad(x, y):
    for x1 in range(x-1, x+3):
        for y1 in range(y-1, y+3):
            if(x1 is not x and y1 is not y):
                tile = Map.getTile(x1,y1)
                if(tile == Map.TILES["user-road"] or tile == Map.TILES["road"]):
                    return True

    return False


def maptest2():
    global gmapLeft
    GMAP = Map.GMAP
    MAP = Map.MAP

    gmapVal = 99

    for i in range(0,6):
        if(len(gmapLeft[str('0')]) > 0):
            gmapVal = str(i)
            break

    if(gmapVal != 99):
        tilesLeft = gmapLeft[gmapVal]

        print(gmapVal + ": " + str(len(gmapLeft[gmapVal])))

        tileSelected = (0,0)
        isgood = False

        whilei = 0
        while(isgood == False):
            #print("While: " + str(whilei))
            whilei += 1
            if(whilei >= 100):
                if(int(gmapVal) < 5):
                    gi = int(gmapVal) + 1
                    gmapVal = str(gi)
                    tilesLeft = gmapLeft[gmapVal]
                    
                    whilei = 0
                    print("trying: " + str(gi))
                else:
                    None
                    #return False
            tileSelected = random.choice(tilesLeft)
            #print(tileSelected)
            tileSelectedVal = Map.getTile(tileSelected[0], tileSelected[1])
            if(tileSelectedVal == Map.TILES["grass"] or tileSelectedVal == Map.TILES["road-to-be"]):
                #if(doesSurroundHaveRoad(tileSelected[0], tileSelected[1])):
                    isgood = True
        

        currentMapValue = Map.getTile(tileSelected[0], tileSelected[1])
        newValue = None
        if(currentMapValue == Map.TILES["road-to-be"]):
            newValue = Map.TILES["road"]
        elif(currentMapValue == Map.TILES["grass"]):
            newValue = str(random.randint(0,2) + 10)
        else:
            return False
        
        Map.setTile(tileSelected[0], tileSelected[1], newValue)
        tilesLeft.remove(tileSelected)





        


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

    #print("Selected tile:" + str(seltileX) + "," + str(seltileY))
    #print(" 1:" + str(surtiles[2]) + " 2:" + str(surtiles[12]) +" 3:" + str(surtiles[22]) +" 4:" + str(surtiles[32]))
    #check if all the surrounding tiles are currently built on and if they are set the selected tile to 00
    for i in range(0,3):
        if(surtiles[i*10+2] == "0" or surtiles[i*10+2] == "00" or surtiles[i*10+2] == "99"):
            surtilesInvalid+=1
    if(surtilesInvalid==3):
        Map.GMAP[seltileX][seltileY] = "00"
        return False
    else:
        newtile = random.randint(0, 3)
        newtileX = newtile*10+0
        newtileY = newtile*10+1
        if(surtiles[newtile*10+2] != "00" and surtiles[newtile*10+2] !="0" and surtiles[newtile*10+2] !="99"):
            if(Map.MAP[surtiles[newtileX]][surtiles[newtileY]] == "1"):
                Map.MAP[surtiles[newtileX]][surtiles[newtileY]] = str(random.randint(0,2) + 10)
                Map.GMAP[surtiles[newtileX]][surtiles[newtileY]] = "0"
            elif(Map.MAP[surtiles[newtileX]][surtiles[newtileY]] == "2"):
                Map.MAP[surtiles[newtileX]][surtiles[newtileY]] = "20"
                Map.GMAP[surtiles[newtileX]][surtiles[newtileY]] = "0"
            else:
                Map.MAP[surtiles[newtileX]][surtiles[newtileY]] = "3"
                Map.GMAP[surtiles[newtileX]][surtiles[newtileY]] = "0"
    surtilesInvalid = 0
    return True
    #put all tiles avalible to be built on into array

    #if len(array) == 0
    #set selected tile in GMAP = 00
    #else
    #select random tile from valid tile array
    #set tile to 0 in gmap and 3 in MAP

    #roll dice to determine which of free tiles to build on dice roll weighted to favor higher priority squares
    #create array of all the free tiles add 5x 4x 3x 2x 1x as many values to the array depentant on priority
    #random.choice(array)



"""
function ran every game tick (game logic loop)
"""
def tick():
    global LastPopChange
    global Population
    global PopChangePerSecond
    global LastPopMilestone
    global GrowthPossible
    global AmoutOfTrash

    if(LastPopChange == None):
        LastPopChange = datetime.datetime.now()
    
    RefreshPopulationRates()
    
    currentTime = datetime.datetime.now()
    if((currentTime - LastPopChange).total_seconds() >= SECONDS_BETWEEN_GROWTH):
        AmoutOfTrash = AmoutOfTrash + (Population * RATE_OF_TRASH/5000)
        Population += PopChangePerSecond
        LastPopChange = currentTime
        if(Population > LastPopMilestone + 100):
            LastPopMilestone += 100
            #print("new building")
            while(not maptest()):
                None
            #b = maptest2()



def RefreshPopulationRates():
    global BirthRate
    global DeathRate
    global Population
    global POLUTION
    global PopChangePerSecond

    BirthRate = Population * FERTILE_CONSTANT / 100
    DeathRate = Population * Map.Pollution / 100 / DEATH_CONSTANT

    PopChangePerSecond = (BirthRate - DeathRate)/20

