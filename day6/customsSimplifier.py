#!/usr/local/bin/python3

# Advent of code puzzle 6-1
# Find number of unique answers within groups from customs declaration forms

# Advent of code puzzle 6-2
# Find number of common answers within groups from customs declaration forms

import string # Easy way to produce all ascii characters

# Count the number of unique characters in a string
def countUniqueCharacters(inputString):

    uniqueCharacters = ""

    for character in inputString:
        if uniqueCharacters.count(character) == 0:
            uniqueCharacters = uniqueCharacters + character

    return len(uniqueCharacters)

# Count the number characters that occur n times in input string
def countRecurringCharacters(inputString, nTimes):

    # Possible answers in the customs declaration form
    possibleCharacters = list(string.ascii_lowercase)

    # Count the number of times each character is present in the input string
    nRecurringCharacters = 0
    for character in possibleCharacters:
        if inputString.count(character) == nTimes:
            nRecurringCharacters = nRecurringCharacters + 1

    return nRecurringCharacters

# Read the input file
customsAnswerFile = open("customsAnswers.txt","r")
allAnswers = customsAnswerFile.readlines()

# Read all answers that were given to customs declaration by groups
answerArray = []
myAnswer = ""
groupSize = 0
for answerLine in allAnswers:

    # If there is empty line, one group customs answers ends
    if(answerLine == "\n"):
        answerArray.append((myAnswer,groupSize))
        groupSize = 0
        myAnswer = ""

    # When there is no empty line, add the information for current group
    else:
        myAnswer = myAnswer + answerLine[0:-1] # Remove newline character from the line
        groupSize = groupSize + 1

# If the remaining passport is not empty, add it to array
if not(myAnswer == ""):
    answerArray.append((myAnswer,groupSize))

# Check the number of unique answers within each group and calculate their sum
uniqueSum = 0
for groupAnswer,groupSize in answerArray:
    uniqueSum = uniqueSum + countUniqueCharacters(groupAnswer)

# Print the answer!
print("There are {:d} unique yes answers in all groups.".format(uniqueSum))

# Then find the number of common answers within each groups
commonSum = 0
for groupAnswer,groupSize in answerArray:
    commonSum = commonSum + countRecurringCharacters(groupAnswer,groupSize)

# Print the answer!
print("There are {:d} common yes answers within all groups.".format(commonSum))
