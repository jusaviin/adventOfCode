#!/usr/local/bin/python3

# Advent of code puzzle 2-1
# Check that lines of number are
#   * all decreasing or increasing
#   * adjacent levels differ between 1-3 units

# Advent of code puzzle 2-2
# Also count lists that can be made following the above rules by removing a single digit from the list

# Check that all numbers are decreasing or increasing
def checkDirection(safetyReport):
    if(len(safetyReport) <= 1):
        return True

    # If the first two numbers are the same, check fails
    directionCheck = (safetyReport[1] - safetyReport[0])
    if(directionCheck == 0):
        return False

    # Check if the numbers are increasing or decreasing
    expectedDirection = (directionCheck < 0)

    # Check that all numbers follow the expected direction
    for i in range(1, len(safetyReport)-1):

        # Note that this will accept some cases where the numbers are the same!
        direction = ((safetyReport[i+1] - safetyReport[i]) < 0)

        # If not, return False
        if(expectedDirection != direction):
            return False

    # If the direction is always the same, this check passes
    return True

# Check that consecutive numbers are within 3 units
def checkDifference(safetyReport):
    if(len(safetyReport) <= 1):
        return True

    # Calculate the difference between numbers and require it be less or equal to 3, but larger than 0
    for i in range(0, len(safetyReport)-1):
        if abs(safetyReport[i+1] - safetyReport[i]) > 3:
            return False
        if abs(safetyReport[i+1] - safetyReport[i]) ==  0:
            return False

    # If all the distances are close, return True
    return True

# Get all combinations of numbers where a single digit is removed
def getDampenedLevels(safetyReport):
    dampenedLevels = []

    for i in range (0, len(safetyReport)):
        dampeningIteration = []
        for j in range(0, len(safetyReport)):
            if i != j:
                dampeningIteration.append(safetyReport[j])
        dampenedLevels.append(dampeningIteration)

    return dampenedLevels


# Read the input file
safetyFile = open("safetyReports.txt","r")
safetyReports = safetyFile.readlines()

# Calculate the number of safe reports
numberOfSafeReports = 0
for report in safetyReports:
    safetyLevelStrings = report.split()

    # Split gives strings, and we need numbers
    safetyLevels = [int(item) for item in safetyLevelStrings]

    # Check that direction and difference are good
    directionGood = checkDirection(safetyLevels)

    if directionGood:
        differenceGood = checkDifference(safetyLevels)

        if differenceGood:
            numberOfSafeReports = numberOfSafeReports + 1

    # If the report fails, try to remove one safety level and see if it can now pass
    if not directionGood or not differenceGood:

        # Apply dampener to the safety levels
        dampenedLevels = getDampenedLevels(safetyLevels)

        for dampenedReport in dampenedLevels:

            # Check that direction and difference are good
            directionGood = checkDirection(dampenedReport)

            if directionGood:
                differenceGood = checkDifference(dampenedReport)

                if differenceGood:
                    numberOfSafeReports = numberOfSafeReports + 1
                    break


print("There are {} safe reports".format(numberOfSafeReports))
