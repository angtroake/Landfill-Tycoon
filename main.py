import pygame
import sys
import ImageUtil


pygame.init()

screen = pygame.display.set_mode((640, 480))
done = False

font = pygame.font.Font(None, 30)
clock = pygame.time.Clock()

ImageUtil.create_image("test", "res/test.png")


while not done:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    background = pygame.Surface(screen.get_size())
    background.fill((255,255,255))
    background = background.convert()
    screen.blit(background, (0,0))

    screen.blit(ImageUtil.get_image('test'), (100, 100))



    fps = font.render(str(int(clock.get_fps())), True, (0, 0, 0))
    screen.blit(fps, (50,50))

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
sys.exit()