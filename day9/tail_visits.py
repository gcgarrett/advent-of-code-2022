# open the puzzle input file
f = open('./puzzle_input.txt')

# global integers holding head and tail coordinates
headX = 0
headY = 0
tailX = 0
tailY = 0
# directory of tail visits, with the key being the tail coordinates represented
# as a comma separated string, and the value just being True
tailVisits = {}

# helper method to move the head one position in the given direction
# parameters.
#   direction (String): The letter indicating the direction to move; "U" is up,
#                       "D" is down, "R" is right, "L" is left
# returns
#   (nothing):          Modifies the global headX and headY variables
def moveHead(direction):
    # method modifies global copies of headX and headY
    global headX
    global headY

    if direction == "U":
        headY += 1
    elif direction == "D":
        headY -= 1
    elif direction == "R":
        headX += 1
    elif direction == "L":
        headX -= 1

# helper method to move the tail if necessary based on how far away it is from
# the head.
def moveTail():
    # method modifies global copies of tailX and tailY
    global tailX
    global tailY

    # calculate the difference between the head and tail positions
    diffX = headX - tailX
    diffY = headY - tailY

    # if the difference along the x-axis is greater than 1 or less than -1,
    # move the tail right if the difference is greater than 1 or down if less
    # than -1
    if diffX > 1:
        tailX += 1
    elif diffX < -1:
        tailX -= 1

    # if the difference along the x-axis is greater than 1 or less than -1
    # and the tail is not at the same y-coordinate as the head, move the tail
    # to match the head's y-coordinates (effectively this moves the tail
    # diagonally)
    if diffX > 1 or diffX < -1:
        if diffY > 0:
            tailY += 1
        elif diffY < 0:
            tailY -= 1

    # if the difference along the y-axis is greater than 1 or less than -1,
    # move the tail up if the difference is greater than 1 or down if less than
    # -1
    if diffY > 1:
        tailY += 1
    elif diffY < -1:
        tailY -= 1

    # if the difference along the y-axis is greater than 1 or less than -1
    # and the tail not at the same x-coordinate as the head, move the tail to
    # match the head's x-coordinates (effectively this moves the tail
    # diagonally)
    if diffY > 1 or diffY < -1:
        if diffX > 0:
            tailX += 1
        elif diffX < 0:
            tailX -= 1

# helper method to record that the tail has visited its current position.
# creates a key of the tail's x and y coordinates as a comma separated string
# so that if a position is visited twice it only gets counted once.
def recordTailVisit():
    key = str(tailX) + "," + str(tailY)
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

    while moveCount < positions:
        # move head
        moveHead(direction)
        # move tail (if necessary)
        moveTail()
        # record the tail visit
        recordTailVisit()
        moveCount += 1

print("Tail visits")
print(len(tailVisits))
