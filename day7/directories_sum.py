# import the Directory and File classes from directories
from directories import *

# open the puzzle input file
f = open('./puzzle_input.txt')

# keep track of the path we traverse
path = []
# create the root directory, which is at "/"
root = Directory("root")
# global reference to the current directory
currentDirectory = root
# sum of the total sizes of directories with total size at most 100,000
totalSum = 0

# helper method to sum the sizes of for a given directory. because a
# directory's size includes the sizes of all its descendant directories this
# will call this function on all of the given directory's children recursively.
# parameters
#   node (Directory): the current directory in the tree
# returns
#   (Integer):        the total size of the directory
# notes
#   also add the sum to the global totalSum value if the sum is at most 100,000
def sumSizes(node):
    # modify global copy of totalSum
    global totalSum
    sum = 0

    # sum sizes of all descendants of this directory
    for child in node.children:
        sum = sum + sumSizes(child)

    # sum size of all files of this directory
    for fi in node.files:
        sum = sum + fi.size

    print("Directory '" + node.name + "' sum is " + str(sum))

    # add sum to global totalSum if value is at most 100,000
    if sum <= 100000:
        totalSum = totalSum + sum
    
    return sum

# loop through the input file
while(True):
    # read next line
    line = f.readline()

    # EOF, break out of the loop
    if line == "":
        break
    
    # split line into tokens
    tokens = line.strip().split(' ')

    if tokens[0] == "$":
        # first token is the $ symbol, indicating a command
        if tokens[1] == "cd":
            # do path operations
            if tokens[2] == "/":
                # set path back to root
                path = []
            elif tokens[2] == "..":
                # move one directory back in the path
                path.pop()
            else:
                # move into child directory
                path.append(tokens[2])
        elif tokens[1] == "ls":
            # do ls operations, which updates the global current directory value
            if len(path) == 0:
                # path length is 0, so we are at the root
                currentDirectory = root
            else:
                # get current directory name, which is the last item in the path
                dirName = path[-1]
                # create a subpath of ancestors to the current directory
                subPath = path[0:-1]
                # reverse the order of the subpath so it acts like a stack
                subPath = subPath[::-1]
                # find the current directory in the tree
                currentDirectory = findDirectory(root, subPath, dirName)
    elif tokens[0] == "dir":
        # create a new child directory of the current directory
        newChild = Directory(tokens[1])
        currentDirectory.addChild(newChild)
    else:
        # create a new file under the current directory
        newFile = File(tokens[1], int(tokens[0]))
        currentDirectory.addFile(newFile)
        

sumSizes(root)

print("--Total sum of directory sizes at most 100,000--")
print(totalSum)
