# open the file with the puzzle input
f = open('./puzzle_input.txt')

# number of assignment pairs where one range fully contains the other
contains = 0

def doesContain(a, b):
    minA = a[0]
    maxA = a[1]
    minB = b[0]
    maxB = b[1]

    return (minA <= minB) and (maxA >= maxB)

# loop through the puzzle input
while(True):
    # read next line
    line = f.readline()

    # EOF, break out of the loop
    if line == "":
        break
    
    # split assignment pair on the "," into range pairs
    rangePairs = line.strip().split(',')
    # split range pairs on the "-" into min/max values and map to ints
    rangeA = list(map(int, rangePairs[0].split('-')))
    rangeB = list(map(int, rangePairs[1].split('-')))

    # test if rangeA contains rangeB or rangeB contains rangeA
    if doesContain(rangeA, rangeB) or doesContain(rangeB, rangeA):
        contains += 1

print("Number of assignment pairs where one range fully contains the other")
print(contains)
