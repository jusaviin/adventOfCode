#!/usr/local/bin/python3

# Advent of code puzzle 10-1
# Map all hiking trails from the scorched map and calculate the number of peaks they connect to

# Advent of code puzzle 10-2
# Calculate the number of trails that connect from trailheads to peaks

# Find peaks from all the trails this point belongs to
def findPeakLocations(hikingMap, iRow, iColumn, currentHeight):
    peakLocations = []

    # If we are at the peak, return the location of the peak
    if currentHeight == 9:
        peakLocations.append((iRow, iColumn))
        return peakLocations

    # If we are not at the peak, find peaks from all directions the path continues to
    if iRow - 1 >= 0:
        if hikingMap[iRow-1][iColumn] == currentHeight+1:
            peakLocations = peakLocations + findPeakLocations(hikingMap, iRow-1, iColumn, currentHeight+1)

    if iRow + 1 < len(hikingMap):
        if hikingMap[iRow+1][iColumn] == currentHeight+1:
            peakLocations = peakLocations + findPeakLocations(hikingMap, iRow+1, iColumn, currentHeight+1)
           
    if iColumn - 1 >= 0:
        if hikingMap[iRow][iColumn-1] == currentHeight+1:
            peakLocations = peakLocations + findPeakLocations(hikingMap, iRow, iColumn-1, currentHeight+1)

    if iColumn + 1 < len(hikingMap[iRow]):
        if hikingMap[iRow][iColumn+1] == currentHeight+1:
            peakLocations = peakLocations + findPeakLocations(hikingMap, iRow, iColumn+1, currentHeight+1)

    # Return all the peak locations
    return peakLocations

# Calculate the score for the trailhead in this location
def findTrailheadScore(hikingMap, trailheadRow, trailheadColumn):

    # First find all peak locations
    peakLocations = findPeakLocations(hikingMap, trailheadRow, trailheadColumn, 0)

    # Remove duplicate locations from the list
    peakLocations = list(set(peakLocations))

    # The trailhead score is the number of unique peaks connecting to the peak
    return len(peakLocations)

# Calculate the rating for the upwards pointing trails at this point
def findTrailRating(hikingMap, iRow, iColumn, currentHeight):

    trailRating = 0

    # If we are at the peak, this is the only possible upwards pointing trail
    if currentHeight == 9:
        return 1

    # If we are not at the peak, find the number of possible trails fro mall directions
    if iRow - 1 >= 0:
        if hikingMap[iRow-1][iColumn] == currentHeight+1:
            trailRating = trailRating + findTrailRating(hikingMap, iRow-1, iColumn, currentHeight+1)

    if iRow + 1 < len(hikingMap):
        if hikingMap[iRow+1][iColumn] == currentHeight+1:
            trailRating = trailRating + findTrailRating(hikingMap, iRow+1, iColumn, currentHeight+1)
           
    if iColumn - 1 >= 0:
        if hikingMap[iRow][iColumn-1] == currentHeight+1:
            trailRating = trailRating + findTrailRating(hikingMap, iRow, iColumn-1, currentHeight+1)

    if iColumn + 1 < len(hikingMap[iRow]):
        if hikingMap[iRow][iColumn+1] == currentHeight+1:
            trailRating = trailRating + findTrailRating(hikingMap, iRow, iColumn+1, currentHeight+1)

    # Return the rating of the trail at this location
    return trailRating

# Read the input file
hikingMapFile = open("hikingMap.txt","r")
hikingMap = hikingMapFile.read().splitlines()

# Convert the strings into arrays of numbers
for i in range(0, len(hikingMap)):
    hikingMap[i] = [int(number) for number in hikingMap[i]]

# Loop over the hiking map, and trace all trails starting from trailheads
trailheadScore = 0
trailheadRating = 0
for iRow in range(0, len(hikingMap)):
    for iColumn in range(0, len(hikingMap[iRow])):
        if hikingMap[iRow][iColumn] == 0:
            trailheadScore = trailheadScore + findTrailheadScore(hikingMap, iRow, iColumn)
            trailheadRating = trailheadRating + findTrailRating(hikingMap, iRow, iColumn, 0)

# Print the total trailhead scare
print("Total trailhead score is {}".format(trailheadScore))
print("Total trailhead rating is {}".format(trailheadRating))
