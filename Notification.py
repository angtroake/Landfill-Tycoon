import pygame
import datetime
from Constants import *


NotificationsToPost = []


NotificationPlaying = False
CurrentNotification = None


font = None

timestart = None

y = 0


def init():
    global font
    font = pygame.font.Font(None, 50)

def render(screen):
    global CurrentNotification
    global y
    posy = screen.get_height() - y

    notScreen = pygame.Surface((800, 150))
    pygame.draw.rect(notScreen, (255, 255, 255), [0,0, notScreen.get_width(), notScreen.get_height()])

    lines = []
    curLine = 0
    if(CurrentNotification != None):
        words = CurrentNotification.split()
        for i in range(0, len(words)):
            if(curLine >= len(lines)):
                lines.append( words[i] + " ")
                continue
            if(16*(len(lines[curLine]) + len(words[i])) < 750):
                lines[curLine] += words[i] + " "
            else:
                curLine += 1
                lines.append(words[i] + " ")
            
        index = 0
        for line in lines:
            text = font.render(line, True, (0,0,0))
            notScreen.blit(text, (notScreen.get_width()/2 - text.get_width()/2,30 + index*30))
            index += 1

        screen.blit(notScreen, (screen.get_width()/2 - notScreen.get_width()/2, posy))


def tick():
    global NotificationPlaying
    global NotificationsToPost
    global CurrentNotification
    global y
    global timestart

    if(NotificationPlaying == False):
        if(len(NotificationsToPost) > 0):
            NotificationPlaying = True
            CurrentNotification = NotificationsToPost[0]
            NotificationsToPost.pop(0)
            timestart = datetime.datetime.now()
    
    else:
        curTime = datetime.datetime.now()
        if((curTime - timestart).total_seconds() < NOTIFICATION_LENGTH_SECONDS - 2):
            if y < 150:
                y += 2
        else:
            if(y > 0):
                y -= 2
        if((curTime - timestart).total_seconds() >= NOTIFICATION_LENGTH_SECONDS):
            NotificationPlaying = False

        
        



def addNotification(text):
    global NotificationsToPost
    NotificationsToPost.append(text)