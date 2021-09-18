
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame


pygame.font.init()
width, height = 1366, 768                           # 924, 693; 1366, 768
size_py = (width, height)
screen = pygame.display.set_mode(size_py, pygame.FULLSCREEN)
clock = pygame.time.Clock()


fps = 60

run = True
while run:
    
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEMOTION:
            lx = event.pos[0]
            ly = event.pos[1]

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:


    clock.tick(fps)
    pygame.display.flip()
