from collections import namedtuple
import csv
from Constants import *
import pygame
import ImageUtil

scrollX = 0
scrollY = 0

Zoom = 1


MAP = None


buildMode = 0


pollution = 0


def loadMap():
    with open("maps/map1/Map.csv") as csvmap:
        reader = csv.reader(csvmap)
        global MAP
        MAP = list(reader)
        MAP[0][0] = '0'




def getTileImage(x,y):
    global MAP
    val = MAP[x][y]
    if(val == '0'):
        return ImageUtil.get_image("water")
    elif(val == '1'):
        return ImageUtil.get_image("grass")
    elif(val == '2'):
        return ImageUtil.get_image("road")
    else:
        return ImageUtil.get_image("temp")




def render(screen):
    global scrollX
    global scrollY
    global Zoom
    global buildMode
    
    #--------------------------------  TILE RENDERING   -------------------------------------

    for cellY in range(0,MAP_HEIGHT+1):
        for cellX in range(0,MAP_WIDTH+1):
            posX = ((cellX * TILE_WIDTH / 2) + (cellY * TILE_WIDTH / 2) - scrollX)*Zoom
            posY = ((cellY * TILE_HEIGHT / 2) - (cellX * TILE_HEIGHT / 2) - scrollY)*Zoom

            if(posX  > 0 and posX < screen.get_width() - 20 and posY > 0 and posY < screen.get_height()):
                color = (100,100,100)
                image = getTileImage(cellX, cellY)

                screen.blit(pygame.transform.scale(image, (int(TILE_WIDTH*Zoom), int(TILE_HEIGHT*Zoom))), (posX, posY-TILE_HEIGHT*Zoom/2))
                
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

    #---------------------------------------------------------------------------------------------
    



#TODO Adjust render limit when testing finished
#TODO FIX CURSOR ON ZOOM
            

            
