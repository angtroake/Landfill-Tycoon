import Map


buildMode = 0

def onMouseClick(x,y):
    Map = Map.MAP
    mouseY = int(((x+scrollY)/TILE_HEIGHT) + ((x+scrollX) / TILE_WIDTH))
    mouseX = -int((-(y+scrollX)/TILE_WIDTH) + ((y+scrollY) / TILE_HEIGHT))



def onMouseRightClick(x,y):
    Map = Map.MAP