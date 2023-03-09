# open the file with the puzzle input
f = open('./puzzle_input.txt')

# specify the marker length
MARKER_LEN = 14

# there's only one line in the puzzle input file
line = f.readline()

def isMarker(characters):
    # create a set of the given characters, which will remove duplicates for us
    uniqueCharacters = set(characters)

    # if the length of the set is 14, then there are no duplicates and we have
    # our start-of-message marker
    return len(uniqueCharacters) == MARKER_LEN

start = 0

while(start < len(line) - MARKER_LEN):
    # slicing is exclusive, so add 14 to the current start value
    end = start + MARKER_LEN

    if isMarker(line[start:end]):
        print("Message start")
        print(str(end))
        break
    else:
        start += 1
