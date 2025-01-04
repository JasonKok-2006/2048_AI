import pygame
import sys

pygame.init()

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

run = True
while run:

    #check if the close button has been pressed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
            run == False

pygame.display.quit()
pygame.quit()
