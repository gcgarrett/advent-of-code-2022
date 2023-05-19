import getopt
import logging
import sys

logging.basicConfig(level=logging.WARNING)

# open the puzzle input file
f = open('./puzzle_input.txt')

class Coordinate:
    def __init__(self):
        self.x = 0
        self.y = 0
    def __str__(self):
        return f'{self.x},{self.y}'
    def incX(self):
        self.x += 1
    def decX(self):
        self.x -= 1
    def incY(self):
        self.y += 1
    def decY(self):
        self.y -= 1

class Node:
    def __init__(self, index, prev = None):
        self.coordinate = Coordinate()
        self.index = index
        self.prev = prev
        self.next = None
    def __str__(self):
        return f'{self.index}:{self.coordinate}'
    def setNext(self, node):
        self.next = node

class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
    def __iter__(self):
        return LinkedListIter(self)
    def __str__(self):
        if self.head is None:
            return "(empty)"
        else:
            llStr = ""
            for node in self:
                llStr += f'{node.coordinate}->'
            return llStr
    def add(self, index):
        if self.head is None:
            node = Node(index)
            self.head = node
            self.tail = node
        else:
            node = Node(index, self.tail)
            self.tail.setNext(node)
            self.tail = node

class LinkedListIter:
    def __init__(self, linkedList):
        self.currentNode = linkedList.head
    def __iter__(self):
        return self
    def __next__(self):
        if self.currentNode is not None:
            node = self.currentNode
            self.currentNode = self.currentNode.next
            return node
        raise StopIteration

# the default number of knots in the rope
ROPE_KNOTS = 2

opts, args = getopt.getopt(sys.argv[1:], "k:", ["knots="])

for opt, arg in opts:
    if opt in ("-k", "--knots"):
        # set number of knots in the rope based on command line input
        ROPE_KNOTS = int(arg)
# create linked list of the knots
knots = LinkedList()
# directory of tail visits, with the key being the tail coordinates represented
# as a comma separated string, and the value just being True
tailVisits = {}

knotIndex = 0

for i in range(ROPE_KNOTS):
    knots.add(i)

# helper method to move the head one position in the given direction
# parameters.
#   node      (Node):   The head node
#   direction (String): The letter indicating the direction to move; "U" is up,
#                       "D" is down, "R" is right, "L" is left
# returns
#   (nothing):          Modifies the head node x and y values
def moveHead(node, direction):
    headCoordinate = node.coordinate

    if direction == "U":
        headCoordinate.incY()
    elif direction == "D":
        headCoordinate.decY()
    elif direction == "R":
        headCoordinate.incX()
    elif direction == "L":
        headCoordinate.decX()

# helper method to move a node if necessary based on how far away it is from
# the previous node.
def moveNode(node):
    nodeCoordinate = node.coordinate
    prevNode = node.prev
    prevCoordinate = prevNode.coordinate

    # calculate the difference between the head and tail positions
    diffX = prevCoordinate.x - nodeCoordinate.x
    diffY = prevCoordinate.y - nodeCoordinate.y
    logging.debug(f'x: {diffX}, y: {diffY}')

    if diffX > 1 or diffX < -1:
        # if the difference along the x-axis is greater than 1 or less than -1,
        # move the node right if the difference is greater than 1 or down if less
        # than -1
        if diffX > 1:
            nodeCoordinate.incX()
        elif diffX < -1:
            nodeCoordinate.decX()

        # if the difference along the x-axis is greater than 1 or less than -1
        # and the node is not at the same y-coordinate as the previous node, move
        # the node to match the previous node's y-coordinates (effectively this
        # moves the node diagonally)
        if diffY > 0:
            nodeCoordinate.incY()
        elif diffY < 0:
            nodeCoordinate.decY()

    elif diffY > 1 or diffY < -1:
        # if the difference along the y-axis is greater than 1 or less than -1,
        # move the node up if the difference is greater than 1 or down if less than
        # -1
        if diffY > 1:
            nodeCoordinate.incY()
        elif diffY < -1:
            nodeCoordinate.decY()

        # if the difference along the y-axis is greater than 1 or less than -1
        # and the node not at the same x-coordinate as the previous node, move the
        # node to match the previous node's x-coordinates (effectively this moves
        # the node diagonally)
        if diffX > 0:
            nodeCoordinate.incX()
        elif diffX < 0:
            nodeCoordinate.decX()

# helper method to record that the tail has visited its current position.
# creates a key of the tail's x and y coordinates as a comma separated string
# so that if a position is visited twice it only gets counted once.
def recordTailVisit():
    key = f'{knots.tail.coordinate}'
    tailVisits[key] = True

# record starting position as visit for tail
recordTailVisit()

# loop through the input file
while(True):
    # read next line
    line = f.readline()

    # EOF, break out of the loop
    if line == "":
        break

    # split line on space, which separates the direction from the number of
    # positions to move
    move = line.strip().split(" ")
    direction = move[0]
    # convert number of positions to move to an integer
    positions = int(move[1])
    moveCount = 0

    # initial state
    logging.info(knots)

    while moveCount < positions:
        for node in knots:
            if node.prev is None:
                # move head
                moveHead(node, direction)
            else:
                # move other nodes (if necessary)
                moveNode(node)
        # record the tail visit
        recordTailVisit()
        logging.info(knots)
        moveCount += 1

print("Tail visits")
print(len(tailVisits))
