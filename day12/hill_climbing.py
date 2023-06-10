import logging
import sys

# configure the logging level
logging.basicConfig(level=logging.INFO)

# open the puzzle input file
f = open('./puzzle_input.txt')

# grid of elevations
grid = []
visitedSquares = {}

# helper method to return the elevation at the given coordinates.
#
# parameters
#   coordinates (Tuple): The tuple of the row and column in the grid
#
# returns
#   (Character):         The character representing the elevation
def getElevation(coordinates):
    row = coordinates[0]
    col = coordinates[1]
    return grid[row][col]

# helper method to return the neighbors of the given coordinates.
#
# parameters
#   coordinates (Tuple): The tuple of the row and column in the grid
# returns
#   (List):              The list of neighboring coordinates as tuples of row
#                        and column in the grid. Does not guarantee the given
#                        coordinates are inside the boundaries of the grid.
def findNeighbors(coordinates):
    row = coordinates[0]
    col = coordinates[1]
    left = (row, col - 1)
    up = (row - 1, col)
    right = (row, col + 1)
    down = (row + 1, col)
    return [left, up, right, down]

# helper method to find the starting coordinates, represented by elevation 'S'.
#
# returns
#   (Tuple): The tuple of the row and column in the grid
def findStart():
    for row, columns in enumerate(grid):
        for col, elevation in enumerate(columns):
            if elevation == 'S':
                return (row, col)

# helper method to validate that the given coordinates are within the
# boundaries of the grid. Coordinates are zero-based.
#
# parameters
#   coordinates (Tuple): The tuple of the row and column in the grid
#
# returns
#   (Boolean):           True if row is greater than equal to 0 and less than
#                        row length AND column is greater than equal to 0 and
#                        less than the column length, False otherwise
def validCoordinates(coordinates):
    row = coordinates[0]
    col = coordinates[1]

    if row >= 0 and row < len(grid):
        if col >= 0 and col < len(grid[row]):
            return True
    
    return False

# helper method to validate that there is a connection between neighboring
# coordinates. If the difference between the neighboring coordinate and the
# current coordinate elevations is 1 or less, there is a connection.
#
# parameters
#   nextCoordinates (Tuple):    The tuple of the row and column in the grid of
#                               the neighboring square
#   currentCoordinates (Tuple): The tuple of the row and column in the grid of
#                               the current square
# returns
#   (Boolean):                  True if a connection exists, False otherwise
def validEdge(nextCoordinates, currentCoordinates):
    if validCoordinates(nextCoordinates):
        currentElevation = getElevation(currentCoordinates)
        nextElevation = getElevation(nextCoordinates)

        if nextElevation == 'E':
            nextElevation = 'z'
        elif nextElevation == 'S':
            nextElevation = 'a'
        
        if currentElevation == 'S':
            currentElevation = 'a'
        
        return (ord(nextElevation) - ord(currentElevation)) <= 1

# Class definition for a Square in the grid. This helps us calculate the depth
# of the target Square later on.
class Square:
    def __init__(self, parent, elevation, coordinates):
        self.parent = parent
        self.elevation = elevation
        self.coordinates = coordinates
        self.neighbors = []
    def __str__(self):
        return f'{self.elevation} @ {self.coordinates}'
    def addNeighbor(self, coordinates):
        if validEdge(coordinates, self.coordinates):
            elevation = getElevation(coordinates)
            neighbor = Square(self, elevation, coordinates)
            self.neighbors.append(neighbor)
    def calculateDepth(self):
        depth = 0
        square = self
        while square.elevation != 'S':
            logging.debug(square)
            square = square.parent
            depth += 1
        return depth

# generate the grid of elevations from the puzzle input
while(True):
    # read next line
    line = f.readline()

    # EOF, break out of the loop
    if line == '':
        break
    
    line = line.strip()

    columns = []
    # convert string of elevations into list of elevations
    columns[:0] = line

    grid.append(columns)

logging.debug(f'Grid size: {len(grid) * len(grid[0])}')

# find the starting coordinates
startCoordinates = findStart()
# get the elevation of the starting coordinates
startElevation = getElevation(startCoordinates)
# create the starting square object
startSquare = Square(None, startElevation, startCoordinates)
# find neighbors of the start square
startNeighbors = findNeighbors(startCoordinates)

# add the neighbors to the start square
for neighbor in startNeighbors:
    startSquare.addNeighbor(neighbor)

logging.debug(f'Start square: {startSquare}')

# initialize list of squares to visit with start square
squares = [startSquare]
# initialize steps with the system maxsize value
steps = sys.maxsize

# BFS loop until we find the end square denoted by the character 'E'
while(True):
    # take the first square in the list of squares to visit
    square = squares.pop(0)

    logging.debug(f'Current square: {square}')

    # if we've already visited this square, ignore it and go to the next square
    # to visit
    if square.coordinates in visitedSquares:
        logging.debug('Visited!')
        continue

    # mark square as visited
    visitedSquares[square.coordinates] = True

    logging.debug(f'Visited squares: {len(visitedSquares)}')

    # if we are visting the end square, calculate the depth of that square to
    # determine how many steps we took to get here. else find the neighbors of
    # this square and add them to the list of squares to visit.
    if square.elevation == 'E':
        # calculate steps
        steps = square.calculateDepth()
        break
    else:
        neighbors = findNeighbors(square.coordinates)

        for neighbor in neighbors:
            square.addNeighbor(neighbor)

        squares.extend(square.neighbors)

logging.info(f'Fewest steps: {steps}')
