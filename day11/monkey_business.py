import getopt
import logging
import re
import sys

logging.basicConfig(level=logging.WARNING)

# open the puzzle input file
f = open('./puzzle_input.txt')

class Item:
    def __init__(self, worryLevel):
        self.worryLevel = worryLevel
    def __str__(self):
        return str(self.worryLevel)
    def setWorryLevel(self, worryLevel):
        self.worryLevel = worryLevel

class Monkey:
    def __init__(self, num, op, opAmt, testAmt, trueMonkey, falseMonkey):
        self.num = num
        self.items = []
        self.op = op
        self.opAmt = opAmt
        self.testAmt = testAmt
        self.trueMonkey = trueMonkey
        self.falseMonkey = falseMonkey
        self.inspectedItems = 0
    def __str__(self):
        worryLevels = []
        for item in self.items:
            worryLevels.append(str(item))
        return f'Monkey {self.num}: {", ".join(worryLevels)}'
    def addItem(self, item):
        self.items.append(item)
    def getItem(self):
        if len(self.items) == 0:
            return None
        else:
            return self.items.pop(0)
    def inspectItem(self):
        self.inspectedItems += 1

# the number of rounds to run
ROUNDS = 20
# are we dividing the worry level, e.g. we are relieved when a monkey throws
# an item
DIV_WORRY_LEVEL = True
# what we should divide the worry level by (or modulo by, in the case where we
# have thousands of rounds)
WORRY_LEVEL_DIVISOR = 3

# command line arguments
#   -r, --rounds: the number of rounds to run
#   -n, --no-div: don't divide the item's worry level by 3 after each round
opts, args = getopt.getopt(sys.argv[1:], 'r:n', ['rounds=', 'no-div'])

for opt, arg in opts:
    if opt in ('-r', '--rounds'):
        ROUNDS = int(arg)
    elif opt in ('-n', '--no-div'):
        DIV_WORRY_LEVEL = False

logging.debug(f'Rounds: {ROUNDS}')
logging.debug(f'Divide the worry level: {DIV_WORRY_LEVEL}')

# list of the monkeys
monkeys = []

num = 0
op = '+'
opAmt = 0
testAmt = 0
trueMonkey = 0
falseMonkey = 0
worryLevels = []

# loop through the input file
while(True):
    # read next line
    line = f.readline()

    # if we encounter a blank line, create a new monkey from the parse values
    if line == '\n' or line == '':
        logging.debug(f'{num}: {op}, {opAmt}, {testAmt}, {trueMonkey}, {falseMonkey}')
        monkey = Monkey(num, op, opAmt, testAmt, trueMonkey, falseMonkey)

        for worryLevel in worryLevels:
            item = Item(worryLevel)
            monkey.addItem(item)

        monkeys.append(monkey)

    # EOF, break out of the loop
    if line == '':
        break

    line = line.strip()

    # parse the first line with the monkey identifier
    match = re.search(r'Monkey ([0-9]):', line)

    if match:
        num = int(match.group(1))

    # parse the second line with the starting items
    if line.startswith('Starting items:'):
        tokens = line.split(': ')
        worryLevels = list(map(int, tokens[1].split(', ')))

    # parse the third line with the operation to perform
    match = re.search(r'Operation: new = old ([+*]) ([old0-9]+)', line)

    if match:
        op = match.group(1)
        opAmt = match.group(2)

    # parse the fourth line with the test condition
    match = re.search(r'Test: divisible by ([0-9]+)', line)

    if match:
        testAmt = int(match.group(1))

    # parse the fifth line with the true condition
    match = re.search(r'If true: throw to monkey ([0-9]+)', line)

    if match:
        trueMonkey = int(match.group(1))

    # parse the sixth line with the false condition
    match = re.search(r'If false: throw to monkey ([0-9]+)', line)

    if match:
        falseMonkey = int(match.group(1))

if not DIV_WORRY_LEVEL:
    # if we are not experiencing relief when a monkey throws an item, that is,
    # dividing the worry level of an item every round, then we need to modulo
    # the worry level of the item so the number isn't astronomical. I was
    # running into errors debugging the code because the worry level numbers
    # exceeded 4300 digits! Since all of the test divisors are prime numbers,
    # we can take the modulo of the worry level of an item with the product of
    # these prime numbers and still obtain valid test results for which monkey
    # to throw to. Thus we are using the Chinese remainder theorem to ensure
    # our worry level does not go through the roof.
    WORRY_LEVEL_DIVISOR = 1
    for monkey in monkeys:
        WORRY_LEVEL_DIVISOR = WORRY_LEVEL_DIVISOR * monkey.testAmt

logging.debug(f'Worry level divisor: {WORRY_LEVEL_DIVISOR}')

# run all of the rounds
for r in range(ROUNDS):
    logging.info(f'Round: {r}')

    # loop through all of the monkeys
    for monkey in monkeys:
        logging.debug(monkey)
        item = monkey.getItem()

        # loop until there are no more items for the monkey
        while item is not None:
            worryLevel = item.worryLevel
            amount = monkey.opAmt

            if amount == 'old':
                # if amount is the string "old", then use the current worry
                # level
                amount = worryLevel
            else:
                # since amount can be the string "old", cast to an int if it
                # isn't
                amount = int(amount)

            logging.debug(f'Worry level: {worryLevel}; Amount: {amount}; Operation: {monkey.op}')

            if monkey.op == '+':
                worryLevel = worryLevel + amount
            elif monkey.op == '*':
                worryLevel = worryLevel * amount

            if DIV_WORRY_LEVEL:
                # divide the worry level by the worry level divisor, getting
                # the floor of the result
                worryLevel = worryLevel // WORRY_LEVEL_DIVISOR
            else:
                # modulo the worry level by the worry level divisor so our
                # worry level doesn't grow to huge numbers (e.g. over 4300
                # digits)
                worryLevel = worryLevel % WORRY_LEVEL_DIVISOR

            # update the item's worry level
            item.setWorryLevel(worryLevel)

            # test if the worry level meets the condition
            if worryLevel % monkey.testAmt == 0:
                monkeys[monkey.trueMonkey].addItem(item)
            else:
                monkeys[monkey.falseMonkey].addItem(item)

            # record that the monkey inspected the item
            monkey.inspectItem()

            # get the next item
            item = monkey.getItem()

def sortByInspectedItems(monkey):
    return monkey.inspectedItems

# sort the monkeys by the number of items they've inspected items
monkeys.sort(reverse=True, key=sortByInspectedItems)

# get a list of times the monkeys have inspected items
inspectedItemsList = list(map(lambda m: m.inspectedItems, monkeys))

logging.debug(f'Number of times the monkeys inspected items: {inspectedItemsList}')

# level of monkey business is the multiple of the number of times the top two
# monkeys have inspected items
x = inspectedItemsList[0]
y = inspectedItemsList[1]

print('Level of monkey business')
print(x * y)
