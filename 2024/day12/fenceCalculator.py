#!/usr/local/bin/python3

# Advent of code puzzle 12-1
# Calculate the cost of fencing all different crops in the field

# Advent of code puzzle 12-2
# For new cost estimate, need to find the number of sides in each region

# Find the number of sides in a given region
def findNumberOfSides(region):

    numberOfSides = 0

    # First, count the number of vertical sides. For this, sort the region coordinates
    sortedRegion = sorted(region, key=lambda point: (point[1], point[0]))

    # Now we can go through the elements one by one, and determine from the surroundings if we are in a vertical side or not
    leftSide = False
    rightSide = False
    for iPlace in range(0, len(sortedRegion)):

        # If the region does not continue to the left of this place, we are on one of the left sides
        if not (sortedRegion[iPlace][0], sortedRegion[iPlace][1] - 1) in region:

            # If the previous position was not in the same left side, increment the side counter
            if not leftSide:
                leftSide = True
                numberOfSides = numberOfSides + 1

        # If the region continues to the left side, we are not on the left sides of the region
        else:
            leftSide = False

        # If the region does not continue to the right of this place, we are on one of the right sides
        if not (sortedRegion[iPlace][0], sortedRegion[iPlace][1] + 1) in region:

            # If the previous position was not in the same right side, increment the side counter
            if not rightSide:
                rightSide = True
                numberOfSides = numberOfSides + 1

        # If the region continues to the right side, we are not on the right sides of the region
        else:
            rightSide = False

        # If we are not in the last place of the region, check the next coordinate
        if iPlace != len(sortedRegion)-1:

            # If the next place is not directly below the current place, reset side counters
            if sortedRegion[iPlace+1][0] != sortedRegion[iPlace][0]+1:
                rightSide = False
                leftSide = False

            # If the column of the place changes, reset side counters
            if sortedRegion[iPlace+1][1] != sortedRegion[iPlace][1]:
                rightSide = False
                leftSide = False

    # Then, count the number of vertical sides. Now we need different sortinf for the points
    sortedRegion = sorted(region, key=lambda point: (point[0], point[1]))

    # Now we can go through the elements one by one, and determine from the surroundings if we are in a vertical side or not
    topSide = False
    bottomSide = False
    for iPlace in range(0, len(sortedRegion)):

        # If the region does not continue to the up of this place, we are on one of the top sides
        if not (sortedRegion[iPlace][0] + 1, sortedRegion[iPlace][1]) in region:

            # If the previous position was not in the same top side, increment the side counter
            if not topSide:
                topSide = True
                numberOfSides = numberOfSides + 1

        # If the region continues to the top side, we are not on the top sides of the region
        else:
            topSide = False

        # If the region does not continue down from this place, we are on one of the bottom sides
        if not (sortedRegion[iPlace][0] - 1, sortedRegion[iPlace][1]) in region:

            # If the previous position was not in the same bottom side, increment the side counter
            if not bottomSide:
                bottomSide = True
                numberOfSides = numberOfSides + 1

        # If the region continues to the bottom side, we are not on the bottom sides of the region
        else:
            bottomSide = False

        # If we are not in the last place of the region, check the next coordinate
        if iPlace != len(sortedRegion)-1:

            # If the next place is not directly right from the current place, reset side counters
            if sortedRegion[iPlace+1][1] != sortedRegion[iPlace][1]+1:
                topSide = False
                bottomSide = False

            # If the row of the place changes, reset side counters
            if sortedRegion[iPlace+1][0] != sortedRegion[iPlace][0]:
                topSide = False
                bottomSide = False

    # Return the number of sides in this region
    return numberOfSides

# Find a perimeter of a given region:
def findPerimeter(region):

    # The current coordinate adds to perimeter if the region does not continue past this coordinate
    perimeter = 0
    for place in region:
        if not (place[0] + 1, place[1]) in region:
            perimeter = perimeter +1
        if not (place[0] - 1, place[1]) in region:
            perimeter = perimeter +1
        if not (place[0], place[1] + 1) in region:
            perimeter = perimeter +1
        if not (place[0], place[1] - 1) in region:
            perimeter = perimeter +1

    # Return the length of the perimeter
    return perimeter

# Find the region to which this index belongs to
def findRegion(fieldMap, iRow, iColumn):

    # Add the current location as one coordinate this region belongs to
    regionCoordinates = [(iRow, iColumn)]

    # Mark that this location has been added to a region
    characterToLookFor = fieldMap[iRow][iColumn]
    fieldMap[iRow][iColumn] = "."

    # Check every direction to see the region can be extanded
    if fieldMap[iRow-1][iColumn] == characterToLookFor:
        regionCoordinates = regionCoordinates + findRegion(fieldMap, iRow-1, iColumn)
    if fieldMap[iRow+1][iColumn] == characterToLookFor:
        regionCoordinates = regionCoordinates + findRegion(fieldMap, iRow+1, iColumn)
    if fieldMap[iRow][iColumn-1] == characterToLookFor:
        regionCoordinates = regionCoordinates + findRegion(fieldMap, iRow, iColumn-1)
    if fieldMap[iRow][iColumn+1] == characterToLookFor:
        regionCoordinates = regionCoordinates + findRegion(fieldMap, iRow, iColumn+1)

    # In the end, return the coordinates of all locations in the region
    return regionCoordinates

# Read the input file
fieldMapFile = open("fieldMap.txt","r")
fieldMapString = fieldMapFile.read().splitlines()

# To make algorithms easier:
#    1) Add a layer of "." characters around the map
#    2) Instead of strings, use arrays of characters
fieldMap = []
topBottomLine = []
for i in range(0, len(fieldMapString[0])+2):
    topBottomLine.append(".")

fieldMap.append(topBottomLine)
for line in fieldMapString:
    mapLine = []
    mapLine.append(".")
    for character in line:
        mapLine.append(character)
    mapLine.append(".")
    fieldMap.append(mapLine)
fieldMap.append(topBottomLine)

# Once we have the input in easier to deal with form, find all regions from the field map
# Loop over all locations in the map
fieldRegions = []
for iRow in range(1, len(fieldMap)-1):
    for iColumn in range(1, len(fieldMap[iRow])-1):

        # If this location is not already part of a documented region, find the region it belongs to
        if fieldMap[iRow][iColumn] != ".":
            fieldRegions.append(findRegion(fieldMap, iRow, iColumn))
            
# Once we have the list of regions, we need to determine the perimeter and area of each region and multiply these together
totalFenceCost = 0
for region in fieldRegions:
    #totalFenceCost = totalFenceCost + findPerimeter(region) * len(region)
    totalFenceCost = totalFenceCost + findNumberOfSides(region) * len(region)

# Print the total fence cost to the console
print("Total cost of the fence is {}".format(totalFenceCost))
