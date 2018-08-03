import pygame
import os

_loaded_images = {}

def create_image(name, path):
    global _loaded_images
    if(get_image(name) == None):
        good_path = path.replace('/', os.sep).replace('\\', os.sep)
        image = pygame.image.load(good_path)
        _loaded_images[name] = image
        return True
    else:
        return False

def get_image(name):
    return _loaded_images.get(name)
