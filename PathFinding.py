import pygame
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
import csv
import random
import json
import Map
import ImageUtil
from Constants import *
import City
import Company
import datetime
import Notification



#                                 0                    1          2           3          4        5        6
#    STRUCTURE:     [(currentCordX, currentCoordY), typeID, targetPosNode, Capacity, AmountFill, path, pathindex]
LiveVehicles = []

#                           0       1        2(0=TL,1=TR,2=BR,3=BL)     3         4
#    STRUCTURE:     [id, (name, capacity, images,                     cost, monthly-cost)]
VehicleTypes = {}

finder = AStarFinder()

CurrentTick = 0
MaxTick = 40


LastBillTime = None


def initVehicleTypes():
    global VehicleTypes
    with open("vehicle.json") as jsonFile:
        tempData = json.load(jsonFile)
        for val in tempData:
            images = (tempData[val]["image-name-TL"], tempData[val]["image-name-TR"], tempData[val]["image-name-BR"], tempData[val]["image-name-BL"])
            VehicleTypes[tempData[val]["id"]] = (tempData[val]["name"], tempData[val]["capacity"], images, tempData[val]["cost"], tempData[val]["monthly-cost"])


def createVehicle(id):
    global VehicleTypes
    global LiveVehicles

    startCoords = getNewRoadTarget()
    randomTarget = getNewRoadTarget()

    path = getPath(startCoords, randomTarget)


    vehicle = [(startCoords[0], startCoords[1]), id, randomTarget, VehicleTypes[id][0], 0, path, 0]
    LiveVehicles.append(vehicle)





def tick():
    global LiveVehicles
    global CurrentTick
    global VehicleTypes
    global MaxTick
    global Mon
    global LastBillTime

    TotalMonthlyCost = 0

    if(CurrentTick >= MaxTick):
        for vehicle in LiveVehicles:
            currentpos = vehicle[0]
            path = vehicle[5]
            pathindex = vehicle[6]
            endpos = vehicle[2]
            vehicleType = VehicleTypes[vehicle[1]]
            #print("Current Pos: " + str(currentpos) + "   End Pos: " + str(endpos) + "   Path Length: " + str(len(path)) + "   Path Index: " + str(pathindex))


            TotalMonthlyCost += vehicleType[4]

            #ADD GARBAGE IF NEXT TO HOUSE
            if(vehicle[4] < vehicleType[1]):
                if(Map.isHouseTile(currentpos[0]+1,currentpos[1]) or Map.isHouseTile(currentpos[0]-1, currentpos[1]) or Map.isHouseTile(currentpos[0], currentpos[1]-1) or Map.isHouseTile(currentpos[0], currentpos[1]+1)):
                    #print("HOUSE NEXT TO")
                    rand = random.randint(0, RANDOM_CHANCE_OF_GARBAGE_GET)
                    if(rand == 0 and City.AmoutOfTrash >= 1 ):
                        vehicle[4] += 1
                        Company.Money += 10
                        City.AmoutOfTrash -= 1
                        #print("Trash: " + str(vehicle[4]) + "      CITY TRASH: " + str(City.AmoutOfTrash))


            
                


            #IF IT HAS REACHED THE END OF ITS RANDOM PATH GENERATE A NEW ONE AND DUMP TRASH IF HAS SOME
            if((currentpos[0] == endpos[0] and currentpos[1] == endpos[1]) or endpos[0] == None or len(path) <= 0 or pathindex >= len(path)):
                
                #IF AT LANDFILL
                if(Map.getTile(currentpos[0], currentpos[1]) == Map.TILES["landfill"]):
                    landfill = Map.Landfillgroups[Map.LandfillTiles[(currentpos[0],currentpos[1])]]
                    spaceLeft = landfill[1] - landfill[0]
                    if spaceLeft >= vehicle[4]:
                        landfill[0] += vehicle[4]
                        vehicle[4] = 0
                    else:
                        landfill += spaceLeft
                        vehicle[4] -= spaceLeft

                endpos = None
                path = None
                while(endpos == None and path == None):
                    if(vehicle[4] >= vehicleType[1]):
                        newfill = getNewLandfillTarget()
                        if(newfill == None):
                            vehicle[2] = getNewRoadTarget()
                            #print("NO Landfill")
                            Notification.addNotification("Citizens worry as full garbage trucks roam the city without a landfill to go to!")
                        else:
                            vehicle[2] = newfill
                            #print("yay landfill!")
                    else:
                        vehicle[2] = getNewRoadTarget()
                    startpos = currentpos
                    path = getPath(startpos, vehicle[2])
                    print(path)

                vehicle[5] = path
                vehicle[6] = 0
                Map.testTruckEnd = endpos
                continue


            #SET POSIITON TO NEXT POOSITION IN PATH
            vehicle[0] = [path[pathindex][0], path[pathindex][1]]
            vehicle[6] += 1


        #MONTHLY COSTS
        currentTime = datetime.datetime.now()
        if(LastBillTime == None):
            LastBillTime = currentTime

        if((currentTime - LastBillTime).total_seconds() >= SECONDS_PER_MONTH):
            Company.Money -= TotalMonthlyCost
            LastBillTime = currentTime


        CurrentTick = 0
    else:
        CurrentTick += 1


