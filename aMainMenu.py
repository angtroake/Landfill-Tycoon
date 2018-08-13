import pygame
import ImageUtil
from Constants import *

#               0       1       2(0,1,2,3)
#         id: [text, function, [x,y,w,h]]
buttons = {}

font = None

def render(screen):
    global buttons
    global font
    Name = ImageUtil.get_image("menu-name-black")
    Back = ImageUtil.get_image("menu-back")
    screen.blit(Back, (0,0))
    screen.blit(Name, (screen.get_width()/2-(Name.get_width()/2), 100))
    for b in buttons:
        button = buttons[b]
        pygame.draw.rect(screen, (81, 144, 184), button[2])
        text = font.render(button[0], True, (255,255,255))
        screen.blit(text, ((button[2][0] + button[2][2]/2) - (text.get_width()/2), (button[2][1] + button[2][3]/2)-(text.get_height()/2)))



def tick():
    None

def onclick(pos):
    global buttons
    for b in buttons:
        button = buttons[b]
        if(pos[0] > button[2][0] and pos[0] < (button[2][0] + button[2][2])):
            if(pos[1] > button[2][1] and pos[1] < (button[2][1] + button[2][3])):
                button[1]()


def init(screen, functionChangeState):
    global buttons
    global font
    buttons[0] = ["Start Game", functionChangeState, [screen.get_width()/2 - 200, 300 , 400, 75]]
    font = pygame.font.Font(None, 30)

