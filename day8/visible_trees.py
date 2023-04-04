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

# helper method to determine if a tree is visible in a row.
# parameters
#   rowIndex (Integer): the row of the tree to check
#   colIndex (Integer): the column of the tree to check
#   height   (Integer): the height of the tree
# returns
#   (Boolean):          True if the tree is visible in the row, false if hidden
def isVisibleInRow(rowIndex, colIndex, height):
    cIndex = 0
    visibleLeft = True
    visibleRight = True

    # loop through the heights in the row
    for h in grid[rowIndex]:
        # if current height is greater or equal to the given tree height...
        if h >= height:
            # this tree is to the left of the given tree, so it is not visible
            # from the left
            if cIndex < colIndex:
                visibleLeft = False
            # this tree is to the right of the given tree, so it is not visible
            # from the right
            elif cIndex > colIndex:
                visibleRight = False
        cIndex += 1

    # a tree is visible in a row if it can be seen from the left or right
    return visibleLeft or visibleRight

# helper method to determine if a tree is visible in a column.
# parameters
#   rowIndex (Integer): the row of the tree to check
#   colIndex (Integer): the column of the tree to check
#   height   (Integer): the height of the tree
# returns
#   (Boolean):          True if the tree is visible in the column, false if
#                       hidden
def isVisibleInCol(rowIndex, colIndex, height):
    rIndex = 0
    visibleTop = True
    visibleBottom = True

    # loop through the heights in the column
    while rIndex < len(grid):
        h = grid[rIndex][colIndex]
        # if current height is greater or equal to the given tree height...
        if h >= height:
            # this tree is above the given tree, so it is not visible from the
            # top
            if rIndex < rowIndex:
                visibleTop = False
            # this tree is below the given tree, so it is not visible from the
            # bottom
            elif rIndex > rowIndex:
                visibleBottom = False
        rIndex += 1

    # a tree is visible in a column if it can be seen from the top or bottom
    return visibleTop or visibleBottom

# helper method to determine if a tree is visible.
# parameters
#   rowIndex (Integer): the row of the tree to check
#   colIndex (Integer): the column of the tree to check
#   height   (Integer): the height of the tree
# returns
#   (Boolean):          True if the tree is visible, false if hidden
def isVisible(rowIndex, colIndex, height):
    # a tree is visible if it can be seen from the top, right, bottom, or left
    return isVisibleInRow(rowIndex, colIndex, height) or isVisibleInCol(rowIndex, colIndex, height)

rowIndex = 0
numberVisible = 0

# loop through the rows
for row in grid:
    colIndex = 0
    # loop through the trees in the row
    for height in row:
        # if the tree is visible, increment the number of visible trees
        if isVisible(rowIndex, colIndex, height):
            numberVisible += 1
        colIndex += 1
    rowIndex += 1

print("Number of visible trees")
print(numberVisible)
