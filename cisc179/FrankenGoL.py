# This is my GoL updated from reviewing ChatGPT and also implementing an
# idea I had to speed things up.  The idea is to, as I calculate each new
# generation, I will build a "living" list with with coordinates of every
# live cell.  At each update, I need only iterate through that list, not
# the entire array looking for live cells.
#


# My code starts here
from random import randint
import tkinter as tk
import numpy as np

class Universe():
    # Universe expects a tuple/list with x,y dimensions
    # Class variables
    dumpOutput = " *"   # Use to print out array without using if/then...
    def __new__(cls, size: tuple, cellsize):
        # Verify we are getting the universe we expect...
        if not ((type(size) is tuple) or (type(size) is list)):
            raise TypeError('Expected tuple or list.')
        elif len(size) != 2:
            raise ValueError('There can be only two dimensions.')

        # Now we know we have a list or tuple with two items
        # Next, verify they are integers.
        if not (isinstance(size[0], int) and isinstance(size[1], int) ):
            raise ValueError('Arguments must be integers.')

        # Now we know we have valid constructor parameters.
        return super(Universe, cls).__new__(cls)

    def __init__(self, size, cellsize):
        self.universeSize = size
        self.cellArray = list()
        self.countArray = list()
        self.livingArray = list()

        # This will set both arrays to proper dimensions.
        self.cellArray = self.countArray = self.resetCount()

        # This is from ChatGPT-3
        self.cellsize = cellsize
        self.grid_width = size[0]
        self.grid_height = size[1]

        xpixels = self.cellsize * size[0]
        ypixels = self.cellsize * size[1]

        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root, width=xpixels, height=ypixels)
        self.canvas.pack()

        # I think this has to be here as when I instantiate the class, it creates the
        # initial "trigger" to get into the update/go loop.
        self.root.after(2000, self.go)

    def resetCount(self):
        self.countArray = [[0 for y in range(self.y)] for x in range(self.x)]
        return self.countArray

    def getX(self):
        return self.universeSize[0]    # One way...

    def getY(self):
        return self.universeSize[1]    # One way...

    def getCell(self, x, y):
        return self.cellArray[x][y]

    def setCell(self, x, y, value):
        if not (value == 1 or value == 0):
            raise ValueError("A cell can only be on (1) or off (0).  We aren't quantum cats!")
        self.cellArray[x][y] = value

    x = property(getX)
    y = property(getY)

    def dumpCount(self):
        boundary = "+" + "-" * self.x + "+"
        print(boundary)
        for y in range(self.y):
            print("|", end="")
            for x in range(self.x):
                print(self.countArray[x][y], end="")
            print("|")

        print(boundary)

    def dumpLiving(self):
        row = 0
        for t in self.livingArray:
            print(t, end="")
            if row != t[1]:
                row = t[1]
                print()

        print()

    def dumpUniverse(self):
        boundary = "+" + "-" * self.x + "+"
        print(boundary)
        for y in range(self.y):
            print("|", end="")
            for x in range(self.x):
                print(Universe.dumpOutput[self.cellArray[x][y]], end="")
            print("|")

        print(boundary)

    def populate_grid(self, density):
        num_cells = int(self.x * self.y * density)
        indices = np.random.choice(self.x * self.y, num_cells, replace=False)
        for idx in indices:
            x, y = np.unravel_index(idx, (self.x, self.y))
            self.setCell(x, y, 1)
            self.livingArray.append((x, y))

    # This is the old-genesis.  ChatGPT provided a better genesys.
    def genisys(self):
        for y in range(self.y):
            for x in range(self.x):
                if randint(0, 1):
                    self.setCell(x, y, 1)
                    self.livingArray.append((x,y))

    def updateNeighbors(self, x, y):
        #print("Notifying neighbors of {},{}...".format(x, y))
        count = self.countArray
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                if x+dx in range(0, self.x) and y+dy in range(0, self.y) and (abs(dx)+abs(dy) != 0):
                    #print("dx, dy: ({}, {}), x, y: ({}, {})".format(dx, dy, x+dx, y+dy))
                    count[x+dx][y+dy] += 1

    # testByLoop iterates through grid and updates a counting array when it
    # finds a live sell
    def testByLoop(self):
        for y in range(self.y):
            for x in range(self.x):
                if self.cellArray[x][y]:
                    self.updateNeighbors(x, y)

    # testByList uses the living list array to update the counting array
    def testByList(self):
        for x, y in self.livingArray:
            self.updateNeighbors(x, y)

    def go(self):
        self.resetCount()
        #self.testByLoop()
        self.testByList()
        self.livingArray = list()

        for y in range(self.y):
            for x in range(self.x):
                n = self.countArray[x][y]
                if n<2 or n>3:
                    self.setCell(x, y, 0)

                # For 2 neighbors, cell state unchanged.  So add cell to liveArray if it is already alive
                elif n == 2 and self.cellArray[x][y]:
                    self.livingArray.append((x, y))

                # For 3 neighbors, cell is alive
                elif n == 3:
                    self.setCell(x, y, 1)
                    self.livingArray.append((x, y))

        self.draw_cells()
        self.root.after(1, self.go)

    def draw_cells(self):
        self.canvas.delete("all")
        for y in range(self.y):
            for x in range(self.x):
                if self.cellArray[x][y]:
                    xgrid = x * self.cellsize
                    ygrid = y * self.cellsize
                    self.canvas.create_rectangle(
                        xgrid,
                        ygrid,
                        xgrid + self.cellsize,
                        ygrid + self.cellsize,
                        fill="black",
                        outline="white",
                    )

    def run(self):
        self.draw_cells()
        self.root.mainloop()


universeSize = [200, 200]
U = Universe(universeSize, 5)
print("Universe spawned: ", U.x, U.y)
print("Turning on the light...")
#U.genisys()
U.populate_grid(0.5)
#U.dumpLiving()
#U.dumpUniverse()
U.run()

