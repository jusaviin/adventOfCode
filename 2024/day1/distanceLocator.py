#!/usr/local/bin/python3

# Advent of code puzzle 1-1
# Order two columns of numbers and find distance between them

# Advent of code puzzle 1-2
# Calculate the similarity score, multiply each number in one list to the number of times it appears in the other list and add them together

def countAppearances(myList, myNumber):
    myCount = 0
    for listNumber in myList:
        if(myNumber == listNumber):
            myCount = myCount + 1
    return myCount

# Read the input file
locationFile = open("historianLists.txt","r")

# Separate the lines into two lists using space as separator
firstList = []
secondList = []
for line in locationFile:
    locations = line.split()
    firstList.append(int(locations[0]))
    secondList.append(int(locations[1]))

# Sort the lists
firstList.sort()
secondList.sort()

# Calculate the distance between locations in the two lists
totalDistance = 0
for iLocation in range(0, len(firstList)):
    totalDistance = totalDistance + abs(firstList[iLocation] - secondList[iLocation])

# Print the total distance between the two lists
print("Total distance between the lists is {}".format(totalDistance))

# Calculate the similarity score between the list
similarityScore = 0
for firstNumber in firstList:
    numberCount = countAppearances(secondList, firstNumber)
    similarityScore = similarityScore + numberCount * firstNumber

# Print the similarity score between the two lists
print("Similarity score between the lists is {}".format(similarityScore))
