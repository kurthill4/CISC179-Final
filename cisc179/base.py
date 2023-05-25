"""
cisc179 base module.

This is the principal module of the cisc179 project.
here you put your main classes and objects.

Be creative! do whatever you want!

If you want to replace this with a Flask application run:

    $ make init

and then choose `flask` as template.
"""


# My code starts here
import os.path
from random import randint

###############################################################
# This was a test on aborting the creation of an object...
class File():
    # Class variables go here

    def __new__(cls, filepath):
        if os.path.exists(filepath):
            return super(File, cls).__new__(cls)
        else:
            raise ValueError

    def __init__(self, filepath):
        self.filepath = filepath
        self.filesize = 0
        self.filehash = ""
###############################################################


class Universe():
    # Universe expects a tuple/list with x,y dimensions
    # Class variables
    dumpOutput = " *"   # Use to print out array without using if/then...
    def __new__(cls, size: tuple):
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

    def __init__(self, size):
        self.universeSize = size
        row = list()
        self.cellArray = list()
        cell = [0, 0]

        self.cellArray = [[0 for y in range(size[1])] for x in range(size[0])]
        self.countArray = [[0 for y in range(size[1])] for x in range(size[0])]

        print(len(self.cellArray))
        print(len(self.cellArray[0]))

    def resetCount(self):
        self.countArray = [[0 for y in range(self.y)] for x in range(self.x)]
        return self.countArray

    def getX(self):
        x = self.universeSize[0]    # One way...
        #x = len(self.cellArray)     # Another way...
        return x

    def getY(self):
        y = self.universeSize[1]    # One way...
        #y = len(self.cellArray[0])     # Another way...
        return y

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


    def dumpUniverse(self):
        boundary = "+" + "-" * self.x + "+"
        print(boundary)
        for y in range(self.y):
            print("|", end="")
            for x in range(self.x):
                print(Universe.dumpOutput[self.cellArray[x][y]], end="")
            print("|")

        print(boundary)


    def genisys(self):
        for y in range(self.y):
            for x in range(self.x):
                self.setCell(x, y, randint(0, 1))


    def updateNeighbors(self, x, y):
        #print("Notifying neighbors of {},{}...".format(x, y))
        count = self.countArray
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                if x+dx in range(0, self.x) and y+dy in range(0, self.y) and (abs(dx)+abs(dy) != 0):
                    #print("dx, dy: ({}, {}), x, y: ({}, {})".format(dx, dy, x+dx, y+dy))
                    count[x+dx][y+dy] += 1


    def go(self):
        self.resetCount()
        for y in range(self.y):
            for x in range(self.x):
                if self.cellArray[x][y]:
                    self.updateNeighbors(x, y)

        for y in range(self.y):
            for x in range(self.x):
                n = self.countArray[x][y]
                if n<2 or n>3:
                    self.setCell(x, y, 0)
                elif n == 3:
                    self.setCell(x, y, 1)


universeSize = [25, 15]
U = Universe(universeSize)
print("Universe spawned: ", U.x, U.y)
print("Turning on the light...")
U.genisys()

for i in range(0, 10):
    U.dumpUniverse()
    U.go()
