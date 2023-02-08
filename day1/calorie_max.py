f = open('./puzzle_input.txt')

currentCalories = 0
caloriesMax = 0

while(True):
    line = f.readline()

    if line == "" or line == "\n":
        if currentCalories > caloriesMax:
            caloriesMax = currentCalories
        currentCalories = 0

    if line == "":
        print("--EOF--")
        break

    if line == "\n":
        print("--NEW ELF--")
        continue
    
    calories = int(line.strip())
    print("--CALORIES--")
    print(calories)
    currentCalories += calories
    print("--CURRENT--")
    print(currentCalories)

print("--MAX CALORIES--")
print(caloriesMax)
