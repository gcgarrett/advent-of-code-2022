import getopt
import logging
import sys

# configure the logging level
logging.basicConfig(level=logging.INFO)

START_ELEVATIONS = ['S']

# command line arguments
#   -s, --start:    the start elevation characters comma separated
#                   (defaults to 'S')
opts, args = getopt.getopt(sys.argv[1:], 's:', ['start='])

for opt, arg in opts:
    if opt in ('-s', '--start'):
        START_ELEVATIONS = arg.split(',')

logging.debug(f'Start elevations: {", ".join(START_ELEVATIONS)}')

# open the puzzle input file
f = open('./puzzle_input.txt')

# grid of elevations
grid = []

# helper method to calculate the shortest path from then given square to the
# end elevation marked by 'E' using a BFS algorithm.
#
# parameters
#   startSquare (Square): The Square object to begin searching from
#
# returns
#   (Number):             The number of steps in the shortest path
def calculateShortestPathHelper(startSquare):
    # initialize the list of squares to visit with the start square
    squaresToVisit = [startSquare]
    # initialize the dictionary of visited coordinates
    visitedSquares = {}
    # initialize fewestSteps to sys.maxsize, so that if we do not find the end
    # square we return this large value instead
    fewestSteps = sys.maxsize

    # BFS loop until we find the end square denoted by the character 'E'
    while len(squaresToVisit) > 0:
        # take the first square in the list of squares to visit
        square = squaresToVisit.pop(0)

        # if we've already visited this square, ignore it and go to the next
        # square to visit
        if square.coordinates in visitedSquares:
            continue

        # mark square as visited
        visitedSquares[square.coordinates] = True

        # if we are visting the end square, calculate the depth of that square
        # to determine how many steps we took to get there and break out of the
        # loop
        if square.elevation == 'E':
            fewestSteps = square.calculateDepth()
            break

        # find the neighbors of this square
        neighbors = findNeighbors(square.coordinates)

        for neighbor in neighbors:
            square.addNeighbor(neighbor)

        # add neighbors to the list of squares to visit
        squaresToVisit.extend(square.neighbors)

    return fewestSteps

# method to calculate the shortest path from then given coordinates to the end
# elevation marked by 'E'.
#
# parameters
#   startCoordinates (Tuple): The tuple of the row and column in the grid
#
# returns
#   (Number):                 The number of steps in the shortest path
def calculateShortestPath(startCoordinates):
    # get the start square elevation
    startElevation = getElevation(startCoordinates)
    # create a Square object with the starting elevation and coordinates
    startSquare = Square(None, startElevation, startCoordinates)
    
    return calculateShortestPathHelper(startSquare)

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

# helper method to find the starting coordinates for all of the elevations in
# the START_ELEVATIONS list
#
# returns
#   (Tuple): The tuple of the row and column in the grid
def findStartCoordinates():
    startCoordinates = []
    for row, columns in enumerate(grid):
        for col, elevation in enumerate(columns):
            if elevation in START_ELEVATIONS:
                startCoordinates.append((row, col))
    return startCoordinates

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

# helper method to convert an elevation character to an ordinal number. The
# elevation 'S' returns the ordinal value for 'a'. The elevation 'E' returns
# the ordinal value for 'z'.
#
# parameters
#   elevation (Character): The elevation character
#
# returns
#   (Integer):             The ordinal value for the elevation 
def getElevationAsOrdinal(elevation):
    match elevation:
        case 'S':
            elevation = 'a'
        case 'E':
            elevation = 'z'
    return ord(elevation)

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
        difference = getElevationAsOrdinal(nextElevation) - getElevationAsOrdinal(currentElevation)
        return difference <= 1

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
        while square.parent is not None:
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

startSquares = findStartCoordinates()

logging.info(f'Number of start squares: {len(startSquares)}')
logging.debug(startSquares)

# map the startSquares list into a list of shortest paths using the
# calculateShortPath function
shortestPaths = list(map(calculateShortestPath, startSquares))
# sort shortest paths in ascending order
shortestPaths.sort()

logging.debug(shortestPaths)
logging.info(f'Fewest steps: {shortestPaths[0]}')
