#!/usr/local/bin/python3

# Advent of code puzzle 11-1
# Transform stones according to a set of rules

# Advent of code puzzle 11-2
# Do the same but with so many times that first implementation algorith does not work!

# Transform a single stone according to transformation rules
def transformStone(number):
    
    # First rule: if number is 0, stone transforms to 1
    if number == 0:
        return [1]

    # Second rule: if there is even number of digits, split the number in half
    stringifiedNumber = str(number)
    numberLength = len(stringifiedNumber)
    if numberLength%2 == 0:
        halfLength = int(numberLength / 2)
        firstNumber = stringifiedNumber[:halfLength]
        secondNumber = stringifiedNumber[halfLength:]
        return[int(firstNumber), int(secondNumber)]

    # Third rule: multiply the number by 2024
    return [number*2024]
        

# Define initial stone arrangement
# To make algorithm more efficient, instead of storing each individual stone, we only store the count for all the stones that have the same number
testStoneArrangement = {125: 1, 17: 1}
realStoneArrangement = {4329: 1, 385: 1, 0: 1, 1444386: 1, 600463: 1, 19: 1, 1: 1, 56615: 1}
stoneArrangement = realStoneArrangement

# Transform the stone arrangement
for iTransformation in range(0, 75):
    transformedArrangement = {}

    # All the stones with the same number transform the same
    for stone, count in stoneArrangement.items():
       newStones = transformStone(stone)

       # Add the new stones to the transformed array. Count the number of duplicate stones
       for newStone in newStones:
           if newStone in transformedArrangement:
               transformedArrangement[newStone] = transformedArrangement[newStone] + count
           else:
               transformedArrangement[newStone] = count

    # After everything is transformed, update the stone arrangement
    stoneArrangement = transformedArrangement

# Print the final number of stones
stoneCount = 0
for stone, count in stoneArrangement.items():
    stoneCount = stoneCount + count
print("Final number of stones is {}".format(stoneCount))
