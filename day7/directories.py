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
