import logging

logging.basicConfig(level=logging.WARNING)

# open the puzzle input file
f = open('./puzzle_input.txt')

# cycles are not zero-based
cycleCount = 1
# initialize register x with value 1
registerX = 1
# list of pixels
pixels = []

# helper method to draw a pixel to the screen. If the sprite is visible, draw
# a pixel. The sprite is 3 pixels wide, with the value in register x being the
# midpoint of the sprite. If the CRT is currently drawing within the width of
# the sprite, then a # is drawn to the screen. Otherwise a . is drawn.
def drawPixel():
    # the left-most pixel is position 0, the right-most is position 39. since
    # the cycle count is one-based, subtract 1 and mod the result with 40 to
    # give us the CRT position
    pixelX = (cycleCount - 1) % 40

    logging.debug(f'Pixel: {pixelX}; register: {registerX}')

    # bounds checking if the CRT position is within the sprite
    if pixelX >= registerX - 1 and pixelX <= registerX + 1:
        pixels.append("#")
    else:
        pixels.append(".")

# helper method to run a cycle. Draws a pixel first, then increments the cycle
# count.
#
# returns
#   (nothing): Increments the global cycle count by 1
def cycle():
    global cycleCount
    # draw the current pixel
    drawPixel()
    # increment count
    cycleCount += 1

# helper method to add the given amount to the value in register x. Waits two
# cycles before adding the value of amount to the value in register x.
#
# parameters
#   amount (Integer): The amount to add to the value in register x
#
# returns
#   (nothing):        Modifies the global value in register x
def addX(amount):
    global registerX
    cycle()
    cycle()
    registerX += amount

# helper method to perform a noop action. Waits 1 cycle then does nothing.
def noop():
    cycle()

# loop through the input file
while(True):
    # read next line
    line = f.readline()

    # EOF, break out of the loop
    if line == "":
        break

    logging.debug(line.strip())

    # split the line on the space; in the case of the add command, grab the
    # amount to add in the second index
    tokens = line.strip().split(" ")
    command = tokens[0]
    amount = 0

    if len(tokens) == 2:
        amount = int(tokens[1])

    match command:
        case "addx":
            addX(amount)
        case "noop":
            noop()

# print the resulting pixels
for row in range(6):
    # pixel start is row times 40 (zero-based)
    pixelStart = row * 40
    # pixel end is pixel start + 40 (exclusive)
    pixelEnd = pixelStart + 40
    print("".join(pixels[pixelStart:pixelEnd]))
