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
    'C': scissors
}

# outcome scores
loss = 0
draw = 3
win = 6

# outcome conversions
outcomesMap = {
    'X': loss,
    'Y': draw,
    'Z': win
}

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
    guideValues = line.strip().split(' ')
    inputShapeScore = shapesMap[guideValues[0]]
    outcomeScore = outcomesMap[guideValues[1]]

    # add outcome score to total score
    totalScore += outcomeScore

    if outcomeScore == draw:
        # add input shape score in case of draw (same shapes)
        totalScore += inputShapeScore
    elif inputShapeScore == rock:
        # if input shape is rock...
        if outcomeScore == win:
            # throw paper to win
            totalScore += paper
        else:
            # throw scissors to lose
            totalScore += scissors
    elif inputShapeScore == paper:
        # if input shape is paper...
        if outcomeScore == win:
            # throw scissors to win
            totalScore += scissors
        else:
            # throw rock to lose
            totalScore += rock
    elif inputShapeScore == scissors:
        # if input shape is scissors...
        if outcomeScore == win:
            # throw rock to win
            totalScore += rock
        else:
            # throw paper to lose
            totalScore += paper

print("--RESULT--")
print(totalScore)
