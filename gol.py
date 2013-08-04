"""
Any live cell with fewer than two live neighbours dies,
as if caused by under-population.

Any live cell with two or three live neighbours lives
on to the next generation.

Any live cell with more than three live neighbours dies,
as if by overcrowding.

Any dead cell with exactly three live neighbours becomes a live cell,
as if by reproduction.
"""

import copy
import curses
import random
import argparse
from time import sleep
from itertools import chain, product

class gol(object):

    def __init__(self, args):
        self.screen = curses.initscr()
        self.screen.keypad(1)
        self.screen.nodelay(1)
        curses.start_color()
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        self.grid = {}
        self.height, self.width = self.screen.getmaxyx()
        self.y_pad = 3
        self.x_pad = 2
        self.y_grid = self.height - self.y_pad
        self.x_grid = self.width - self.x_pad
        self.char = "*"
        self.rate = args.r
        self.generations = args.g
        curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
        self.win = curses.newwin(self.height, self.width, 0, 0)

    def __del__(self):
        self.win.clear()
        self.win.refresh()
        curses.echo()
        curses.endwin()

    def DrawHUD(self, n=0):
        """
        Draw information on population size and current generation
        """
        self.win.box()
        self.win.addstr(1, 2, "Game of Life")
        self.win.addstr(self.height - self.y_pad, self.x_pad, "Population: %i   " % len(self.grid))
        self.win.addstr(self.height - self.x_pad, self.x_pad, "Generation: %s" % n)
        return

    def DrawGrid(self):
        """
        Redraw the grid with the new generation
        """
        grid_cp = copy.copy(self.grid)
        active =  self.grid.keys()

        for cell in product(xrange(self.y_pad, self.y_grid), xrange(self.x_pad, self.x_grid)):
            n = self.CountNeighbours(cell)
            x, y = cell
            if cell in active:
                self.win.addch(x, y, self.char, curses.color_pair(self.grid[cell]))
                if n < 2 or n > 3:
                    del grid_cp[cell]
                else:
                    grid_cp[cell] = 1
            else:
                self.win.addch(x, y, ' ')
                if n == 3:
                    grid_cp[cell] = 2

        self.grid = grid_cp
        self.win.refresh()
        return

    def CountNeighbours(self, cell):
        """
        Return the number active neighbours within one positions away from cell
        """
        count = 0
        x, y = cell
        active =  self.grid.keys()

        for neighbour in product(xrange(x-1, x+2), xrange(y-1, y+2)):
            if neighbour in active and neighbour != cell:
                count += 1
        return count

    def Breed(self):
        """
        main loop iterating through generations, population should be
        initialised before calling Breed using RandomStart or TestStart
        """
        for i in xrange(1, self.generations + 1):
            if self.screen.getch() == ord('q'):
                break
            self.DrawHUD(i)
            self.DrawGrid()
            sleep(self.rate)
        return

    def RandomStart(self, n):
        """
        Initialise the game with n random points
        """
        for _ in xrange(0, n):
            ry = random.randint(self.y_pad, self.y_grid)
            rx = random.randint(self.x_pad, self.x_grid)
            self.grid[(ry, rx)] = 1

        # Draw initial generation
        self.DrawHUD()
        self.DrawGrid()
        sleep(self.rate)
        return

    def TestStart(self):
        """
        Initialise the game with a predefined set up where the behaviour is deterministic
        """
        blinker = [(4, 4), (4, 5),(4, 6)]
        toad = [(9, 5), (9, 6),(9, 7), (10, 4), (10, 5),(10, 6)]
        glider = [(4, 11), (5, 12), (6, 10), (6, 11), (6, 12)]

        for cell in chain(blinker, toad, glider):
            self.grid[cell] = 1

        # Draw initial generation
        self.DrawHUD()
        self.DrawGrid()
        sleep(self.rate)
        return


def main(args):
    game = gol(args)
    game.RandomStart(args.n)
    game.Breed()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-g", default=50, type=int, help="The number of generations")
    parser.add_argument("-r", default=0.02, type=float, help="The refresh rate")
    parser.add_argument("-n", default=300, type=int, help="The number of initial points")
    main(parser.parse_args())
