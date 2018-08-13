import pygame
import os

_loaded_sounds = {}

def create_sound(name, path, alpha = True):
    global _loaded_sounds
    if(get_sound(name) == None):
        good_path = path.replace('/', os.sep).replace('\\', os.sep)
        sound = pygame.mixer.Sound(good_path)
        _loaded_sounds[name] = sound
        return True
    else:
        return False

def get_sound(name):
    return _loaded_sounds.get(name)

def play_sound(name):
    sound = get_sound(name)
    sound.play()