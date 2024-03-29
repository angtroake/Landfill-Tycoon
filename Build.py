import Map
from Constants import *
import Company
import pygame

buildMode = 0

buildStart = [None, None]

blackholepos = (0 , 0)
font = None


def init():
    global font
    font = pygame.font.Font(None, 25)

def onMouseClick(x,y):
    global buildStart
    

    pos = mousePosToCoord(x,y)

    if buildMode == BUILD_MODE_ROAD:
        initRoadBuild(pos)
    elif buildMode == BUILD_MODE_LANDFILL:
        initLandfillBuild(pos)
    elif buildMode == BUILD_MODE_DELETE:
        handleDelete(pos)
    elif buildMode == BUILD_MODE_BLACKHOLE:
        handleBlackhole(pos)

def render(screen):
    global buildStart
    global font

    pos1 = pygame.mouse.get_pos()
    pos = mousePosToCoord(pos1[0], pos1[1])

    if(buildStart[0] != None):
        
        selectorBoxTR = None
        selectorBoxTL = None
        selectorBoxBR = None
        selectorBoxBL = None
    
        if(buildMode == BUILD_MODE_LANDFILL):
            color = (255,255,255)
            if(abs(pos[0]-buildStart[0]) + 1 < 3 and abs(pos[1]-buildStart[1]) +1 < 3):
                color = (255,0,0)
            selectorBoxTL = Map.getScreenPositionOfCoord(min(pos[0], buildStart[0]), min(pos[1], buildStart[1]))
            selectorBoxTR  = Map.getScreenPositionOfCoord(max(pos[0], buildStart[0])+1, min(pos[1], buildStart[1]))
            selectorBoxBR = Map.getScreenPositionOfCoord(max(pos[0], buildStart[0]) +1, max(pos[1], buildStart[1]) + 1)
            selectorBoxBL = Map.getScreenPositionOfCoord(min(pos[0], buildStart[0]), max(pos[1], buildStart[1])+1)
            pygame.draw.line(screen, color, selectorBoxTL, selectorBoxTR)
            pygame.draw.line(screen, color, selectorBoxTR, selectorBoxBR)
            pygame.draw.line(screen, color, selectorBoxBR, selectorBoxBL)
            pygame.draw.line(screen, color, selectorBoxBL, selectorBoxTL)

            area = (abs(pos[0]-buildStart[0])+1) * (abs(pos[1]-buildStart[1])+1)
            color = (255,255,255)
            if(area * COST_OF_LANDFILL > Company.Money):
                color = (255,0,0)

            cost = font.render("-" + str(area*COST_OF_LANDFILL) + "$", True, color)
            screen.blit(cost, (pos1[0], pos1[1] - 10))
        
    elif(buildMode == BUILD_MODE_DELETE):

        color = (255,255,255)
        moneyNeeded = Map.TILEOBJECTS[Map.getTile(pos[0], pos[1])][0]
        if(moneyNeeded != -1):
            if(moneyNeeded > Company.Money):
                color = (255,0,0)

            cost = font.render("-" + str(Map.TILEOBJECTS[Map.getTile(pos[0], pos[1])][0]) + "$", True, color)
            screen.blit(cost, (pos1[0], pos1[1] - 10))
    

    buildingCost = 0
    displaybuilding = False

    if(buildMode == BUILD_MODE_FIRE):
        displaybuilding = True
        buildingCost = COST_OF_BURNER
    elif(buildMode == BUILD_MODE_RECYCLE):
        displaybuilding = True
        buildingCost = COST_OF_RECYCLE
    elif(buildMode == BUILD_MODE_BLACKHOLE):
        displaybuilding = True
        buildingCost = COST_OF_BHOLE
    
        
    if(displaybuilding):
        color = (255,255,255)
        if(landfillNextToPos(pos) and Map.getTile(pos[0], pos[1]) in VALID_CONSTRUCTION_SPOTS):
            if(Company.Money < buildingCost):
                color = (255,0,0)
            cost = font.render("-" + str(buildingCost) + "$", True, color)
            screen.blit(cost, (pos1[0], pos1[1] - 10))
        else:
            color = (255,0,0)
            selectorBoxTL = Map.getScreenPositionOfCoord(pos[0], pos[1])
            selectorBoxTR  = Map.getScreenPositionOfCoord(pos[0]+1, pos[1])
            selectorBoxBR = Map.getScreenPositionOfCoord(pos[0]+1, pos[1]+1)
            selectorBoxBL = Map.getScreenPositionOfCoord(pos[0], pos[1]+1)
            pygame.draw.line(screen, color, selectorBoxTL, selectorBoxTR)
            pygame.draw.line(screen, color, selectorBoxTR, selectorBoxBR)
            pygame.draw.line(screen, color, selectorBoxBR, selectorBoxBL)
            pygame.draw.line(screen, color, selectorBoxBL, selectorBoxTL)
    

            



            
            
        


