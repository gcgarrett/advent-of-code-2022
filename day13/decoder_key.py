from functools import cmp_to_key
import json
import logging
from math import prod

# configure the logging level
logging.basicConfig(level=logging.INFO)

# the divider packets
DIVIDER_PACKETS = [[[2]], [[6]]]

# open the puzzle input file
f = open('./puzzle_input.txt')

# method to compare two lists of values to determine if their values are in
# order using the documentation above. if no decision is made, 0 is returned
#
# parameters
#   a (List):  The a list to compare
#   b (List):  The b list to compare
#
# returns
#   (Integer): Returns -1 if a is before b, 1 if a is after b, and 0 if no
#              decision could be made
def compare(a, b):
    # iterate through the number of items in the a list
    for i in range(len(a)):
        aValue = a[i]
        try:
            bValue = b[i]
        except IndexError:
            # we have run out of items in the b list, meaning a comes after b
            return 1

        # if exactly one of the items to compare is a number, convert it to a
        # list to compare with the other item that is already a list
        if type(aValue) is int and type(bValue) is list:
            aValue = [aValue]
        elif type(aValue) is list and type(bValue) is int:
            bValue = [bValue]
        
        if type(aValue) is int:
            # if the a number is less than the b number, then the a list comes
            # before the b list; if the a number is greater than the b number
            # then the a list comes after the b list
            if aValue < bValue:
                return -1
            elif aValue > bValue:
                return 1
        elif type(aValue) is list:
            # compare the two list values
            subResult = compare(aValue, bValue)

            # if a decision is made by the two list values, then return it
            if subResult != 0:
                return subResult

    # the two lists are of equal length, but no decision was made, so return
    # 0
    if len(a) == len(b):
        logging.debug('No decision made checking sub lists')
        return 0

    # we iterated through all of the items in the a list, which is shorter
    # than the b list, so return -1 since the a list comes before the b list
    return -1

packets = []

# parse the puzzle input, skipping blank lines
while(True):
    # read next line
    line = f.readline()

    # EOF, break out of the loop
    if line == '':
        break

    # Blank line, skip
    if line == '\n':
        continue

    line = line.strip()

    # convert the line to a list using json.loads
    packets.append(json.loads(line))

# add the divider packets
packets.extend(DIVIDER_PACKETS)

# sort the packets using the `compare` function, which is converted to a key
# function using `cmp_to_key`
sortedPackets = sorted(packets, key=cmp_to_key(compare))

dividerPacketIndices = []

for index, packet in enumerate(sortedPackets, start=1):
    if packet in DIVIDER_PACKETS:
        # if packet is one of the divider packets, append its index to the
        # list
        dividerPacketIndices.append(index)

# multiply the divider packet indices together to get the decoder key
decoderKey = prod(dividerPacketIndices)

logging.info(f'Decoder key: {decoderKey}')
