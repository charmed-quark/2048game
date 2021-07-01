#import sys, pygame as pg, random
import sys, random
from gridmoves import Moves
#pg.init()

class GameLogic:

    #allows us to use the moving functionality
    moves = Moves()

    def __init__(self, grid_size, target_score):
        self.GRID_SIZE = grid_size
        self.TARGET_SCORE = target_score
        self.game_over = False
        self.game_won = False
        self.game_grid = [[0 for x in range(self.GRID_SIZE)] for y in range(self.GRID_SIZE)]
        self.empty_cells = [(x, y) for x in range(self.GRID_SIZE) for y in range(self.GRID_SIZE)]
        self.spawn_on_next_turn = True
        self.legal_moves = ["left", "right", "up", "down", "quit"]


    #GRID_SIZE = 4           # expand this to be optional later and add 3x3 and 5x5
    #TARGET_SCORE = 2048
    # initialize N x N game grid
    # keep track of empty cells for spawning new blocks; initially all cells empty

    """
    Checks if the target score has been attained. If yes, the game is won.
    """
    def check_win(self):
        for row in self.game_grid:
            if self.TARGET_SCORE in row:
                self.game_won = True
                print("You win! :D  You can keep playing though!")
                break 

    """
    This should only be run when the board is FULL, otherwise there are always
    available moves.
    Checks if every game state resulting from a future move is the same.
    If that is the case, the game is lost.
    If it's possible to make a move that changes the game state, we can keep going.
    """
    def check_loss(self):
        if  GameLogic.moves.move_left(self.game_grid) == self.game_grid and \
            GameLogic.moves.move_right(self.game_grid) == self.game_grid and \
            GameLogic.moves.move_up(self.game_grid) == self.game_grid and \
            GameLogic.moves.move_down(self.game_grid) == self.game_grid:
                self.game_over = True
                print("You lose!")
                sys.exit()

    """
    Creates a new tile in an empty cell after a legal move.
    """
    def spawn_tile(self):
        if random.random() > 0.9:
            #10% probability to spawn a 4
            val = 4
        else:   
            val = 2

        # retrieve a random cell from the list of empty cells, and put the new tile there
        row, col = self.empty_cells[random.randrange(len(self.empty_cells))] 
        self.game_grid[row][col] = val

    def turn(self, move):

        self.spawn_on_next_turn = True
        if move == "left" and self.game_grid != GameLogic.moves.move_left(self.game_grid):
            self.game_grid = GameLogic.moves.move_left(self.game_grid)
        elif move == "right" and self.game_grid != GameLogic.moves.move_right(self.game_grid):
            self.game_grid = GameLogic.moves.move_right(self.game_grid)
        elif move == "up" and self.game_grid != GameLogic.moves.move_up(self.game_grid):
            self.game_grid = GameLogic.moves.move_up(self.game_grid)
        elif move == "down" and self.game_grid != GameLogic.moves.move_down(self.game_grid):
            self.game_grid = GameLogic.moves.move_down(self.game_grid)
        elif move == "quit":  #quit
            sys.exit()
        else:   # if the move has no effect, then don't spawn a new tile
            self.spawn_on_next_turn = False
            print("This move is DANGEROUS AND ILLEGAL")

        # update the list of empty cells
        for row in range(self.GRID_SIZE):
            for col in range(self.GRID_SIZE):
                if self.game_grid[row][col] == 0 and (row, col) not in self.empty_cells:
                    self.empty_cells.append((row, col))
                elif self.game_grid[row][col] != 0 and (row, col) in self.empty_cells:
                    self.empty_cells.remove((row, col))
        
        if self.spawn_on_next_turn:
            self.spawn_tile()

        # draw here
        for row in self.game_grid:
            print(row)  #placeholder
        print('*****')

        if(len(self.empty_cells) == 0): 
            self.check_loss()

        self.check_win()