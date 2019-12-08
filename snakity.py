import curses
from random import randint, seed
from time import time


class Snakity:

    height = 30
    width = 60
    speed = 200
    length = 4
    powerup = ()
    run = True
    initial_dir = (1, 0)
    arrows = {ord('q'): (-1, 0), ord('d'): (1, 0), ord('z'): (0, -1), ord('s'): (0,1)}

    def __init__(self):
        self.snake = [(x+2, int(self.height/2)) for x in range(self.length)]
        self.dirv = self.initial_dir
        self.scr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        self.scr.keypad(True)
        self.scr = curses.newwin(self.height, self.width)
        self.scr.nodelay(1)
        self.sandbox = curses.newwin(self.height - 2, self.width, 1, 0)
        seed(time)

    def clean(self):
        curses.nocbreak()
        curses.echo()
        self.scr.keypad(False)
        curses.endwin()
    
    def displayScore(self):
        self.scr.addstr(0, 0, "Score: {}".format(self.length * 10))

    def displayBox(self):
        self.sandbox.box()

    def updatePowerup(self):
        tries = 0
        self.length += 1
        self.speed = int(0.95 * self.speed)
        while(self.powerup in self.snake) or tries == 0:
            self.powerup = (randint(1, self.width - 2), randint(2, self.height-3))
            tries += 1

    def displayPowerup(self):
        self.scr.addch(self.powerup[1], self.powerup[0], curses.ACS_DIAMOND)

    def isNewCellFree(self, newCell):
    # returns: 0:game over; 1:powerup; 2:continue
        if newCell in self.snake:
            return 0
        elif newCell[0] == 0 or newCell[0] == self.width - 1 or newCell[1] == 1 or newCell[1] == self.height - 2:
            return 0
        elif newCell == self.powerup:
            return 1
        return 2

    def updateSnake(self):
        newCell = (self.snake[-1][0] + self.dirv[0], self.snake[-1][1] + self.dirv[1])
        ret = self.isNewCellFree(newCell)
        if ret ==  0: # game over
            self.run = False
        elif ret == 1: # powerup
            self.updatePowerup()

        self.snake.append(newCell)
        if len(self.snake) > self.length:
            del self.snake[0]

    def displaySnake(self):
        for i,j in self.snake:
            self.scr.addch(j, i, "O")

    def clearSnakeTail(self):
        self.scr.addch(self.snake[0][1], self.snake[0][0], " ")

    def keyCheck(self):
        char = self.scr.getch()
        if char == 27: # KEY_ESC
            return False
        if char in self.arrows.keys():
            # no U-turn
            if self.arrows[char][0] != self.dirv[0] and self.arrows[char][1] != self.dirv[1]:
                self.dirv = self.arrows[char]
        return True
    
    def gameLoop(self):
        self.displayBox()
        self.updatePowerup()
        while(self.run):
            self.clearSnakeTail()
            self.updateSnake()
            self.displaySnake()
            self.displayPowerup()
            self.displayScore()
            if self.run:
                self.run = self.keyCheck()
                self.scr.refresh()
                self.sandbox.refresh()
            curses.napms(self.speed)


def main():
    game = Snakity()
    game.gameLoop()
    game.clean()
    exit()

if __name__ == "__main__":
    main()

