import os
import pygame
from pygame.locals import *

move = 11

pygame.init()
screen = pygame.display.set_mode((500, 500), HWSURFACE | DOUBLEBUF | RESIZABLE)
pic = pygame.image.load("resources/Coal.png")
screen.blit(pygame.transform.scale(pic, (move, move)), (0, 0))
pygame.display.flip()

while True:
    pygame.event.pump()
    event = pygame.event.wait()
    screen.fill(pygame.Color("black"))
    screen.blit(pygame.transform.scale(pic, (move, move)), (10, 10))
    if event.type == QUIT:
        pygame.display.quit()
    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
        if move >= 11:
            move -= 1
    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
        move += 1
    pygame.display.flip()