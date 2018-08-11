import pygame
import os

_loaded_images = {}

def create_image(name, path, alpha = True):
    global _loaded_images
    if(get_image(name) == None):
        good_path = path.replace('/', os.sep).replace('\\', os.sep)
        image = pygame.image.load(good_path)
        image = image.convert_alpha()
        if(alpha == False):
            image = image.convert()
        _loaded_images[name] = image
        return True
    else:
        return False

def get_image(name):
    return _loaded_images.get(name)
