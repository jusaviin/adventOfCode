#!/usr/local/bin/python3

# Advent of code puzzle 15-1
# Determine the 2020th number of the memory game

# Advent of code puzzle 15-2
# Determine the 30000000th number of the memory game

# Determine what is the next number based on the previous numbers
def nextNumberSpoken(numbersSpoken):

    # Check how many time the last number is spoken
    lastNumberSpokenCount = numbersSpoken.count(numbersSpoken[len(numbersSpoken)-1])

    # If the last number spoken was the first time it was said, the next number is 0
    if lastNumberSpokenCount == 1:
        return 0

    # If the last number is spoken more than once, next number is the number of turns apart the number is from when it was previously spoken.
    gapSize = 1
    for index in range(len(numbersSpoken)-2,-1,-1):
        if numbersSpoken[index] == numbersSpoken[len(numbersSpoken)-1]:
            return gapSize
        gapSize = gapSize + 1

    # We should never be here. Return error
    return "ERROR"

# Fast algorithm to determine what is the next number based on the previous numbers
def nextNumberSpokenQuick(numberDictionary):

    # Find the current turn and the last spoken number
    lastNumber = numberDictionary["last"]

    # If the last number is spoken more than once, next number is the number of turns apart the number is from when it was previously spoken.
    if numberDictionary[lastNumber][0] > 0:
        nextNumber = numberDictionary[lastNumber][1] - numberDictionary[lastNumber][0]

    # If the last number has not been spoken before, the next number is zero
    else:
        nextNumber = 0

    # Return the next number and whether is has been seen before
    return nextNumber

#############################
##       Main program      ##
#############################

# Initial number array
numbersSpoken = [6,13,1,15,2,0]

# Find the 2020th number spoken
while len(numbersSpoken) < 2020:
    nextNumber = nextNumberSpoken(numbersSpoken)
    numbersSpoken.append(nextNumber)

# Print the answer!
print("The 2020th number spoken is {:d}".format(numbersSpoken[2019]))

# Do the same but with an improved algorithm to get more easily into large numbers!
numberDictionary = {6:(-1,1), 13:(-1,2), 1:(-1,3), 15:(-1,4), 2:(-1,5), 0:(-1,6), "last":0}

for turn in range(7, 30000001):
    nextNumber = nextNumberSpokenQuick(numberDictionary)
    if nextNumber in numberDictionary:
        numberDictionary[nextNumber] = (numberDictionary[nextNumber][1], turn)
    else:
        numberDictionary[nextNumber] = (-1,turn)
    numberDictionary["last"] = nextNumber

# Print the answer!
print("The 30000000th number spoken is {:d}".format(nextNumber))
