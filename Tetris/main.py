import pygame,manager
from globals import *

pygame.init()

running  = True
clock = pygame.time.Clock()
screen = pygame.display.set_mode((width*size, height*size))
manager = manager.SceneManager()

while running:       
    keypressed = manager.scene.handles()
    manager.scene.updates(keypressed)
    manager.scene.render(screen)
    clock.tick(60)


