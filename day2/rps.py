# open the file with the puzzle input
f = open('./puzzle_input.txt')

# shape scores
rock = 1
paper = 2
scissors = 3

# shape conversions
shapesMap = {
    'A': rock,
    'B': paper,
    'C': scissors,
    'X': rock,
    'Y': paper,
    'Z': scissors
}

# outcome scores
loss = 0
draw = 3
win = 6

# my score
totalScore = 0

# loop through the puzzle input
while(True):
    # read next line
    line = f.readline()

    # EOF, break out of the loop
    if line == "":
        break

    # do calculations
    shapes = line.strip().split(' ')
    opponentShapeScore = shapesMap[shapes[0]]
    myShapeScore = shapesMap[shapes[1]]

    # add shape score to total score
    totalScore += myShapeScore

    if opponentShapeScore == myShapeScore:
        # draw
        totalScore += draw
    elif myShapeScore == paper and opponentShapeScore == rock:
        # win: paper beats rock
        totalScore += win
    elif myShapeScore == scissors and opponentShapeScore == paper:
        # win: scissors beat paper
        totalScore += win
    elif myShapeScore == rock and opponentShapeScore == scissors:
        # win: rock beats scissors
        totalScore += win
    else:
        # loss
        totalScore += loss

print("--RESULT--")
print(totalScore)
