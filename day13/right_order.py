import json
import logging

# configure the logging level
logging.basicConfig(level=logging.INFO)

# open the puzzle input file
f = open('./puzzle_input.txt')

# Puzzle documentation
#
# When comparing two values, the first value is called left and the second
# value is called right. Then:
#
# If both values are integers, the lower integer should come first. If the left
# integer is lower than the right integer, the inputs are in the right order.
# If the left integer is higher than the right integer, the inputs are not in
# the right order. Otherwise, the inputs are the same integer; continue
# checking the next part of the input.
#
# If both values are lists, compare the first value of each list, then the
# second value, and so on. If the left list runs out of items first, the inputs
# are in the right order. If the right list runs out of items first, the inputs
# are not in the right order. If the lists are the same length and no
# comparison makes a decision about the order, continue checking the next part
# of the input.
#
# If exactly one value is an integer, convert the integer to a list which
# contains that integer as its only value, then retry the comparison. For
# example, if comparing [0,0,0] and 2, convert the right value to [2] (a list
# containing 2); the result is then found by instead comparing [0,0,0] and [2].

# method to compare two lists of values to determine if their values are in
# order using the documentation above. if no decision is made, None is returned
#
# parameters
#   left (List):    The left list to compare
#   right (List):   The right list to compare
#
# returns
#   (Boolean|None): Returns True if the lists are in order, False if not, and
#                   None if no decision could be made
def compare(left, right):
    # iterate the number of items in the left list
    for i in range(len(left)):
        lValue = left[i]
        try:
            rValue = right[i]
        except IndexError:
            # we have run out of items in the right list, meaning the lists are
            # not in order
            logging.debug(f'Ran out of items on the right; index: {i}, length: {len(right)}')
            return False

        # if exactly one of the items to compare is a number, convert it to a
        # list to compare with the other item that is already a list
        if type(lValue) is int and type(rValue) is list:
            lValue = [lValue]
        elif type(lValue) is list and type(rValue) is int:
            rValue = [rValue]
        
        if type(lValue) is int:
            # if the left number is less than the right number, then the lists
            # are in order; if the left number is greater than the right number
            # then the lists are out of order
            if lValue < rValue:
                logging.debug(f'Left value less than right, items are in order: {lValue} < {rValue}')
                return True
            elif lValue > rValue:
                logging.debug(f'Left value greater than right, items are out of order: {lValue} > {rValue}')
                return False
        elif type(lValue) is list:
            logging.debug(f'Sub Left: {lValue}')
            logging.debug(f'Sub Right: {rValue}')
            logging.debug('--------------')
            # compare the two list values
            subResult = compare(lValue, rValue)

            # if a decision is made by the two list values, then return it
            if subResult is not None:
                logging.debug(f'Decision made when checking sub list: {subResult}')
                return subResult

    # the two lists are of equal length, but no decision was made, so return
    # None
    if len(left) == len(right):
        logging.debug('No decision made checking sub lists')
        return None

    # we iterated through all of the items in the left list, which is shorter
    # than the right list, so return True
    return True

# read the full puzzle input file
puzzleInput = f.read()
# split pairs on two new line (e.g. they are separated by a blank line)
pairs = puzzleInput.split('\n\n')

validIndices = []

# enumerate the pairs, setting 1 as the start index
for index, pair in enumerate(pairs, start=1):
    logging.debug(f'Pair: {index}')

    # split the pair on the new line to get the packets
    packets = pair.split('\n')
    # json parse the first (left) packet
    left = json.loads(packets[0])
    # json parse the second (right) packet
    right = json.loads(packets[1])

    logging.debug(f'Left: {left}')
    logging.debug(f'Right: {right}')
    logging.debug('===============')

    # if the compared packets are in the right order, add the index to the list
    # of valid pairs
    if compare(left, right):
        validIndices.append(index)

logging.debug(f'Valid indices: {validIndices}')

# sum the valid indices
indicesSum = sum(validIndices)

logging.info(f'Sum of indices: {indicesSum}')
