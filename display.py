import pygame as pg 
from gamelogic import GameLogic

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_q,
    KEYDOWN,
    QUIT,
)

pg.init()
pg.font.init()

GRID_SIZE = 4
CELL_WIDTH = 100
CELL_DISTANCE = 10
GRID_WIDTH = CELL_WIDTH*GRID_SIZE + CELL_DISTANCE*(GRID_SIZE+1)
SCREEN_WIDTH = GRID_WIDTH + 2*CELL_WIDTH
SCREEN_HEIGHT = SCREEN_WIDTH

game = GameLogic(GRID_SIZE, 2048)

# Set up the drawing window and window name
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption('2048 clone')

### COLORS ###
grid_color = (187, 173, 160)
cell_colors = {
    0 : (205, 193, 180),
    2 : (238, 228, 218),
    4 : (238, 225, 201),
    8 : (243, 178, 122),
    16 : (246, 150, 100),
    32 : (247, 124, 95),
    64 : (247, 95, 59),
    128 : (205, 193, 180),
    256 : (237, 204, 98),
    512 : (205, 193, 180),
    1024 : (205, 193, 180),
    2048 : (205, 193, 180),
}
# for the individual tile colors we should probably use a dict to retrieve them.

# set up text blocks to display
myfont = pg.font.SysFont('Ubuntu Light', 50)
title_surface = myfont.render('2048 clone', False, (0, 0, 0))
instructions_surface = myfont.render('Use arrow keys to play.', False, (0, 0, 0))


# Run until the user asks to quit
running = True
game.spawn_tile()
while running:

    for event in pg.event.get():
        # Did the user hit a key?
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                game.turn("left")
            elif event.key == K_RIGHT:
                game.turn("right")
            elif event.key == K_UP:
                game.turn("up")
            elif event.key == K_DOWN:
                game.turn("down")
            elif event.key == K_q or event.key == K_ESCAPE:  #quit
                running = False
        # Did the user click the window close button? If so, stop the loop.
        elif event.type == QUIT:
            running = False

    # Fill the background with off-white
    screen.fill((249, 246, 242))

    # Draw text blocks
    screen.blit(title_surface, (CELL_WIDTH, CELL_WIDTH/2))
    screen.blit(instructions_surface, (CELL_WIDTH, (SCREEN_WIDTH - CELL_WIDTH/2)))

    # Draw grid. The final argument makes the corners rounded.
    pg.draw.rect(screen, grid_color, (CELL_WIDTH, CELL_WIDTH, GRID_WIDTH, GRID_WIDTH), 0, 10)

    # Draw each cell.
    increment = CELL_WIDTH + CELL_DISTANCE
    for row in range(GRID_SIZE):
        x = 0
        y = increment + row*increment
        for col in range(GRID_SIZE):
            x += increment
            cell_value = game.game_grid[row][col]
            pg.draw.rect(screen, cell_colors[cell_value], (x, y, CELL_WIDTH, CELL_WIDTH), 0, 5)
            if cell_value != 0:
                if cell_value <= 4:
                    num_color = (119, 110, 101) #dark color
                else:
                    num_color = (249, 246, 242) #light color
                number = myfont.render(str(cell_value), False, num_color)
                screen.blit(number, (x, y))


    # Flip the display (refreshes)
    pg.display.flip()

# Done! Time to quit.
pg.quit()