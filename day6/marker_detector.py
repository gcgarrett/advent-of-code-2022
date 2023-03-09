# open the file with the puzzle input
f = open('./puzzle_input.txt')

# there's only one line in the puzzle input file
line = f.readline()

def isMarker(characters):
    # create a set of the given characters, which will remove duplicates for us
    uniqueCharacters = set(characters)

    # if the length of the set is 4, then there are no duplicates and we have
    # our start-of-packet marker
    return len(uniqueCharacters) == 4

start = 0

while(start < len(line) - 4):
    # slicing is exclusive, so add 4 to the current start value
    end = start + 4

    if isMarker(line[start:end]):
        print("Marker start")
        print(str(end))
        break
    else:
        start += 1