def onMouseRelease(x,y):
    global buildStart
    pos = mousePosToCoord(x,y)

    if(buildMode == BUILD_MODE_ROAD):
        handleBuildRoad(pos)
    elif(buildMode == BUILD_MODE_LANDFILL):
        handleBuildLandfill(pos)
    elif(buildMode == BUILD_MODE_FIRE):
        handleIncenerator(pos)
    elif(buildMode == BUILD_MODE_RECYCLE):
        handleRecycle(pos)



def onMouseRightClick(x,y):
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
    return [int(x2d), int(y2d)]





#---------------------------------------- ROAD METHODS -----------------------------------------------------------------

def initRoadBuild(pos):
    global buildStart
    if(pos[0] >= 0 and pos[0] <= MAP_WIDTH and pos[1] >= 0 and pos[1] <= MAP_HEIGHT):
        buildStart = [pos[0], pos[1]]



def handleBuildRoad(pos):
    global buildStart
    if(buildStart[0] != None):
        roadwidth = pos[0]- buildStart[0]
        roadheight = pos[1] - buildStart[1]
        totalRoad = roadwidth * roadheight


        if(totalRoad*COST_OF_ROAD <= Company.Money ):
            if(roadheight == 0 or roadwidth == 0):
                
                for x in range(min(buildStart[0], buildStart[0]+roadwidth), max(buildStart[0]+1, buildStart[0]+roadwidth+1)):
                    for y in range(min(buildStart[1], buildStart[1]+roadheight),max(buildStart[1]+1, buildStart[1]+roadheight+1)):
                        if(Map.getTile(x, y) in VALID_CONSTRUCTION_SPOTS):
                            Map.setTile(x,y,Map.TILES["user-road"])
                            Company.Money -= COST_OF_ROAD
        buildStart[0] = None
        buildStart[1] = None

#---------------------------------------- LANDFILL METHODS -----------------------------------------------------------------


def initLandfillBuild(pos):
    global buildStart
    if(pos[0] >= 0 and pos[0] <= MAP_WIDTH and pos[1] >= 0 and pos[1] <= MAP_HEIGHT):
        buildStart = [pos[0], pos[1]]
        

def handleBuildLandfill(pos):
    global buildStart
    if(buildStart[0] != None):
        landfillwidth = pos[0] - buildStart[0]
        landfillheight = pos[1] - buildStart[1]
        landfillArea = (abs(landfillwidth) + 1)*(abs(landfillheight)+1)

        canBuild = True
        ListBlocks = []

        if(landfillArea*COST_OF_LANDFILL <= Company.Money):
            if(abs(landfillwidth)+1 >= 3 and abs(landfillheight)+1 >= 3):
                for x in range(min(buildStart[0], buildStart[0]+landfillwidth), max(buildStart[0]+1, buildStart[0]+landfillwidth+1)):
                    for y in range(min(buildStart[1], buildStart[1]+landfillheight),max(buildStart[1]+1, buildStart[1]+landfillheight+1)):
                        if(Map.getTile(x,y) not in VALID_CONSTRUCTION_SPOTS):
                            buildStart[0] = None
                            canBuild = False
                            break
                        else:
                            ListBlocks.append((x,y))
            else:
                canBuild = False
        else:
            canBuild = False
        if canBuild:            
            for block in ListBlocks:
                Map.setTile(block[0],block[1], Map.TILES["landfill"])
                Map.GMAP[block[0]][block[1]] = "00"
            
            Company.Money -= COST_OF_LANDFILL*landfillArea


        buildStart[0] = None
