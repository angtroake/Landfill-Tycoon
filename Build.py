import Map
from Constants import *
import Company

buildMode = 0

buildStart = [None, None]


def onMouseClick(x,y):
    global buildStart
    

    pos = mousePosToCoord(x,y)

    if buildMode == BUILD_MODE_ROAD:
        initRoadBuild(pos)
    elif buildMode == BUILD_MODE_LANDFILL:
        initLandfillBuild(pos)
        


def onMouseRelease(x,y):
    global buildStart
    mapInstance = Map.MAP
    pos = mousePosToCoord(x,y)

    if(buildMode == BUILD_MODE_ROAD):
        handleBuildRoad(pos)
    elif(buildMode == BUILD_MODE_LANDFILL):
        handleBuildLandfill(pos)



def onMouseRightClick(x,y):
    mapInstance = Map.MAP
    Zoom = Map.Zoom
    scrollX = Map.scrollX
    scrollY = Map.scrollY

    mouseY = int(((x+Map.scrollY)/TILE_HEIGHT) + ((x+Map.scrollX) / TILE_WIDTH))/TILE_WIDTH
    mouseX = -int((-(y+Map.scrollX)/TILE_WIDTH) + ((y+Map.scrollY) / TILE_HEIGHT))/TILE_HEIGHT

    hoverPosX = ((mouseX * TILE_WIDTH*Zoom / 2) + (mouseY * TILE_WIDTH*Zoom / 2) - scrollX)*Zoom
    hoverPosY = ((mouseY * TILE_HEIGHT*Zoom / 2) - (mouseX * TILE_HEIGHT*Zoom / 2) - scrollY)*Zoom



def mousePosToCoord(x,y):
    Zoom = Map.Zoom
    scrollX = Map.scrollX
    scrollY = Map.scrollY

    mouseY = int(((y+scrollY)/TILE_HEIGHT) + ((x+scrollX) / TILE_WIDTH))
    mouseX = -int((-(x+scrollX)/TILE_WIDTH) + ((y+scrollY) / TILE_HEIGHT))

    hoverPosX = ((mouseX * TILE_WIDTH*Zoom / 2) + (mouseY * TILE_WIDTH*Zoom / 2) - scrollX)*Zoom
    hoverPosY = ((mouseY * TILE_HEIGHT*Zoom / 2) - (mouseX * TILE_HEIGHT*Zoom / 2) - scrollY)*Zoom

    x2d = ((hoverPosX+scrollX)-2*(hoverPosY+scrollY))/TILE_WIDTH
    y2d = ((hoverPosY+scrollY)/TILE_HEIGHT + (hoverPosX+scrollX)/TILE_WIDTH)
    return (int(x2d), int(y2d))





#---------------------------------------- ROAD METHODS -----------------------------------------------------------------

def initRoadBuild(pos):
    mapInstance = Map.MAP
    global buildStart
    if(pos[0] >= 0 and pos[0] <= MAP_WIDTH and pos[1] >= 0 and pos[1] <= MAP_HEIGHT):
        buildStart = [pos[0], pos[1]]



def handleBuildRoad(pos):
    mapInstance = Map.MAP
    global buildStart
    if(buildStart[0] != None):
        roadwidth = pos[0]- buildStart[0]
        roadheight = pos[1] - buildStart[1]
        totalRoad = roadwidth * roadheight


        if(totalRoad*COST_OF_ROAD <= Company.Money ):
            if(roadheight == 0 or roadwidth == 0):
                
                for x in range(min(buildStart[0], buildStart[0]+roadwidth), max(buildStart[0]+1, buildStart[0]+roadwidth+1)):
                    for y in range(min(buildStart[1], buildStart[1]+roadheight),max(buildStart[1]+1, buildStart[1]+roadheight+1)):
                        if(mapInstance[x][y] in VALID_CONSTRUCTION_SPOTS):
                            mapInstance[x][y] = Map.TILES["user-road"]
                            Company.Money -= COST_OF_ROAD
        buildStart[0] = None
        buildStart[1] = None

#---------------------------------------- LANDFILL METHODS -----------------------------------------------------------------


def initLandfillBuild(pos):
    mapInstance = Map.MAP
    global buildStart
    if(pos[0] >= 0 and pos[0] <= MAP_WIDTH and pos[1] >= 0 and pos[1] <= MAP_HEIGHT):
        buildStart = [pos[0], pos[1]]

def handleBuildLandfill(pos):
    mapInstance = Map.MAP
    global buildStart
    if(buildStart[0] != None):
        landfillwidth = pos[0]- buildStart[0]
        landfillheight = pos[1] - buildStart[1]
        landfillArea = landfillwidth*landfillheight

        canBuild = True
        ListBlocks = []

        if(landfillArea*COST_OF_LANDFILL <= Company.Money):
            if(landfillwidth >= 3 and landfillwidth >= 3):
                for x in range(min(buildStart[0], buildStart[0]+landfillwidth), max(buildStart[0]+1, buildStart[0]+landfillwidth+1)):
                    for y in range(min(buildStart[1], buildStart[1]+landfillheight),max(buildStart[1]+1, buildStart[1]+landfillheight+1)):
                        if(mapInstance[x][y] not in VALID_CONSTRUCTION_SPOTS):
                            canBuild = False
                            break
                        else:
                            ListBlocks.append((x,y))
        if canBuild:            
            for block in ListBlocks:
                mapInstance[block[0]][block[1]] = Map.TILES["landfill"]
            Company.Money -= landfillArea*COST_OF_LANDFILL




