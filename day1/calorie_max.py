f = open('./puzzle_input.txt')

currentCalories = 0
caloriesList = []

# loop through the input file
while(True):
    # get next line
    line = f.readline()

    # append the current calories count to the list if we are looking at a new
    # elf or are at the end of the file
    if line == "" or line == "\n":
        caloriesList.append(currentCalories)
        currentCalories = 0

    # EOF, break out of the loop
    if line == "":
        break

    # New elf, continue to the next one
    if line == "\n":
        continue

    # convert the line from a string to an integer
    calories = int(line.strip())
    # add value to running total
    currentCalories += calories

# sort list in descending order
caloriesList.sort(reverse=True)
# sum just the top three calorie counts
topCaloriesTotal = sum(caloriesList[:3])

print("--TOP CALORIES TOTAL--")
print(topCaloriesTotal)
