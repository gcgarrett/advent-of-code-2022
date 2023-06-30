import getopt
import logging
import operator
import re
import sys

# configure the logging level
logging.basicConfig(level=logging.INFO)

ROW = 10

# command line arguments
#   -r, --row: the row to test against, defaults to 10
opts, args = getopt.getopt(sys.argv[1:], 'r:', ['row='])

for opt, arg in opts:
    if opt in ('-r', '--row'):
        ROW = int(arg)

logging.debug(f'Row to test against: {ROW}')

# open the puzzle input file
f = open('./puzzle_input.txt')

# store beacons in a dictionary to ensure no duplicates. The dictionary uses
# the beacon coordinates tuple as a key, with the Beacon object being the value
beacons = {}
# store sensors in an array
sensors = []

# class representing coordinates
#
# instance variables
#   x (Integer): the x-coordinate
#   y (Integer): the y-coordinate
#
# methods
#   toTuple: method that returns coordinates as a tuple, (x, y)
class Coordinates:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __str__(self):
        return f'x={self.x}, y={self.y}'
    def toTuple(self):
        return (self.x, self.y)

# class representing a beacon
#
# instance variables
#   coordinates (Coordinates): the beacon coordinates
class Beacon:
    def __init__(self, coordinates):
        self.coordinates = coordinates
    def __str__(self):
        return f'Beacon is at {self.coordinates}'

# class representing a sensor
#
# instance variables
#   coordinates (Coordinates): the sensor coordinates
#   beacon (Beacon):           the sensor's closest beacon
#
# methods
#   calculateDistance:    method that calculates the sensor's Manhattan
#                         distance to its closest beacon
#   intersectionsWithRow: method to generate the list of coordinates that
#                         the sensor can see in the given row
class Sensor:
    def __init__(self, coordinates, beacon):
        self.coordinates = coordinates
        self.beacon = beacon
    def __str__(self):
        return f'Sensor at {self.coordinates}: closest beacon is at {self.beacon.coordinates}'
    def calculateDistance(self):
        sensorX = self.coordinates.x
        sensorY = self.coordinates.y
        beaconX = self.beacon.coordinates.x
        beaconY = self.beacon.coordinates.y
        xDistance = abs(sensorX - beaconX)
        yDistance = abs(sensorY - beaconY)
        return xDistance + yDistance
    def intersectionsWithRow(self, row):
        distance = self.calculateDistance()
        sensorX = self.coordinates.x
        sensorY = self.coordinates.y
        intersections = []
        yDistance = distance
        xDistance = 0
        xOp = operator.add
        yTestOp = None
        yDistanceOp = None
        stopOp = None

        logging.debug(f'Row: {row}; sensor y: {sensorY}')

        if row > sensorY:
            yTestOp = operator.add
            stopOp = operator.le
        else:
            yTestOp = operator.sub
            stopOp = operator.ge

        logging.debug(f'yTestOp: {yTestOp.__qualname__}; stopOp: {stopOp.__qualname__}')

        while stopOp(row, yTestOp(sensorY, yDistance)) and xDistance <= distance:
            currentRow = yTestOp(sensorY, yDistance)
            logging.debug(f'Current row: {currentRow}; stop op? {stopOp(row, currentRow)}')
            logging.debug(f'Y distance: {yDistance}; X distance: {xDistance}')
            if xDistance == 0:
                intersections.append((sensorX, row))
            else:
                intersections.append((sensorX + xDistance, row))
                intersections.append((sensorX - xDistance, row))
            yDistance -= 1
            xDistance += 1

        return intersections

# parse the puzzle input
while(True):
    # read next line
    line = f.readline()

    # EOF, break out of the loop
    if line == '':
        break
    
    line = line.strip()

    sensorX = 0
    sensorY = 0
    beaconX = 0
    beaconY = 0

    match = re.search(r'Sensor at x=(-?[0-9]+), y=(-?[0-9]+): closest beacon is at x=(-?[0-9]+), y=(-?[0-9]+)', line)

    if match:
        sensorX = int(match.group(1))
        sensorY = int(match.group(2))
        beaconX = int(match.group(3))
        beaconY = int(match.group(4))
        # create sensor coordinates
        sensorCoordinates = Coordinates(sensorX, sensorY)
        # create beacon coordinates
        beaconCoordinates = Coordinates(beaconX, beaconY)
        beaconTuple = beaconCoordinates.toTuple()
        beacon = None
        if beaconTuple in beacons:
            # if the beacon is already found in the beacon dictionary, use it
            beacon = beacons[beaconTuple]
        else:
            # beacon was not found in beacon dictionary, create a new instance
            # and add it to the dictionary
            beacon = Beacon(beaconCoordinates)
            beacons[beaconTuple] = beacon
        # create a new sensor instance and add to the list of sensors
        sensor = Sensor(sensorCoordinates, beacon)
        sensors.append(sensor)

logging.debug(f'Found {len(sensors)} sensors')

# use a set of intersection coordinates to remove duplicates
intersectionSet = None

for sensor in sensors:
    logging.debug(f'{sensor}; distance: {sensor.calculateDistance()}')
    sensorIntersections = sensor.intersectionsWithRow(ROW)
    logging.debug(f'Sensor intersections: {sensorIntersections}')

    if intersectionSet is None:
        # initialize set to the first sensor's intersections
        intersectionSet = set(sensorIntersections)
    else:
        # create a union set of existing intersections and new ones
        intersectionSet = intersectionSet | set(sensorIntersections)

logging.debug(len(intersectionSet))

# create a set of beacon coordinates
beaconSet = set(beacons.keys())

# remove beacon coordinates from intersection coordinate sets
intersectionSet = intersectionSet - beaconSet

logging.info(f'Positions that cannot contain a beacon: {len(intersectionSet)}')
