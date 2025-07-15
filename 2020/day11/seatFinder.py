#!/usr/local/bin/python3

# Advent of code puzzle 11-1
# Find a stable seating configuration

# Advent of code puzzle 11-2
# Find a stable seating configuration using line of sight

# Find what is in the line of sight
def whatDoISee(seatMap, row, column, nRows, nColumns, stepDown, stepRight):

    # Remember the initial direction
    stepIncrementDown = stepDown
    stepIncrementRight = stepRight

    # Continue on the direction of sight until we hit an object that is not floor
    while True:

        # If we go out of the map, interpret that as we would see just floor
        if row + stepDown >= nRows or row + stepDown < 0:
            return "."

        if column + stepRight >= nColumns or column + stepRight < 0:
            return "."

        # If there is no floor in the direction of the sight, return the object
        if seatMap[row+stepDown][column+stepRight] != ".":
            return seatMap[row+stepDown][column+stepRight]

        # If what we see is floor, continue in straight line
        stepDown = stepDown + stepIncrementDown
        stepRight = stepRight + stepIncrementRight


# Find out what happens to the seat based in line of sight information!
def newCoordinateInLineOFSight(seatMap, row, column, nRows, nColumns):

    # Check what is in the given coordinate
    thisLocation = seatMap[row][column]

    # Check what we see in the line of sight
    adjacentLocations = ""
    for rightStep in range(-1,2):
        for downStep in range(-1,2):
            if rightStep == 0 and downStep == 0:
                continue
            adjacentLocations = adjacentLocations + whatDoISee(seatMap, row, column, nRows, nColumns, downStep, rightStep)

    # If the seat and seats in line of sight are empty, the seat is taken
    if thisLocation == "L":
        if adjacentLocations.count("#") == 0:
            return "#"

    # If the seat is taken, it is vacated if at least five seats in line of sight are taken
    if thisLocation == "#":
        if adjacentLocations.count("#") >= 5:
            return "L"

    # If we are on the floor, it will not change
    return thisLocation

# Get the information about adjacent coordinates for the given coordinate
def getAdjacentInformation(seatMap, row, column, nRows, nColumns):

    adjacentLocations = ""

    # Coordinate above the given coordinate
    if row != 0:
        adjacentLocations = adjacentLocations + seatMap[row-1][column]

    # Coordinate one up and one left from the given coordinate
    if row != 0 and column != 0:
        adjacentLocations = adjacentLocations + seatMap[row-1][column-1]

    # Coordinate to the left from the given coordinate
    if column != 0:
        adjacentLocations = adjacentLocations + seatMap[row][column-1]

    # Coordinate one down and one left from the given coordinate
    if row != nRows-1 and column != 0:
        adjacentLocations = adjacentLocations + seatMap[row+1][column-1]

    # Coordinate below the given coordinate
    if row != nRows-1:
        adjacentLocations = adjacentLocations + seatMap[row+1][column]

    # Coordinate one down and one right from the given coordinate
    if row != nRows-1 and column != nColumns-1:
        adjacentLocations = adjacentLocations + seatMap[row+1][column+1]

    # Coordinate to the right from the given coordinate
    if column != nColumns-1:
        adjacentLocations = adjacentLocations + seatMap[row][column+1]

    # Coordinate one up and one right from the given coordinate
    if row != 0 and column != nColumns-1:
        adjacentLocations = adjacentLocations + seatMap[row-1][column+1]

    return adjacentLocations

# Check a coordinate in map and see if it is vacated
def newCoordinate(seatMap, row, column, nRows, nColumns):

    # Check what is in the given coordinate
    thisLocation = seatMap[row][column]

    # If the seat and adjacent seats are empty, the seat is taken
    if thisLocation == "L":
        adjacentLocations = getAdjacentInformation(seatMap, row, column, nRows, nColumns)
        if adjacentLocations.count("#") == 0:
            return "#"

    # If the seat is taken, it is vacated if at least four adjacent seats are taken
    if thisLocation == "#":
        adjacentLocations = getAdjacentInformation(seatMap, row, column, nRows, nColumns)
        if adjacentLocations.count("#") >= 4:
            return "L"

    return thisLocation

#############################
##       Main program      ##
#############################

# Read the input file
seatFile = open("seatMap.txt","r")
originalMap = seatFile.readlines()

# Remove end line character from the maps and copy it to newMap
newMap = [line[0:-1] for line in originalMap]
seatMap = [line for line in newMap]

# Get the dimensions of the seating array
rows = len(seatMap)
columns = len(seatMap[0])

# Iterate the seat map until it does not change anymore
while True:
    for row in range(0,rows):
        newMap[row] = ""
        for column in range(0,columns):
            newMap[row] = newMap[row] + newCoordinate(seatMap, row, column, rows, columns)

    # If there were no changes we are done!
    if newMap == seatMap:
        break

    # If there were changes in the map, update seatMap and continue
    seatMap = [line for line in newMap]

# After the iterations have finished, count the number of occupied seats
takenSeats = 0
for row in seatMap:
    takenSeats = takenSeats + row.count("#")

# Print the answer!
print("In a stable situation, there are {:d} taken seats.".format(takenSeats))

# Reset the map variables
newMap = [line[0:-1] for line in originalMap]
seatMap = [line for line in newMap]

# Iterate the seat map using line of sight ruleset until it does not change
while True:
    for row in range(0,rows):
        newMap[row] = ""
        for column in range(0,columns):
            newMap[row] = newMap[row] + newCoordinateInLineOFSight(seatMap, row, column, rows, columns)

    # If there were no changes we are done!
    if newMap == seatMap:
        break

    # If there were changes in the map, update seatMap and continue
    seatMap = [line for line in newMap]

# After the iterations have finished, count the number of occupied seats
takenSeats = 0
for row in seatMap:
    takenSeats = takenSeats + row.count("#")

# Print the answer!
print("In a stable situation, there are {:d} taken seats in line of sight.".format(takenSeats))
