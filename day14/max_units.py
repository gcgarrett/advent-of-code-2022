import logging

# configure the logging level
logging.basicConfig(level=logging.INFO)

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

# figure out what the minimum X, maximum X, and maximum Y coordinates are
minX = 1000
maxX = 0
minY = 0 # we know the sand falls from 500,0
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
    logging.debug(coordinates)

    prevCoordinates = None

    # loop through the coordinates to parse out the lines of rock
    for i, coordinate in enumerate(coordinates):
        # split and map the coordinate string into a tuple of ints
        points = tuple(map(int, coordinate.split(',')))
        pointX = points[0]
        pointY = points[1]

        if pointX > maxX:
            # set new maximum x-coordinate
            maxX = pointX

        if pointX < minX:
            # set new minimum x-coordinate
            minX = pointX

        if pointY > maxY:
            # set new maximum y-coordinate
            maxY = pointY

        currentCoordinates = points

        if prevCoordinates is not None:
            # create a new line from the previous and current coordinates
            lines.append(Line(prevCoordinates, currentCoordinates))

        prevCoordinates = currentCoordinates

logging.debug(f'minX: {minX}; maxX: {maxX}; minY: {minY}; maxY: {maxY}')

# create a grid of empty spaces (represented by '.') to fill in the rows and
# columns
grid = [['.' for x in range((maxX - minX) + 1)] for y in range((maxY - minY) + 1)]

# signify the sand source with the '+' character
grid[0][500 - minX] = '+'

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

    # treat minX as 0 in our grid, so subtract minX from the start and end
    # x-coordinates
    startX = startX - minX
    endX = endX - minX

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
    print(' '.join(row))

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
    x = 500 - minX
    y = 0

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
                break
        except IndexError:
            # the grain of sand has fallen into the void
            sandFalling = False
            break

# prints the resulting cave state with sand and rock structures
print('Resulting state')
for row in grid:
    print(' '.join(row))

logging.info(f'Sand units: {sandCount}')
