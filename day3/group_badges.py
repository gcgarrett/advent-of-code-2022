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

# rucksacks group
rucksackGroup = []
# sum of priorities
sumOfPriorities = 0

# loop through the puzzle input
while(True):
    # read next line
    line = f.readline()

    # if we have all of the rucksacks for the group...
    if len(rucksackGroup) == 3:
        for item in rucksackGroup[0]:
            # check if item is in the other rucksacks
            if item in rucksackGroup[1] and item in rucksackGroup[2]:
                # add item priority to the sum
                sumOfPriorities += priorities.index(item)
                break
        # clear rucksacks from the list to start next group
        rucksackGroup.clear()

    # EOF, break out of the loop
    if line == "":
        break

    # create set of unique items in the rucksack
    rucksackItems = set(line.strip())
    # add rucksack to the group
    rucksackGroup.append(rucksackItems)

print("Sum of priorities")
print(sumOfPriorities)
