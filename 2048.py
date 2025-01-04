import pygame
import sys

pygame.init()

#screen parameters
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 400

tile_size = 100

#colours
bg = (200, 200, 200)
line = (0, 0, 0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

#This finction draws the grid to keep the tiles in
def draw_grid(tile_size):
    screen.fill(bg)

    #veritcal lines
    for x in range(tile_size, SCREEN_WIDTH, tile_size):
        pygame.draw.line(screen, line, (x,0), (x, SCREEN_HEIGHT))

    #horizontal lines
    for x in range(tile_size, SCREEN_HEIGHT, tile_size):
        pygame.draw.line(screen, line, (0, x), (SCREEN_WIDTH, x))


run = True
while run:
    #check if the close button has been pressed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
            run == False

    draw_grid(tile_size)

    pygame.display.update()


pygame.display.quit()
pygame.quit()
