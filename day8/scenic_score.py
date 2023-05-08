# open the puzzle input file
f = open('./puzzle_input.txt')

# the grid of tree heights
grid = []

# loop through the input file
while(True):
    # read next line
    line = f.readline()

    # EOF, break out of the loop
    if line == "":
        break
    
    # generate the row, mapping the height characters to integers
    row = list(map(int, list(line.strip())))
    # append the row to the grid
    grid.append(row)

# Helper method to calculate the number of visible trees to the left of the
# given tree.
# parameters
#   rowIndex (Integer): the row of the tree to check
#   colIndex (Integer): the column of the tree to check
#   height   (Integer): the height of the tree
# returns
#   (Integer):          The number of visible trees to the left
def viewLeft(rowIndex, colIndex, height):
    score = 0
    currentColIndex = colIndex - 1

    while currentColIndex >= 0:
        currentTreeHeight = grid[rowIndex][currentColIndex]
        score += 1

        if currentTreeHeight < height:
            currentColIndex -= 1
        else:
            break
    
    return score

# Helper method to calculate the number of visible trees above the given tree.
# parameters
#   rowIndex (Integer): the row of the tree to check
#   colIndex (Integer): the column of the tree to check
#   height   (Integer): the height of the tree
# returns
#   (Integer):          The number of visible trees above
def viewUp(rowIndex, colIndex, height):
    score = 0
    currentRowIndex = rowIndex - 1

    while currentRowIndex >= 0:
        currentTreeHeight = grid[currentRowIndex][colIndex]
        score += 1

        if currentTreeHeight < height:
            currentRowIndex -= 1
        else:
            break
    
    return score

# Helper method to calculate the number of visible trees below the given tree.
# parameters
#   rowIndex (Integer): the row of the tree to check
#   colIndex (Integer): the column of the tree to check
#   height   (Integer): the height of the tree
# returns
#   (Integer):          The number of visible trees below
def viewDown(rowIndex, colIndex, height):
    score = 0
    currentRowIndex = rowIndex + 1

    while currentRowIndex < len(grid[rowIndex]):
        currentTreeHeight = grid[currentRowIndex][colIndex]
        score += 1

        if currentTreeHeight < height:
            currentRowIndex += 1
        else:
            break
    
    return score

# Helper method to calculate the number of visible trees to the right of the
# given tree.
# parameters
#   rowIndex (Integer): the row of the tree to check
#   colIndex (Integer): the column of the tree to check
#   height   (Integer): the height of the tree
# returns
#   (Integer):          The number of visible trees to the right
def viewRight(rowIndex, colIndex, height):
    score = 0
    currentColIndex = colIndex + 1

    while currentColIndex < len(grid):
        currentTreeHeight = grid[rowIndex][currentColIndex]
        score += 1

        if currentTreeHeight < height:
            currentColIndex += 1
        else:
            break
    
    return score

# Helper method to calculate the scenic score of a given tree.
# parameters
#   rowIndex (Integer): the row of the tree to check
#   colIndex (Integer): the column of the tree to check
# returns
#   (Integer):          The tree's scenic score
def calculateScenicScore(rowIndex, colIndex):
    height = grid[rowIndex][colIndex]

    # scenic score is the multiplication of the scores looking up, left, right,
    # and down
    return viewUp(rowIndex, colIndex, height) * viewLeft(rowIndex, colIndex, height) * viewRight(rowIndex, colIndex, height) * viewDown(rowIndex, colIndex, height)

rowIndex = 0
maxScenicScore = 0

# loop through the rows
for row in grid:
    colIndex = 0
    # loop through the trees in the row
    for tree in row:
        scenicScore = calculateScenicScore(rowIndex, colIndex)
        # if scenic score is greater than the current max, set as new max
        # scenic score
        if scenicScore > maxScenicScore:
            maxScenicScore = scenicScore
        colIndex += 1
    rowIndex += 1

print("Highest scenic score")
print(maxScenicScore)
