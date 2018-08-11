import Map
from Constants import *

buildMode = 0

def onMouseClick(x,y):
    mapInstance = Map.MAP
    Zoom = Map.Zoom
    scrollX = Map.scrollX
    scrollY = Map.scrollY

    mouseY = int(((y+scrollY)/TILE_HEIGHT) + ((x+scrollX) / TILE_WIDTH))
    mouseX = -int((-(x+scrollX)/TILE_WIDTH) + ((y+scrollY) / TILE_HEIGHT))

    hoverPosX = ((mouseX * TILE_WIDTH*Zoom / 2) + (mouseY * TILE_WIDTH*Zoom / 2) - scrollX)*Zoom
    hoverPosY = ((mouseY * TILE_HEIGHT*Zoom / 2) - (mouseX * TILE_HEIGHT*Zoom / 2) - scrollY)*Zoom

    x2d = ((hoverPosX+scrollX)-2*(hoverPosY+scrollY))/TILE_WIDTH
    y2d = ((hoverPosY+scrollY)/TILE_HEIGHT + (hoverPosX+scrollX)/TILE_WIDTH)

    if buildMode == 1:
        mapInstance[mouseX][mouseY] = '2'


def onMouseRightClick(x,y):
    mapInstance = Map.MAP
    Zoom = Map.Zoom
    scrollX = Map.scrollX
    scrollY = Map.scrollY

    mouseY = int(((x+Map.scrollY)/TILE_HEIGHT) + ((x+Map.scrollX) / TILE_WIDTH))/TILE_WIDTH
    mouseX = -int((-(y+Map.scrollX)/TILE_WIDTH) + ((y+Map.scrollY) / TILE_HEIGHT))/TILE_HEIGHT

    hoverPosX = ((mouseX * TILE_WIDTH*Zoom / 2) + (mouseY * TILE_WIDTH*Zoom / 2) - scrollX)*Zoom
    hoverPosY = ((mouseY * TILE_HEIGHT*Zoom / 2) - (mouseX * TILE_HEIGHT*Zoom / 2) - scrollY)*Zoom

    