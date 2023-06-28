import getopt
import logging
import sys

# configure the logging level
logging.basicConfig(level=logging.INFO)

HAS_FLOOR = False
MAX_X = 1000
SAND_SOURCE = (500, 0)

# command line arguments
#   -f, --floor: configures the cave to include a floor
opts, args = getopt.getopt(sys.argv[1:], 'f', ['floor'])

for opt, arg in opts:
    if opt in ('-f', '--floor'):
        HAS_FLOOR = True

# open the puzzle input file
f = open('./puzzle_input.txt')

lines = []

# Class definition for a Line of rock. `start` is the start coordinate and
# `end` is the end coordinate
class Line:
    def __init__(self, start, end):
        self.start = start
        self.end = end
    def __str__(self):
        return f'{self.start} -> {self.end}'

# figure out what the maximum Y coordinates are
maxY = 0

# parse the puzzle input
while(True):
    # read next line
    line = f.readline()

    # EOF, break out of loop
    if line == '':
        break

    # get the list of coordinates on the input line
    coordinates = line.strip().split(' -> ')

    prevCoordinates = None

    # loop through the coordinates to parse out the lines of rock
    for i, coordinate in enumerate(coordinates):
        # split and map the coordinate string into a tuple of ints
        points = tuple(map(int, coordinate.split(',')))
        pointX = points[0]
        pointY = points[1]

        if pointY > maxY:
            # set new maximum y-coordinate
            maxY = pointY

        currentCoordinates = points

        if prevCoordinates is not None:
            # create a new line from the previous and current coordinates
            lines.append(Line(prevCoordinates, currentCoordinates))

        prevCoordinates = currentCoordinates

logging.debug(f'maxY: {maxY}')

if HAS_FLOOR:
    # if the cave has a floor, add two to the maximum y-coordinate and add a
    # horizontal line to represent the cave floor
    maxY += 2
    lines.append(Line((0, maxY), (MAX_X, maxY)))

# create a grid of empty spaces (represented by '.') to fill in the rows and
# columns; add 1 as the coordinates are 0-based (e.g. if maxY is 9, then we
# require 10 rows to include the zeroth row along with 1 through 9).
grid = [['.' for x in range(MAX_X + 1)] for y in range(maxY + 1)]

# signify the sand source with the '+' character
grid[SAND_SOURCE[1]][SAND_SOURCE[0]] = '+'

# loop through the lines to add the rock lines to the grid
for l in lines:
    start = l.start
    end = l.end

    startX = start[0]
    startY = start[1]
    endX = end[0]
    endY = end[1]

    if start[0] > end[0]:
        # make sure the start x comes before the end x
        startX = end[0]
        endX = start[0]
    elif start[1] > end[1]:
        # make sure the start y comes before the end y
        startY = end[1]
        endY = start[1]

    logging.debug(f'startX: {startX}; startY: {startY}; endX: {endX}; endY: {endY}')

    if startX != endX:
        # there's a difference in the start and end x-coordinates, so create a
        # horizontal line
        for x in range(abs(startX - endX) + 1):
            grid[startY][startX + x] = '#'
    elif startY != endY:
        # there's a difference in the start and end y-coordinates, so create a
        # vertical line
        for y in range(abs(startY - endY)):
            grid[startY + y][startX] = '#'

# prints the initial cave state with rock structures
print('Initial state')
for row in grid:
    print(''.join(row))

# method to validate that the given coordinate is empty. An empty space is
# indicated by a '.' character.
#
# parameters
#   x (Integer): The x-coordinate
#   y (Integer): The y-coordinate
#
# returns
#   (Boolean):   True if the given coordinate is empty; False if not
def validateMove(x, y):
    return grid[y][x] == '.'

# simulate sand falling into the cave
sandFalling = True
sandCount = 0

while sandFalling:
    # sand falls from coordinate 500,0, but we are truncating the space to
    # start with minX as 0, so all x-coordinates need to subtract minX
    x = SAND_SOURCE[0]
    y = SAND_SOURCE[1]

    while(True):
        try:
            # first try falling down
            if validateMove(x, y + 1):
                y += 1
            # next try falling to the left
            elif validateMove(x - 1, y + 1):
                x -= 1
                y += 1
            # next try falling to the right
            elif validateMove(x + 1, y + 1):
                x += 1
                y += 1
            # the grain of sand has come to rest
            else:
                grid[y][x] = 'o'
                sandCount += 1
                if HAS_FLOOR and x == SAND_SOURCE[0] and y == SAND_SOURCE[1]:
                    # if the cave has a floor, then we have filled up the cave
                    # to the sand source
                    sandFalling = False
                break
        except IndexError:
            # the grain of sand has fallen into the void
            sandFalling = False
            break

# prints the resulting cave state with sand and rock structures
print('Resulting state')
for row in grid:
    print(''.join(row))

logging.info(f'Sand units: {sandCount}')
