# import the Directory and File classes and findDirectory method from
# directories
from directories import *

# open the puzzle input file
f = open('./puzzle_input.txt')

# total disk space available, 70,000,000
TOTAL_DISK_SPACE = 70000000
# free disk space required to do upgrade, 30,000,000
UPGRADE_FREE_SPACE = 30000000
# keep track of the path we traverse
path = []
# create the root directory, which is at "/"
root = Directory("root")
# global reference to the current directory
currentDirectory = root

# helper method to find the size of a given directory. because a directory's
# size includes the sizes of all its descendant directories this will call this
# function on all of the given directory's children recursively.
# parameters
#   node (Directory): the current directory in the tree
# returns
#   (Integer):        the total size of the directory
def size(node):
    sum = 0

    # sum sizes of all descendants of this directory
    for child in node.children:
        sum = sum + size(child)

    # sum size of all files of this directory
    for fi in node.files:
        sum = sum + fi.size
    
    return sum

# helper method to collect the size of the given directory and all of its
# children.
# parameters
#   node (Directory): the current directory in the tree
# returns
#   (List):           the list of directory sizes
def collectSizes(node, sizes = []):
    # calculate size of directory
    nodeSize = size(node)

    # add size to result
    sizes.append(nodeSize)

    # loop through children and run this function on each of them
    for child in node.children:
        collectSizes(child, sizes)

    return sizes

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
        
# calculate the used space on the disk (e.g. the root node size)
usedSpace = size(root)
# calculate the unused space on the disk
unusedSpace = TOTAL_DISK_SPACE - usedSpace
# calculate minimum we need to delete to upgrade
threshold = UPGRADE_FREE_SPACE - unusedSpace
# collect the directory sizes
directorySizes = collectSizes(root)
# set smallest value to maximum (TOTAL_DISK_SPACE)
smallest = TOTAL_DISK_SPACE

for directorySize in directorySizes:
    # if directory size is greater than or equal to the threshold and it is
    # less than the smallest value, use it for the smallest value
    if directorySize >= threshold and directorySize < smallest:
        smallest = directorySize

print("Smallest size to free up space")
print(smallest)