#---------------------------------------- BULLDOZE METHODS -----------------------------------------------------------------
def handleDelete(pos):
    
    tileV = Map.getTile(pos[0], pos[1])
    costToDelete = Map.TILEOBJECTS[tileV][0]
    if costToDelete != -1:
        if(Company.Money >= costToDelete and tileV != Map.TILES["landfill"]):
            Map.setTile(pos[0],pos[1], Map.ORIGINAL_MAP[pos[0]][pos[1]])
            Map.GMAP[pos[0]][pos[1]] = Map.ORIGINAL_GMAP[pos[0]][pos[1]]
            Company.Money -= costToDelete
            if(Map.isHouseTile(pos[0], pos[1], original=True) or Map.ORIGINAL_MAP[pos[0]][pos[1]] == Map.TILES["road"]):
                Map.setTile(pos[0], pos[1], Map.TILES["grass"])
            if(tileV == Map.TILES["fire"]):
                landfill = landfillNextToPos(pos)
                if(landfill != None):
                    Map.Landfillgroups[Map.LandfillTiles[landfill]][3] -= 1
            elif(tileV == Map.TILES["recycle"]):
                landfill = landfillNextToPos(pos)
                if(landfill != None):
                    Map.Landfillgroups[Map.LandfillTiles[landfill]][4] -= 1
            elif(tileV == Map.TILES["blackhole"]):
                landfill = landfillNextToPos(pos)
                if(landfill != None):
                    Map.Landfillgroups[Map.LandfillTiles[landfill]][5] -= 1
        if(tileV == Map.TILES["landfill"]):
            group = Map.Landfillgroups[Map.LandfillTiles[(pos[0], pos[1])]]
            print(group)
            if(group[0] <= group[1] - GARBAGE_PER_LANDFILL_TILE):
                if(buildingNextToPos(pos) == None):
                    if(Company.Money >= costToDelete):
                        Company.Money -= costToDelete
                        group[1] -= GARBAGE_PER_LANDFILL_TILE
                        Map.LandfillTiles.pop((pos[0], pos[1]))
                        Map.setTile(pos[0],pos[1], Map.ORIGINAL_MAP[pos[0]][pos[1]])
                        Map.GMAP[pos[0]][pos[1]] = Map.ORIGINAL_GMAP[pos[0]][pos[1]]

            
                
        
#---------------------------------------  BUILDING HANDLE -------------------------------------
def handleIncenerator(pos):
    tile = Map.getTile(pos[0], pos[1])
    if(tile in VALID_CONSTRUCTION_SPOTS):
        landfill = landfillNextToPos(pos)
        if(landfill != None):
            group = Map.Landfillgroups[Map.LandfillTiles[landfill]]
            if(Company.Money >= COST_OF_BURNER):
                group[3] += 1
                Map.setTile(pos[0], pos[1], Map.TILES["fire"])
                Company.Money -= COST_OF_BURNER

def handleBlackhole(pos):
    global blackholepos
    blackholepos = pos
    tile = Map.getTile(pos[0], pos[1])
    if(tile in VALID_CONSTRUCTION_SPOTS):
        landfill = landfillNextToPos(pos)
        if(landfill != None):
            group = Map.Landfillgroups[Map.LandfillTiles[landfill]]
            if(Company.Money >= COST_OF_BHOLE):
                group[5] += 1
                Map.setTile(pos[0], pos[1], Map.TILES["blackhole"])
                Company.Money -= COST_OF_BHOLE


def handleRecycle(pos):
    tile = Map.getTile(pos[0], pos[1])
    if(tile in VALID_CONSTRUCTION_SPOTS):
        landfill = landfillNextToPos(pos)
        if(landfill != None):
            group = Map.Landfillgroups[Map.LandfillTiles[landfill]]
            if(Company.Money >= COST_OF_RECYCLE):
                group[4] += 1
                Map.setTile(pos[0], pos[1], Map.TILES["recycle"])
                Company.Money -= COST_OF_RECYCLE


def landfillNextToPos(pos):
    if(Map.getTile(pos[0]-1,pos[1]) == Map.TILES["landfill"]):
        return (pos[0]-1,pos[1])
    elif(Map.getTile(pos[0]+1,pos[1]) == Map.TILES["landfill"]):
        return (pos[0]+1,pos[1])
    elif(Map.getTile(pos[0],pos[1]-1) == Map.TILES["landfill"]):
        return (pos[0],pos[1]-1)
    elif(Map.getTile(pos[0],pos[1]+1) == Map.TILES["landfill"]):
        return (pos[0],pos[1]+1)
    else:
        return None

def buildingNextToPos(pos):
    buildingtiles = [Map.TILES["fire"], Map.TILES["recycle"], Map.TILES["blackhole"]]


    if(Map.getTile(pos[0]-1,pos[1]) in buildingtiles):
        return (pos[0]-1,pos[1])
    elif(Map.getTile(pos[0]+1,pos[1]) in buildingtiles):
        return (pos[0]+1,pos[1])
    elif(Map.getTile(pos[0],pos[1]-1) in buildingtiles):
        return (pos[0],pos[1]-1)
    elif(Map.getTile(pos[0],pos[1]+1) in buildingtiles):
        return (pos[0],pos[1]+1)
    else:
        return None