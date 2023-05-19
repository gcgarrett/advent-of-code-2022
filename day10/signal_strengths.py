import logging

logging.basicConfig(level=logging.WARNING)

# open the puzzle input file
f = open('./puzzle_input.txt')

# cycles are not zero-based
cycleCount = 1
# initialize register x with value 1
registerX = 1
# list of signal strengths
signalStrengths = []

# helper method to check if the signal strength needs to be calculated based on
# which cycle it is. Signal strength is calculated on the 20th, 60th, 100th,
# 140th, 180th, and 220th cycles.
#
# returns
#   (nothing): Appends the calculated signal strength to the list if
#              appropriate
def checkSignalStrength():
    logging.debug(f'Cycle: {cycleCount}; X: {registerX}')
    # if it is the 20th cycle or 20 plus some multiple of 40 (60, 100, 140,
    # 180, 220) then calculate and store the signal strength
    if cycleCount == 20 or (cycleCount - 20) % 40 == 0:
        # signal strength is cycle count multiplied by value in register x
        signalStrength = cycleCount * registerX
        logging.debug(f'Signal strength: {signalStrength}')
        signalStrengths.append(signalStrength)

# helper method to run a cycle. Checks if the signal strength needs to be
# calculated first, then increments the cycle count.
#
# returns
#   (nothing): Increments the global cycle count by 1
def cycle():
    global cycleCount
    # check for signal strength
    checkSignalStrength()
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

logging.info(signalStrengths)

print("Signal strengths sum")
print(sum(signalStrengths))
