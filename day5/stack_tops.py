# open the initial stack states input
stacksFile = open('./stacks.txt')

stacks = []

while(True):
    # read next stack
    stackString = stacksFile.readline()

    # EOF, break out of the loop
    if stackString == "":
        break
    
    # create stack from crates
    stack = list(stackString.strip())
    # add to list of stacks
    stacks.append(stack)

movesFile = open('./moves.txt')

while True:
    # read next move
    moveString = movesFile.readline()

    # EOF, break out of the loop
    if moveString == "":
        break

    # split move into tokens
    tokens = moveString.strip().split(' ')

    count = 0
    start = 0
    end = 0

    # create iterator for the tokens
    iterator = iter(tokens)

    while True:
        try:
            # read next token
            token = next(iterator)

            if token == "move":
                # store the number of crates to move
                count = int(next(iterator))
            
            if token == "from":
                # store the stack to move from (zero based, so subtract 1)
                start = int(next(iterator)) - 1
            
            if token == "to":
                # store the stack to move to (zero based, so subtract 1)
                end = int(next(iterator)) - 1
        
        except StopIteration:
            # no more tokens, break out of loop
            break

    i = 0

    # move the crates
    while i < count:
        # pop crate off the from stack
        crate = stacks[start].pop()
        # push (append) to the to stack
        stacks[end].append(crate)
        i += 1

print("Stack tops")
for stack in stacks:
    if len(stack) > 0:
        print(stack.pop())
    else:
        print("_")
