# open the file with the puzzle input
f = open('./puzzle_input.txt')

# tuple of priorties; probably there's a better way to do this initialization.
# _ takes up the zero index in the list.
# use a tuple because we want it to be immutable.
priorities = (
    '_',
    'a',
    'b',
    'c',
    'd',
    'e',
    'f',
    'g',
    'h',
    'i',
    'j',
    'k',
    'l',
    'm',
    'n',
    'o',
    'p',
    'q',
    'r',
    's',
    't',
    'u',
    'v',
    'w',
    'x',
    'y',
    'z',
    'A',
    'B',
    'C',
    'D',
    'E',
    'F',
    'G',
    'H',
    'I',
    'J',
    'K',
    'L',
    'M',
    'N',
    'O',
    'P',
    'Q',
    'R',
    'S',
    'T',
    'U',
    'V',
    'W',
    'X',
    'Y',
    'Z'
)

# sum of priorities
sumOfPriorities = 0

# loop through the puzzle input
while(True):
    # read next line
    line = f.readline()

    # EOF, break out of the loop
    if line == "":
        break

    # split rucksack items into compartments
    rucksackItems = list(line.strip())
    itemCount = len(rucksackItems)
    # find midpoint in rucksack
    splitOn = itemCount // 2

    # create sets of the items in the two compartments, that way the items we
    # iterate over are unique

    # create a set of items in the first compartment
    compartmentA = set(rucksackItems[:splitOn])
    # create a set of items in the second compartment
    compartmentB = set(rucksackItems[splitOn:])

    # find duplicate
    for item in compartmentA:
        if item in compartmentB:
            # add item priority to the sum
            sumOfPriorities += priorities.index(item)

print("Sum of priorities")
print(sumOfPriorities)