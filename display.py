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
    K_m,
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

GRID_SIZE = 3
CELL_WIDTH = 100
CELL_DISTANCE = 10
GRID_WIDTH = CELL_WIDTH*GRID_SIZE + CELL_DISTANCE*(GRID_SIZE+1)
SCREEN_WIDTH = GRID_WIDTH + 2*CELL_WIDTH
SCREEN_HEIGHT = SCREEN_WIDTH

# Game object
game = GameLogic(GRID_SIZE, 8)

# Set up the drawing window and window name
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption('2048 clone')

### COLORS ###
grid_color = (187, 173, 160)
dark_color = (119, 110, 101)
light_color = (249, 246, 242)
black = (0,0,0)
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
text_surface = menufont.render('Press space bar to start', True, dark_color)

# IN-GAME
gamefont = pg.font.SysFont('Arial', 25)
blockfont = pg.font.SysFont('UbuntuMono-R', 50)
title = gamefont.render('2048 clone', True, black)
instructions = gamefont.render('Use arrow keys to play. Press Q to quit.', True, black)

# END-OF-GAME
overlay = pg.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
overlay.fill(light_color)
overlay.set_alpha(150)

text_loss = gamefont.render('Oof.', True, black)
text_win = gamefont.render('You win! Press any key to keep playing.', True, black)
text_options = gamefont.render('Options: ', True, black)
text_undo = gamefont.render('U: undo.', True, black)
text_restart = gamefont.render('R: restart.', True, black)
text_menu = gamefont.render('M: menu.', True, black)
text_quit = gamefont.render('Q: quit.', True, black)


### DRAWING FUNCTIONS ###

def draw_menu():
    screen.fill(light_color)
    screen.blit(text_surface, (10, 10))
    pg.display.flip()

def draw_game():
    screen.fill(light_color)
    screen.blit(title, (CELL_WIDTH, CELL_WIDTH/2))
    screen.blit(instructions, ((SCREEN_WIDTH - instructions.get_width())//2, (SCREEN_HEIGHT - CELL_WIDTH/2)))

    score_surface = gamefont.render("Score: " + str(game.score), True, black)
    screen.blit(score_surface, ((SCREEN_WIDTH-(CELL_WIDTH+score_surface.get_width())), CELL_WIDTH/2))

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

# Render multiple lines of text directly beneath one another.
def textrender(lines):
    for i, line in enumerate(lines):
        screen.blit(line, (CELL_WIDTH//2, CELL_WIDTH+line.get_height()*i))

### GAME LOOP ###

in_game = True
skip_menu = False
while in_game:

    game.reset()
    
    ### MENU ###

    if not skip_menu: 
        waiting = True 
        while waiting and in_game:  #hot fix. should be improved both her and in game loop

            for event in pg.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        waiting = False
                elif event.type == QUIT:
                    waiting, in_game = False, False 

            draw_menu()


    ### MAIN GAME ###

    # Run until the user asks to quit
    running = True
    win_confirmed = False
    game.spawn_tile()
    # Deque should be O(1) in both directions and automatically remove items from opposite end when full
    prev_states = deque(maxlen=3)

    while running and in_game:

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
                        print("Undoing move.")
                elif event.key == K_m:  # return to main menu
                    running, skip_menu = False, False
                elif event.key == K_r:  # restart
                    running, skip_menu = False, True
                elif event.key == K_q:  #quit
                    running, in_game = False, False

                if save_next:
                    if not prev_states or (prev_states and prev_states[-1] != game.game_grid):
                        prev_states.append(old_state)
            # Did the user click the window close button? If so, stop the loop.
            elif event.type == QUIT:
                running, in_game = False, False

        draw_game()

        if game.game_over:
            screen.blit(overlay, (0,0))
            textrender([text_loss, text_options, text_undo, text_restart, text_menu, text_quit])
            pg.display.flip()
            waiting = True

            while waiting:
                for event in pg.event.get():
                    if event.type == KEYDOWN:
                        if event.key == K_u:
                            game.game_grid = prev_states.pop()
                            waiting, game.game_over = False, False
                            # something's wrong with this one I think.
                        elif event.key == K_m:  # return to main menu
                            waiting, running, skip_menu = False, False, False
                        elif event.key == K_r:  # restart
                            waiting, running, skip_menu = False, False, True
                        elif event.key == K_q:
                            waiting, running, in_game = False, False, False
        
        if not win_confirmed and game.game_won:
            screen.blit(overlay, (0,0))
            textrender([text_win, text_options, text_restart, text_menu, text_quit])
            pg.display.flip()
            waiting, win_confirmed = True, True
            
            while waiting:
                for event in pg.event.get():
                    if event.type == KEYDOWN:
                        if event.key == K_m:  # return to main menu
                            waiting, running, skip_menu = False, False, False
                        elif event.key == K_r:
                            waiting, running, skip_menu = False, False, True
                        elif event.key == K_q:
                            waiting, running, in_game = False, False, False
                        else:
                            waiting = False

# Done! Time to quit.
pg.quit()