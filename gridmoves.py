import numpy as np


class Moves:

    ### MOVEMENT FUNCTIONS ###
    # Work by matrix manipulation
    # Makes copies of the game state in order to test moves -- could be optimized?
    # Although these are arrays of 16 elements and probably AT ABSOLUTE MOST 100.

    def move_left(self, grid):
        matrix = np.asarray(grid)
        for i in range(len(matrix)):
            matrix[i] = self.compress_list_and_pad(matrix[i], "left")
            matrix[i] = self.merge_left(matrix[i])
        return matrix.tolist()

    def move_right(self, grid):
        matrix = np.asarray(grid)
        for i in range(len(matrix)):
            matrix[i] = self.compress_list_and_pad(matrix[i], "right")
            matrix[i] = self.merge_right(matrix[i])
        return matrix.tolist()

    def move_up(self, grid):
        matrix = np.transpose(self.move_left(np.transpose(grid)))
        return matrix.tolist()        # this syntax is bc numpy works with optimized arrays and not regular lists

    def move_down(self, grid):
        matrix = np.transpose(self.move_right(np.transpose(grid)))
        return matrix.tolist()


    ### MOVEMENT HELPER FUNCTIONS
    # Compressing elements in lists

    """
    Takes a list as an argument.
    Removes all Nones and returns a list of the remaining elements.
    Order is preserved.

    This creates a new list, it's not in place. Could be a problem?
    """
    def compress_list(self, lst):
        shifted = []
        for elem in lst:
            if elem != 0:
                shifted.append(elem)

        return shifted

    """
    Takes a list, compresses its elements, and preserves the length by padding the
    list with 0. The elements are placed on the side of the list indicated by
    the argument shift_elems_to.

    Args:
        - lst: the list to be compressed
        - shift_elems_to: options 'left' or 'right' to indicate to which side the
        elements go, i.e. the padding goes on the other side.

    Returns a new list with the elements of the original list compressed and the
    extra space padded.
    """
    def compress_list_and_pad(self, lst, shift_elems_to):
        original_length = len(lst)
        lst = self.compress_list(lst)
        try:
            if len(lst) < original_length:
                if shift_elems_to.lower() == "left":
                    lst.extend([0]*(original_length - len(lst)))
                elif shift_elems_to.lower() == "right":
                    lst[:0] = [0]*(original_length - len(lst))
        except ValueError:
            print("You tried to shift the list in some illegal direction")

        return lst

    """
    Combines tiles with left adjacency taking precedence.
    Adjacent identical tiles are merged into one tile with twice the value.
    Returns a list with spaces between merged tiles removed, left-shifted.
    """
    def merge_left(self, lst):
        if len(lst) < 2: return lst 

        # Starting from the left side, checks every 2 adjacent elements for
        # equality; if they are equal, they are combined.
        # Bound of len-1 is EXCLUSIVE, so i+1 is at most len-1.
        for i in range(0, len(lst)-1):
            if lst[i] == lst[i+1] and lst[i] != 0:
                lst[i] = 2*lst[i]
                lst[i+1] = 0

        # get rid of remaining nones
        return self.compress_list_and_pad(lst, "left")

    """
    Combines tiles with right adjacency taking precedence.
    Adjacent identical tiles are merged into one tile with twice the value.
    Returns a list with spaces between merged tiles removed, right-shifted.
    """
    def merge_right(self, lst):
        if len(lst) < 2: return lst 

        # Starting from the right side, checks every 2 adjacent elements for
        # equality; if they are equal, they are combined
        # Bound of 0 is EXCLUSIVE, so i-1 is 0 at its smallest.
        for i in range(len(lst)-1, 0, -1):
            if lst[i] == lst[i-1] and lst[i] != 0:
                lst[i] = 2*lst[i]
                lst[i-1] = 0

        # get rid of remaining nones
        return self.compress_list_and_pad(lst, "right")
