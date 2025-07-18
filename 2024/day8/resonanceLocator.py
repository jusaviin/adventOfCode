#!/usr/local/bin/python3

# Advent of code puzzle 8-1
# Locate antinodes of antennas. Same types of antennas in a line make an antinode to a location where one antenna is twice as far away as the other antenna

# Advent of code puzzle 8-2
# Actually, all location in direct line are good

# Find antinodes based on problem 1 definition
def findAllAntinodes(antennaLocations):
    allAntiNodes = []
    nAntennas = len(antennaLocations)

    # We need at least two antennas to create antinodes
    if nAntennas < 2:
        return allAntiNodes

    # Calculate the antinodes from all pairs of antennas
    for i in range(0, nAntennas):
        for j in range(i+1, nAntennas):
            rowDifference = abs(antennaLocations[i][0] - antennaLocations[j][0])
            columnDifference = abs(antennaLocations[i][1] - antennaLocations[j][1])

            if antennaLocations[i][0] < antennaLocations[j][0]:
                antiNodeRow0 = antennaLocations[i][0] - rowDifference
                antiNodeRow1 = antennaLocations[j][0] + rowDifference
            else:
                antiNodeRow0 = antennaLocations[i][0] + rowDifference
                antiNodeRow1 = antennaLocations[j][0] - rowDifference

            if antennaLocations[i][1] < antennaLocations[j][1]:
                antiNodeColumn0 = antennaLocations[i][1] - columnDifference
                antiNodeColumn1 = antennaLocations[j][1] + columnDifference
            else:
                antiNodeColumn0 = antennaLocations[i][1] + columnDifference
                antiNodeColumn1 = antennaLocations[j][1] - columnDifference

            
            allAntiNodes.append((antiNodeRow0, antiNodeColumn0))
            allAntiNodes.append((antiNodeRow1, antiNodeColumn1))

    return allAntiNodes
                
# Find antinodes based on problem 2 definition
def findLinearAntinodes(antennaLocations, mapHeight, mapWidth):
    linearAntinodes = []
    nAntennas = len(antennaLocations)

    # We need at least two antennas to create antinodes
    if nAntennas < 2:
        return linearAntinodes

    # Calculate the antinodes from all pairs of antennas
    for i in range(0, nAntennas):
        for j in range(i+1, nAntennas):

            rowDifference =  antennaLocations[j][0] - antennaLocations[i][0]
            columnDifference = antennaLocations[j][1] - antennaLocations[i][1]
           
            counter = 0
            for iRow in range(antennaLocations[i][0], -1, -rowDifference):
                iColumn = antennaLocations[i][1] - counter*columnDifference
                if iColumn >= 0:
                    if iColumn < mapWidth:
                        linearAntinodes.append((iRow, iColumn))
                counter = counter + 1

            counter = 1
            for iRow in range(antennaLocations[i][0]+rowDifference, mapHeight, rowDifference):
                iColumn = antennaLocations[i][1] + counter*columnDifference
                if iColumn >= 0:
                    if iColumn < mapWidth:
                        linearAntinodes.append((iRow, iColumn))
                counter = counter + 1

    return linearAntinodes


# Read the input file
antennaMapFile = open("antennaMap.txt","r")
antennaMap = antennaMapFile.read().splitlines()

# Make a list of all possible character that can signify a location of an antenna
from string import ascii_lowercase, ascii_uppercase
antennaTypes = ascii_lowercase + ascii_uppercase + "0123456789"

# Loop over all the places in the map and create a dictionary of all antennas we find
mapWidth = len(antennaMap[0])
mapHeight = len(antennaMap)
antennaLocationByType = {}
for iRow in range(0, mapHeight):
    for iColumn in range(0, mapWidth):
        if antennaMap[iRow][iColumn] in antennaTypes:
            if antennaMap[iRow][iColumn] in antennaLocationByType:
                # If the key is in the dictionary, add antenna location to the list
                antennaLocationByType[antennaMap[iRow][iColumn]].append((iRow, iColumn))
            else:
                # If the key is not in the dictionary, make a new list for this key
                antennaLocationByType[antennaMap[iRow][iColumn]] = [(iRow, iColumn)]

# Loop over all kinds of antennas and calculate their antinodes
allAntinodes = []
linearAntinodes = []
epsilon = 0.1
for antennaType, antennaLocation in antennaLocationByType.items():
 
    # Find possible locations of antinode:
    possibleAntinodes = findAllAntinodes(antennaLocation)

    # Add acceptable antinodes to the all antinodes list
    for potentialAntinode in possibleAntinodes:

        # Check that the antinode is on the map
        if potentialAntinode[0] < 0:
            continue
        if potentialAntinode[0] >= mapHeight:
            continue
        if potentialAntinode[1] < 0:
            continue
        if potentialAntinode[1] >= mapWidth:
            continue

        # Only add the antinode to the list if that location is not already on there
        if not potentialAntinode in allAntinodes:
            allAntinodes.append(potentialAntinode)

    # Do the calculation also with linear antinode definition
    possibleAntinodes = findLinearAntinodes(antennaLocation, mapHeight, mapWidth)

    # Add antinodes that are not already in linear antinodes list to that list
    for potentialAntinode in possibleAntinodes:

        # Only add the antinode to the list if that location is not already on there
        if not potentialAntinode in linearAntinodes:
            linearAntinodes.append(potentialAntinode)

#print(sorted(linearAntinodes, key=lambda tup: tup[0]))

# Print the number of antinodes in the end
print("Antennas produce a total of {} antinodes within the map boundaries.".format(len(allAntinodes)))
print("Antennas produce a total of {} linear antinodes within the map boundaries.".format(len(linearAntinodes)))
