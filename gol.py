"""Play Conway's Game of Life."""

import curses
import time


class GOL(object):
    """A gameboard for Conway's Game of Life."""

    def __init__(self,x,y):
        """Initiate The Gameboard."""
        self.hasrun = False
        self.original_board = None
        self.iteration = 0
        self.isblank = None
        self.ischanged = None
        self.rows = y
        self.columns = x
        self.new_board = None
        self.stdscr = None
        self.board = []
        for i in range(y):
            self.board.append([0 for j in range(x)])

    def set_square(self, x, y):
        """Set square (x,y) to 1."""
        self.board[y][x] = 1

    def add_structure(self, struct, xoffset, yoffset):
        """Add the matrix 'struct' to the gameboard at (xoffset,yoffset).

        This will overwrite all other structures.
        """
        for y, row in enumerate(struct):

            for x, square in enumerate(row):
                if square == 1:
                    self.board[y+yoffset][x+xoffset] = 1
                else:
                    self.board[y+yoffset][x+xoffset] = 0

    def initilize_screen(self):

        self.stdscr = curses.initscr()
        curses.noecho()

    def end_screen(self):
        curses.echo()
        curses.endwin()

    def print_board(self):
        self.stdscr.clear()

        for y, row in enumerate(self.board):

            for x, square in enumerate(row):
                if square == 1:
                    self.stdscr.addstr(y, x*2, '*')
                else:
                    self.stdscr.addstr(y, x*2, ' ')

        self.stdscr.refresh()

    def update_board(self):
        if self.hasrun is False:
            self.original_board = self.board
        # Generate New board
        self.new_board = []
        blank = True
        changed = False
        for i in range(self.rows):
            self.new_board.append([0 for j in range(self.columns)])
            # For each square, find current state and number of neighbours
        for row in range(self.rows):
            for column in range(self.columns):
                current_state = self.board[row][column]
                neighbours = self._calculate_neighbours(column, row)

                # Conway's Rules!
                if current_state == 1 and neighbours < 2:
                    self.new_board[row][column] = 0
                    changed = True
                elif current_state == 1 and neighbours > 1 and neighbours < 4:
                    self.new_board[row][column] = 1
                    blank = False

                elif current_state == 1 and neighbours > 3:
                    self.new_board[row][column] = 0
                    changed = True
                elif current_state == 0 and neighbours == 3:
                    self.new_board[row][column] = 1
                    blank = False
                    changed = True
        self.board = self.new_board
        self.new_board = None
        self.iteration += 1
        if blank is True:
            self.isblank = True
        else:
            self.isblank = False
        if changed is False:
            self.ischanged = False
        else:
            self.ischanged = True
        self.hasrun = True

    def reset(self):
        self.board = self.original_board
        self.hasrun = False

    def run(self, pause, rounds):
        self.initilize_screen()
        self.print_board()
        time.sleep(pause)
        for round in range(rounds):
            self.update_board()
            self.print_board()
            time.sleep(pause)
        self.end_screen()

    def _calculate_neighbours(self, x, y):
        neighbours = 0
        try:
            if self.board[y-1][x] == 1 and y >= 1:
                neighbours += 1
        except IndexError:
            pass
        try:
            if self.board[y+1][x] == 1:
                neighbours += 1
        except IndexError:
            pass
        try:
            if self.board[y][x-1] == 1 and x >= 1:
                neighbours += 1
        except IndexError:
            pass
        try:
            if self.board[y][x+1] == 1:
                neighbours += 1
        except IndexError:
            pass
        try:
            if self.board[y - 1][x - 1] == 1 and y >= 1 and x >= 1:
                neighbours += 1
        except IndexError:
            pass
        try:
            if self.board[y-1][x+1] == 1 and y >= 1:
                neighbours += 1
        except IndexError:
            pass
        try:
            if self.board[y+1][x-1] == 1 and x >= 0:
                neighbours += 1
        except IndexError:
            pass
        try:
            if self.board[y+1][x+1] == 1:
                neighbours += 1
        except IndexError:
            pass
        return neighbours

    def test(self, rounds, failisblank=True, failnochange=False):
        passed = True
        for round in range(rounds):
            self.update_board()
            if failisblank is True and self.isblank is True:
                passed = False
                break
            if failnochange is True and self.ischanged is False:
                passed = False
                break
        return passed



def test_iterations(structuresize, gridsize, rounds, failisblank=True, \
    failnochange=False):
    '''
    Generates a list of all possible structures based on structuresize (a sqare grid)
    tests them for rounds, and returns the ones that pass
    '''
    teststructures = generate_binary_grid(structuresize)
    results = []
    for structure in teststructures:
        game = GOL(gridsize, gridsize)
        game.add_structure(structure, xoffset=int(gridsize/2), yoffset=int(gridsize/2))
        result = game.test(rounds, failisblank=failisblank, failnochange=failnochange)

        if result is True:
            results.append(structure)
    return results


def test_list(struclist, gridsize, rounds, failisblank=True, failnochange=False):
    """
    Take a list of structures, places each of them on the
    gameboard in the lower right quadrent, and tests it for x number of rounds.
    Returns a list of strucures that have passed
    """
    results = []
    for structure in struclist:
        game = GOL(gridsize, gridsize)
        game.add_structure(structure, xoffset=int(gridsize/2), yoffset=int(gridsize/2))
        result = game.test(rounds, failisblank=failisblank, failnochange=failnochange)
        if result is True:
            results.append(structure)
    return results


def rotate_structure(structure):
    """Rotates a structre clockwise once."""
    pass


def generate_binary_grid(gridsize):
    """
    Generate all possible iterations of a square binary matrix. Gridsize is
    the size of the side of the square - eg. 3 generates all 3x3 binary matrices.
    """
    results = []

    grid = [0 for x in range(gridsize**2)]

    for x in range((2**(gridsize)**2)-1):
        grid[0] += 1

        for index, entry in enumerate(grid):

            if entry > 1:
                grid[index] = 0
                grid[index+1] += 1
            else:
                break
        new_grid = [grid[i:i+gridsize] for i in range(0, len(grid), gridsize)]
        results.append(new_grid)
    return(results)
