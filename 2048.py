import pygame
import sys

pygame.init()
pygame.display.set_caption("2048 AI")

#screen parameters
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 400

#tile parameter
tile_size = 100

#dictionary to link value with images
images = dict([(2, "tiles/2.png"), (4, "tiles/4.png"), (8, "tiles/8.png"), (16, "tiles/16.png"), (32, "tiles/32.png"), (64, "tiles/64.png"), (128, "tiles/128.png"), (256, "tiles/256.png"), (512, "tiles/512.png"), (1024, "tiles/1024.png"), (2048, "tiles/2048.png")])

#2D array to keep track of the game
board = [[0, 0, 0, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0],
         [4, 0, 2, 0]]

#colours
bg = (200, 200, 200)
line = (0, 0, 0)

#creates the game window
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

#this function displays the tiles to the screen
def correct_tiles():
    for i in range(0, 4):
        for j in range(0, 4):
            if board[i][j] > 0:
                tile = pygame.image.load(images[board[i][j]])
                screen.blit(tile, ((j * 100) + 1, (i * 100) + 1))
                

run = True
while run:
    #check if the close button has been pressed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
            run == False

    draw_grid(tile_size)
    correct_tiles()

    pygame.display.update()


pygame.display.quit()
pygame.quit()
