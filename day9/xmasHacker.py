#!/usr/local/bin/python3

# Advent of code puzzle 9-1
# Find the first value from the list that is not a sum of two of the 25 previous numbers

# Advent of code puzzle 9-2
# Find a set of contiguous numbers that sums to the number from problem 9-1

# Check if the value in index is valid according to XMAS encoding with a given preamble size
def isValidNumber(xmasSequence, preambleSize, index):

    # If the index is from preamble, just return true. This is not really part of data.
    if index < preambleSize:
        return True

    # If the index is too large, return False
    if index >= len(xmasSequence):
        return False

    # Check if the value at position index is a sum of two numbers from preambleSize entries before that
    for i in range(index-preambleSize, index):
        for j in range(i+1, index):
            if xmasSequence[i]+xmasSequence[j] == xmasSequence[index]:
                return True

    # If the value at index is not a sum of previous values, return False
    return False

# Check if the given number is a sum of groupSize contiguous numbers in the xmasSequence
def isContiguousSum(xmasSequence, groupSize, number):

    # Check if the value at position index is a sum of two numbers from preambleSize entries before that
    for i in range(0, len(xmasSequence)-groupSize):
        contiguousSum = 0
        for j in range(i, i+groupSize):
            contiguousSum = contiguousSum + xmasSequence[j]

        # If we find the sum, return the first an last index summing to that
        if contiguousSum == number:
            return (i, i+groupSize)

    # If the value at index is not a sum of previous values, return -1 as index
    return (-1,-1)

# Find smallest and largest number in a given range
def findSmallestAndLargest(xmasSequence, firstIndex, lastIndex):

    minNumber = 1e20
    maxNumber = -1e20

    for index in range(firstIndex,lastIndex):
        if xmasSequence[index] < minNumber:
            minNumber = xmasSequence[index]
        if xmasSequence[index] > maxNumber:
            maxNumber = xmasSequence[index]

    return (minNumber, maxNumber)

# Read the input file
xmasFile = open("xmasSequence.txt","r")
xmasSequenceRaw = xmasFile.readlines()

# Convert the sequence to numbers
xmasSequence = [int(i) for i in xmasSequenceRaw]

# Find the first number that is not a sum of previous values
nonValidNumber = -1
nonValidIndex = -1
preambleSize = 25
for index in range(preambleSize,len(xmasSequence)):
    if not isValidNumber(xmasSequence, preambleSize, index):
        nonValidNumber = xmasSequence[index]
        nonValidIndex = index
        break

# Print the answer!
print("The first number not following xmas rules is {:d}".format(nonValidNumber))

# Find a contiguous set of numbers that sum to nonValidNumber
firstIndex = -1
lastIndex = -1
for setSize in range(2,nonValidIndex):
    (firstIndex,lastIndex) = isContiguousSum(xmasSequence, setSize, nonValidNumber)
    if firstIndex >= 0:
        break

# Find the smallest and largest numbers in the obtained range
(smallNumber, bigNumber) = findSmallestAndLargest(xmasSequence, firstIndex, lastIndex)

# Print the indices for the range and the sum of smallest and largest numbers in the range
print("{:d} is as sum of numbers from index {:d} to index {:d}".format(nonValidNumber, firstIndex, lastIndex-1))
print("Sum of smallest and largest numbers in this range is is {:d}".format(smallNumber + bigNumber))
