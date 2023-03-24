# open the puzzle input file
f = open('./puzzle_input.txt')

# create a class to represent the directories
class Directory:
    def __init__(self, name):
        self.name = name
        self.children = []
        self.files = []
    def addChild(self, child):
        self.children.append(child)
    def getChildByName(self, childName):
        for child in self.children:
            if child.name == childName:
                return child
        return None
    def addFile(self, file):
        self.files.append(file)

# create a class to represent the files
class File:
    def __init__(self, name, size):
        self.name = name
        self.size = size

# keep track of the path we traverse
path = []
# create the root directory, which is at "/"
root = Directory("root")
# global reference to the current directory
currentDirectory = root
# sum of the total sizes of directories with total size at most 100,000
totalSum = 0

# helper method to find a directory in the tree
# parameters
#   node (Directory): the current directory in the tree
#   path (List):      the list of folders in the path, reversed so it acts like
#                     a stack, with the directory closest to the root at the
#                     top
#   name (String):    the name of the directory we are looking for
# returns
#   (Directory):        returns the directory when found or None
def findDirectory(node, path, name):
    nextDirectory = None
    nextChildName = None

    # if path still includes items, we are looking for an ancestor directory
    # of the given directory, so pop off the ancestor directory name and look
    # for that in the current directory's children
    if len(path) > 0:
        nextDirectory = path.pop()

    if nextDirectory != None:
        nextChildName = nextDirectory
    else:
        # else look for the given directory name
        nextChildName = name

    # find the target directory in the current directory's children
    childNode = node.getChildByName(nextChildName)

    if nextDirectory != None:
        # if we were finding an ancestory directory, call again for the found
        # directory with the modified path where the found directory name was
        # removed
        return findDirectory(childNode, path, name)
    else:
        # else return what we found for the given directory
        return childNode

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
