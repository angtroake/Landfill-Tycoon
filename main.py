import pygame
import sys
import ImageUtil
import Map
from pygame.locals import *


pygame.init()

screen = pygame.display.set_mode((1280, 720), DOUBLEBUF)

done = False

font = pygame.font.Font(None, 30)
clock = pygame.time.Clock()

ImageUtil.create_image("test", "res/test.png")
ImageUtil.create_image("grass", "res/tile/tile-grass.png")
ImageUtil.create_image("road", "res/tile/tile-road.png")
ImageUtil.create_image("water", "res/tile/tile-water.png")
ImageUtil.create_image("temp", "res/tile/tile-template.png")

Map.loadMap()


Zoom = 1
ZoomTick = 0


while not done:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if(event.button == 4):
                if(Zoom > 0.5):
                    Zoom -= 0.5
            elif(event.type == 5):
                if(Zoom < 2):
                    Zoom += 0.5
            print(Zoom)
            Map.Zoom = Zoom


    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        Map.scrollX += 20
    elif keys[pygame.K_LEFT]:
        Map.scrollX -= 20
    if keys[pygame.K_UP]:
        Map.scrollY -= 20
    elif keys[pygame.K_DOWN]:
        Map.scrollY += 20

    background = pygame.Surface(screen.get_size())
    background.fill((85,85,85))
    background = background.convert()
    screen.blit(background, (0,0))

    Map.render(screen)



    fps = font.render(str(int(clock.get_fps())), True, (0, 0, 0))
    screen.blit(fps, (50,50))

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
sys.exit()