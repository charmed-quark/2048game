import pygame as pg 
from gamelogic import GameLogic
from collections import deque

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_SPACE,
    K_r,
    K_q,
    K_u,
    KEYDOWN,
    MOUSEBUTTONDOWN,
    QUIT,
)

pg.init()
pg.font.init()

### CONFIGS ###

GRID_SIZE = 4
CELL_WIDTH = 100
CELL_DISTANCE = 10
GRID_WIDTH = CELL_WIDTH*GRID_SIZE + CELL_DISTANCE*(GRID_SIZE+1)
SCREEN_WIDTH = GRID_WIDTH + 2*CELL_WIDTH
SCREEN_HEIGHT = SCREEN_WIDTH


# Set up the drawing window and window name
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption('2048 clone')

### COLORS ###
grid_color = (187, 173, 160)
dark_color = (119, 110, 101)
light_color = (249, 246, 242)
cell_colors = {
    0 : (205, 193, 180),
    2 : (238, 228, 218),
    4 : (238, 225, 201),
    8 : (243, 178, 122),
    16 : (246, 150, 100),
    32 : (247, 124, 95),
    64 : (247, 95, 59),
    128 : (243, 217, 107),
    256 : (237, 204, 98),
    512 : (229, 192, 42),
    1024 : (227, 186, 20),
    2048 : (49, 100, 92),
    4096 : (247, 100, 116),
    8192 : (241, 75, 97),
    16384 : (235, 66, 63),
    32768 : (108, 183, 214),
    65536 : (93, 161, 226),
    131072 : (0, 127, 194),
}

### TEXT BLOCKS ###

# MENU
menufont = pg.font.SysFont('Arial', 20)
text_surface = menufont.render('Click anywhere or press space bar to start', True, dark_color)

# IN-GAME
gamefont = pg.font.SysFont('Arial', 25)
blockfont = pg.font.SysFont('UbuntuMono-R', 50)
title_surface = gamefont.render('2048 clone', True, (0, 0, 0))
instructions_surface = gamefont.render('Use arrow keys to play. Press Q to quit.', True, (0, 0, 0))

def draw_menu():
    # Fill the background with off-white
    screen.fill(light_color)

    # Add text
    screen.blit(text_surface, (10, 10))

    pg.display.flip()

def draw_game():
        # Fill the background with off-white
        screen.fill(light_color)

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
                        num_color = dark_color
                    else:
                        num_color = light_color
                    number = blockfont.render(str(cell_value), True, num_color)
                    num_rect = number.get_rect(center=(x+(CELL_WIDTH//2), y+(CELL_WIDTH//2)))
                    screen.blit(number, num_rect)

        # Flip the display (refreshes)
        pg.display.flip()



in_game = True
while in_game:

    game = GameLogic(GRID_SIZE, 2048)
    
    ### MENU ###

    waiting = True 
    while waiting and in_game:  #hot fix. should be improved both her and in game loop

        for event in pg.event.get():
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    waiting = False
            elif event.type == MOUSEBUTTONDOWN:
                mouse_presses = pg.mouse.get_pressed()
                if mouse_presses[0]:    #left mouse button
                    waiting = False
            elif event.type == QUIT:
                waiting = False 
                in_game = False

        draw_menu()

    ### GAME LOOP ###

    # set up text blocks to display

    # Run until the user asks to quit
    running = True
    game.spawn_tile()
    # Deque should be O(1) in both directions and automatically remove items from opposite end when full
    prev_states = deque(maxlen=3)
    #prev_states.append(game.game_grid)
    #print("The previous state is currently...." + str(prev_states[0]))
    while running and not game.game_over:

        old_state = game.game_grid

        for event in pg.event.get():

            save_next = True    # Tracking old states for undo purposes

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
                elif event.key == K_u:  # undo previous move
                    if prev_states and prev_states[-1] != game.game_grid:
                        game.game_grid = prev_states.pop()
                        save_next = False
                        # If we've used undo, we do not want to save the resulting state
                        # because we will get caught in a loop.
                elif event.key == K_q or event.key == K_ESCAPE:  #quit
                    running = False

                if save_next:
                    if not prev_states or (prev_states and prev_states[-1] != game.game_grid):
                        prev_states.append(old_state)
            # Did the user click the window close button? If so, stop the loop.
            elif event.type == QUIT:
                running = False

        draw_game()

    ### LOSING SCREEN ###
    waiting = True
    while waiting and in_game:
        line1 = menufont.render('You lose :(', True, dark_color)
        line2 = menufont.render('Press R to restart or Q/ESC to quit', True, dark_color)

        for event in pg.event.get():
            # Did the user hit a key?
            if event.type == KEYDOWN:
                if event.key == K_r:
                    waiting = False
                    game.game_over = False
                elif event.key == K_q or event.key == K_ESCAPE:  #quit
                    waiting = False
                    in_game = False
            elif event.type == QUIT:
                waiting = False 
                in_game = False

        screen.fill(light_color)        
        screen.blit(line1, (10, 10))
        screen.blit(line2, (10, 50))

        pg.display.flip()

# Done! Time to quit.
pg.quit()