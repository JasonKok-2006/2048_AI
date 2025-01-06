import pygame
import sys
import random

#screen parameters
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 400

#tile parameter
tile_size = 100

#dictionary to link value with images
images = dict([(0, "tiles/0.png"), (2, "tiles/2.png"), (4, "tiles/4.png"), (8, "tiles/8.png"), (16, "tiles/16.png"), (32, "tiles/32.png"), (64, "tiles/64.png"), (128, "tiles/128.png"), (256, "tiles/256.png"), (512, "tiles/512.png"), (1024, "tiles/1024.png"), (2048, "tiles/2048.png")])

#colours
bg = (200, 200, 200)
line = (0, 0, 0)

#creates the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.init()
pygame.display.set_caption("2048 AI")

class Game:

    #2D array to keep track of the game
    board = [[0, 0, 0, 0],
            [0, 2, 0, 0],
            [0, 0, 2, 0],
            [0, 0, 0, 0]]

    def __init__(self):
        #screen parameters
        SCREEN_WIDTH = 400
        SCREEN_HEIGHT = 400

        #tile parameter
        tile_size = 100

        #dictionary to link value with images
        images = dict([(0, "tiles/0.png"), (2, "tiles/2.png"), (4, "tiles/4.png"), (8, "tiles/8.png"), (16, "tiles/16.png"), (32, "tiles/32.png"), (64, "tiles/64.png"), (128, "tiles/128.png"), (256, "tiles/256.png"), (512, "tiles/512.png"), (1024, "tiles/1024.png"), (2048, "tiles/2048.png")])

        #2D array to keep track of the game
        Game.board = [[0, 0, 0, 0],
                      [0, 2, 0, 0],
                      [0, 0, 2, 0],
                      [0, 0, 0, 0]]

        #colours
        bg = (200, 200, 200)
        line = (0, 0, 0)

        #creates the game window
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        pygame.init()
        pygame.display.set_caption("2048 AI")

        Game.reset()

    def reset():
        #2D array to keep track of the game
        Game.board = [[0, 0, 0, 0],
                      [0, 2, 0, 0],
                      [0, 0, 2, 0],
                      [0, 0, 0, 0]]

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
                if Game.board[i][j] > 0:
                    tile = pygame.image.load(images[Game.board[i][j]])
                    screen.blit(tile, ((j * 100) + 1, (i * 100) + 1))

    def left():
        for i in range(0, 4):
            new_row = []

            #strips the row of empty tiles
            for tile in Game.board[i]:
                if tile != 0:
                    new_row.append(tile)

            #merge same values if they are adjacent
            for j in range(0, len(new_row) - 1):
                if new_row[j] == new_row[j+1]:
                    new_row[j] *= 2
                    new_row[j+1] = 0
            
            #find out how many zeros there are
            zero_count = new_row.count(0)

            #removes all zeros
            for x in range(zero_count):
                new_row.remove(0)

            #fills the new row up with zeros
            while len(new_row) < 4:
                new_row.append(0)

            #replaces the old row with the new row
            Game.board[i] = new_row

    def right():
        for i in range(4):  # Iterate over each row
            new_row = []

            #reverse the row to handle movement to the right
            reversed_row = Game.board[i][::-1]

            #strip the row of empty tiles
            for tile in reversed_row:
                if tile != 0:
                    new_row.append(tile)

            #merge adjacent tiles
            for j in range(len(new_row) - 1):
                if new_row[j] == new_row[j + 1]: 
                    new_row[j] *= 2 
                    new_row[j + 1] = 0  

            #remove zeros created during merging
            zero_count = new_row.count(0)
            for _ in range(zero_count):
                new_row.remove(0)

            #fill the row up with zeros to maintain length 4
            while len(new_row) < 4:
                new_row.append(0)

            #reverse the row back to its original order
            Game.board[i] = new_row[::-1]


    def up():
        for i in range(0, 4):
            new_column = []

            #makes a new column ignoring empty tiles
            for j in range(0, 4):
                if Game.board[j][i] != 0:
                    new_column.append(Game.board[j][i])

            #merge same values if they are adjacent
            for j in range(0, len(new_column) - 1):
                if new_column[j] == new_column[j+1]:
                    new_column[j] *= 2
                    new_column[j+1] = 0
            
            #find out how many zeros there are
            zero_count = new_column.count(0)

            #removes all zeros
            for x in range(zero_count):
                new_column.remove(0)

            #fills the new row up with zeros
            while len(new_column) < 4:
                new_column.append(0)

            #replaces the old row with the new row
            for k in range(0, 4):
                Game.board[k][i] = new_column[k]

    def down():
        for i in range(0, 4):
            new_column = []

            #makes a new column ignoring empty tiles
            for j in range(0, 4):
                j = 3 - j #reverses the column
                if Game.board[j][i] != 0:
                    new_column.append(Game.board[j][i])
            


            #merge same values if they are adjacent
            for j in range(0, len(new_column) - 1):
                if new_column[j] == new_column[j+1]:
                    new_column[j] *= 2
                    new_column[j+1] = 0
            
            #find out how many zeros there are
            zero_count = new_column.count(0)

            #removes all zeros
            for x in range(zero_count):
                new_column.remove(0)

            #fills the new row up with zeros
            while len(new_column) < 4:
                new_column.append(0)

            #reverses the row again
            new_column = new_column[::-1]

            #replaces the old row with the new row
            for k in range(0, 4):
                Game.board[k][i] = new_column[k]

    def place_tile():
        empty_spaces = []

        #checks the board for empty spaces
        for row in range(0, 4):
            for col in range(0, 4):
                if Game.board[row][col] == 0:
                    #appends a value tp the list (0-15)
                    empty_spaces.append((row * 4) + col)

        #chooses a value randomly from that list
        new_location_value = empty_spaces[random.randint(0, len(empty_spaces) - 1)]

        #chooses the value of the new tile (5% chance for a 4)
        new_tile_value = random.randint(0, 100)
        if new_tile_value <= 95:
            new_tile_value = 2
        else:
            new_tile_value = 4

        #update the board
        row = new_location_value // 4
        col = new_location_value % 4
        Game.board[row][col] = new_tile_value

    def game_over():
        # Check for empty spaces
        for row in Game.board:
            if 0 in row:
                return False

        # Check for possible merges horizontally
        for row in Game.board:
            for col in range(3):  # Only need to check adjacent tiles
                if row[col] == row[col + 1]:
                    return False

        # Check for possible merges vertically
        for col in range(4):
            for row in range(3):  # Only need to check adjacent tiles
                if Game.board[row][col] == Game.board[row + 1][col]:
                    return False

        return True  # No empty spaces or possible merges

    def check_win():
        for i in range(0, 4):
            for j in range(0, 4):
                if Game.board[i][j] == 2048:
                    return True
                
    def game_step(action):
        #keeps track of the board change
        board_changed = False

        #happens if an input has been made
        for event in pygame.event.get():
            #if the close window button hass been pressed - the code stops
            if event.type == pygame.QUIT:
                sys.exit()
                run = False

        #This might cause crashes but we'll see later on
        previous_board = [row[:] for row in Game.board]  # Copy the board

        if action == pygame.K_LEFT:
            Game.left()

        elif action == pygame.K_RIGHT:
            Game.right()

        elif action == pygame.K_UP:
            Game.up()

        elif action == pygame.K_DOWN:
            Game.down()

        # Check if the board has changed
        board_changed = (previous_board != Game.board)

        #place a tile if the board has changed
        if board_changed:
            Game.place_tile()

        # Check for game over
        if Game.game_over():
            print("Game Over!")

        #check if the game has been finished
        if Game.check_win():
            print("You win!")
            run = False

        #functions to change the display of the game screen
        Game.draw_grid(tile_size)
        Game.correct_tiles()

        pygame.display.update()

run = True
while run:
    Game.game_step()

pygame.display.quit()
pygame.quit()
