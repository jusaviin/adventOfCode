#!/usr/local/bin/python3

# Advent of code puzzle 6-1
# Count the spaces the guard occupies behofe she leaves the map

# Advent of code puzzle 6-2
# Add an obstruction such that the guard gets stuck in a loop

# Read the input file
labMapFile = open("labMap.txt","r")
labMap = labMapFile.read().splitlines()

# To begin, we need to find the location of the guard
currentRow = -1
currentColumn = -1
for iRow in range(0, len(labMap)):
    if "^" in labMap[iRow]:
        currentRow = iRow
        currentColumn = labMap[iRow].find("^")
        break

# Once we have located the guard, add the current location to the list of visited locations
startingLocation = (currentRow,currentColumn)
guardLocations = [startingLocation]

# Define the movement of the guardian
rowSpeed = [-1, 0, 1, 0]
columnSpeed = [0, 1, 0, -1]
direction = 0


# Note: Remove duplicate entries from list: myList = list(set(myList))

# Keep moving the guardian until she moves off the map
while True:
    
    # If the movement place the guardian off the map, stop moving the guardian
    if currentRow + rowSpeed[direction] < 0:
        break
    if currentRow + rowSpeed[direction] >= len(labMap):
        break
    if currentColumn + columnSpeed[direction] < 0:
        break
    if currentColumn + columnSpeed[direction] >= len(labMap[currentRow]):
        break

    # If the movement does not drop the guardian off the map, check if there is an obstacle on direction of movement
    if labMap[currentRow + rowSpeed[direction]][currentColumn + columnSpeed[direction]] == "#":
        # If there is an obstacle, change the direction of the guardian
        direction = direction + 1
        if direction == 4:
            direction = 0
    else:
        # If there is no obstacle, move the guardian and add the new location to the locations array
        currentRow = currentRow + rowSpeed[direction]
        currentColumn = currentColumn + columnSpeed[direction]
        if not (currentRow, currentColumn) in guardLocations:
            guardLocations.append((currentRow, currentColumn))

# Once the guard stops moving, print the number of locations the guard visited
print("The guard will be in {} locations!".format(len(guardLocations)))

# In the second part of the problem, we need to add obstacles to the original path of the guard and see that in how many cases out of these, the guard will get stuck in an infinite loop

# The starting location of the guard is not a valid place to place an obstacle, so remove it from the list of locations
guardLocations.remove(startingLocation)

# Then, loop over the allowed locations and try to add an obstacle to those locations. Count the number of cases an infinite loop is created
infiniteLoopCount = 0
debugCount = 0
for obstacleLocation in guardLocations:

    # It takes a while to run the code. Ensure the user that the core is running and not stuck anywhere
    if(debugCount % 100 == 0):
        print("Placing obstacle in location {} out of {} possible ones".format(debugCount, len(guardLocations)+1))
    
    # Define the starting location for the guard
    currentRow = startingLocation[0]
    currentColumn = startingLocation[1]
    direction = 0
    guardLocationAndDirection = [(currentRow, currentColumn, direction)]

    # Keep moving the guard until she falls of the map or gets stuck in an infinite loop
    while True:
    
        # If the movement place the guardian off the map, stop moving the guardian
        if currentRow + rowSpeed[direction] < 0:
            break
        if currentRow + rowSpeed[direction] >= len(labMap):
            break
        if currentColumn + columnSpeed[direction] < 0:
            break
        if currentColumn + columnSpeed[direction] >= len(labMap[currentRow]):
            break


        # If the movement does not drop the guardian off the map, check if there is an obstacle on direction of movement
        if labMap[currentRow + rowSpeed[direction]][currentColumn + columnSpeed[direction]] == "#" or (currentRow + rowSpeed[direction], currentColumn +columnSpeed[direction]) == obstacleLocation:
            # If there is an obstacle, change the direction of the guardian
            direction = direction + 1
            if direction == 4:
                direction = 0
        else:
            # If there is no obstacle, move the guardian and add the new location to the locations array
            currentRow = currentRow + rowSpeed[direction]
            currentColumn = currentColumn + columnSpeed[direction]

        # Check if the guard is stuck in an infinite loop
        if (currentRow, currentColumn, direction) in guardLocationAndDirection:

            # If the guard been in the same location with the same direction before, she has eneter infinite loop
            infiniteLoopCount = infiniteLoopCount + 1
            break

        # If we are not in an infinite loop, add the new location and direction of the guardian to the log
        guardLocationAndDirection.append((currentRow, currentColumn, direction))
    
    debugCount = debugCount+1

# After counting infinite loops, print the results to console
print("Obstacle can be placed in {} locations to create an infinite loop!".format(infiniteLoopCount))
