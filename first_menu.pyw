from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame

fps = 30
pygame.init()
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption('')
clock = pygame.time.Clock()

run = True
while run:
    clock.tick(fps)
    screen.fill(pygame.Color('White'))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.flip()
pygame.quit()
