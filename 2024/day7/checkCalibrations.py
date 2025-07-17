#!/usr/local/bin/python3

# Advent of code puzzle 7-1
# Check that calibrations work with "*" and "+" operators

# Advent of code puzzle 7-2
# Add also concatenation operator "||"

# Find all possible results when these operands are operated with "*", "+" or "||"
# "||" operator just merges the two numbers 1 || 2 = 12
def findPossibleResults(operands):
    
    possibleResults = []

    # If there are only two operands left, the three possbile results are addition, multiplication and concatenation of these two operands
    if len(operands) == 2:
        possibleResults.append(operands[0] * operands[1])
        possibleResults.append(operands[0] + operands[1])
        possibleResults.append(int(str(operands[0]) + str(operands[1])))
        return possibleResults

    # If there are more than two operands left, replace the first two operands in the list with operated results
    additionOperands = []
    additionOperands.append(operands[0] + operands[1])
    multiplicationOperands = []
    multiplicationOperands.append(operands[0] * operands[1])
    concatenationOperands = []
    concatenationOperands.append(int(str(operands[0]) + str(operands[1])))

    for i in range(2, len(operands)):
        additionOperands.append(operands[i])
        multiplicationOperands.append(operands[i])
        concatenationOperands.append(operands[i])

    # Find the possible results for the new set of operands where the first operation has been performed
    possibleResults = possibleResults + findPossibleResults(additionOperands)
    possibleResults = possibleResults + findPossibleResults(multiplicationOperands)
    possibleResults = possibleResults + findPossibleResults(concatenationOperands)

    # Return all possible results
    return possibleResults

# Function for checking if a calibration is good
def checkCalibration(calibration):
    
    # First, split the calibration with ":" to separate operands and the expected result
    separatedContents = calibration.split(":")
    expectedResult = int(separatedContents[0])

    # Split the second part of separated contents from spaces to find all operands
    operandsString = separatedContents[1].split()
    operands = [int(operand) for operand in operandsString]

    # Find all possible results if operands are multiplied and added together
    possibleResults = findPossibleResults(operands)

    # If the expexted result is in the list of possible results, calibration is good
    if expectedResult in possibleResults:
        return expectedResult

    # If the expected result is not in the list of possible results, calibration is bod
    return 0

# Read the input file
calibrationFile = open("calibrations.txt","r")
potentialCalibrations = calibrationFile.read().splitlines()

# Loop over all calibrations and calculate check sum of good calibrations
checkSum = 0
for calibration in potentialCalibrations:
    checkSum = checkSum + checkCalibration(calibration)

# Print the checksum to console
print("Checksum of all calibrations is {}".format(checkSum))