def render(screen):
    global LiveVehicles
    for vehicle in LiveVehicles:
        renderVehicle(vehicle, screen)



def renderVehicle(vehicle, screen):
    currentpos = vehicle[0]
    images = VehicleTypes[vehicle[1]][2]
    image = ImageUtil.get_image(images[3])
    isoPos = Map.getScreenPositionOfCoord(currentpos[0], currentpos[1])
    if(vehicle[6] < len(vehicle[5])):
        nextpos = vehicle[5][vehicle[6]]
        #pygame.draw.rect(screen, (255,0,0), [isoPos[0]-25, isoPos[1]-25, 50, 50])

        if(nextpos[0] > currentpos[0]):
            image = ImageUtil.get_image(images[1])
        elif(nextpos[0] < currentpos[0]):
            image = ImageUtil.get_image(images[3])
        elif(nextpos[1] > currentpos[1]):
            image = ImageUtil.get_image(images[2])
        elif(nextpos[1] < currentpos[1]):
            image = ImageUtil.get_image(images[0])
        
    isoPos[0] += (TILE_WIDTH/2 - image.get_width()/2)
    isoPos[1] -= image.get_height()/2
    
            
    screen.blit(image, isoPos)


"""
returns vehicle if there is one in that tile
if not it returns false
"""
def tileHasVehicle(x, y):
    global LiveVehicles
    for vehicle in LiveVehicles:
        if(vehicle[0][0] == x and vehicle[0][1] == y):
            return vehicle

    return False





#---------------------------------PATH FINDING FUNCTIONS-------------------------------------



"""
gets the path from start pos to end on PATHMAP. returns a list of positions (AKA move to this pos next)
"""
def getPath(start, end):
    RoadMap = Map.PATHMAP
    global finder

    grid = Grid(matrix = RoadMap)
    start = grid.node(start[0], start[1])
    end = grid.node(end[0], end[1])
    path, runs = finder.find_path(start, end, grid)
    #print(grid.grid_str(path=path, start=start, end=end))

    return path



"""
Returns a random spot on PATHMAP where there is a road
"""
def getNewRoadTarget():
    RoadMap = Map.PATHMAP
    returns = [0,0]
        
    while RoadMap[returns[0]][returns[1]] != '1':
        returns = random.choice([(j,i) for i, row in enumerate(RoadMap) for j, val in enumerate(row) if val=='1'])

    return returns


def getNewLandfillTarget():
    RoadMap = Map.PATHMAP
    returns = [0,0]

    if(any('2' in sub for sub in RoadMap)):
        print("there is a 2")
        returns = random.choice([(j,i) for i, row in enumerate(RoadMap) for j, val in enumerate(row) if val=='2'])
    else:
        return None

    return returns









#--------- OLD CODE USED FOR TESTING
"""
def run():
    matrix = None

    with open("maps/pathfindingtestmap.csv") as csvmap:
        reader = csv.reader(csvmap)
        matrix = list(reader)
    

    grid = Grid(matrix = matrix)
    start = grid.node(1,4)
    end = grid.node(26,13)

    print(len(matrix))

    while(matrix[start.x][start.y] != '1'):
        start = grid.node(random.randint(0, len(matrix[0]))-1, random.randint(0, len(matrix))-1)
        

    finder = AStarFinder()
    path, runs = finder.find_path(start, end, grid)

    print("RUNS: ", runs, "path length: ", len(path))
    print(grid.grid_str(path=path, start=start, end=end))
    print(path[0])
    print(path[1])
"""
