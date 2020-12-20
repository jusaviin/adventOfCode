#!/usr/local/bin/python3

# Advent of code puzzle 17-1
# Simulate six time steps of Conway cubes in three dimensions

# Advent of code puzzle 17-2
# Simulate six time steps of Conway cubes in four dimensions

# Get the number of neighboring cubes that are active
def getActiveNeighbors(cubeStates, x, y, z):

    # Check all the 26 neighboring states from the given coordinate
    nActiveNeighbors = 0
    for xx in range(x-1,x+2):
        for yy in range(y-1,y+2):
            for zz in range(z-1,z+2):

                # Only look at neighbors, skip the given coordinate
                if xx == x and yy == y and zz == z:
                    continue

                # Check if the neighbor is active
                coordinate = "({:d},{:d},{:d})".format(xx,yy,zz)
                try:
                    if cubeStates[coordinate] == "#":
                        nActiveNeighbors = nActiveNeighbors + 1
                except KeyError:
                    dummy = "No key means not active cube"

    # Return the number of active neighbors
    return nActiveNeighbors

# Get the number of neighboring cubes that are active
def getActiveNeighbors4D(cubeStates, x, y, z, w):

    # Check all the 26 neighboring states from the given coordinate
    nActiveNeighbors = 0
    for xx in range(x-1,x+2):
        for yy in range(y-1,y+2):
            for zz in range(z-1,z+2):
                for ww in range(w-1,w+2):

                    # Only look at neighbors, skip the given coordinate
                    if xx == x and yy == y and zz == z and ww == w:
                        continue

                    # Check if the neighbor is active
                    coordinate = "({:d},{:d},{:d},{:d})".format(xx,yy,zz,ww)
                    try:
                        if cubeStates[coordinate] == "#":
                            nActiveNeighbors = nActiveNeighbors + 1
                    except KeyError:
                        dummy = "No key means not active cube"

    # Return the number of active neighbors
    return nActiveNeighbors


# Read the initial state and produce a dictionary of coordinates
def readInitialState(cubeInitialState):

    # Dictionary for the cube states
    cubeStates = {}

    # Go through the coordinates one by one:
    for y in range(0,len(cubeInitialState)):
        for x in range(0,len(cubeInitialState[y])-1):
            coordinate = "({:d},{:d},0)".format(x,-y)
            cubeStates[coordinate] = cubeInitialState[y][x]

    # Return the state coordinates
    return cubeStates

# Read the initial state and produce a dictionary of coordinates
def readInitialState4D(cubeInitialState):

    # Dictionary for the cube states
    cubeStates = {}

    # Go through the coordinates one by one:
    for y in range(0,len(cubeInitialState)):
        for x in range(0,len(cubeInitialState[y])-1):
            coordinate = "({:d},{:d},0,0)".format(x,-y)
            cubeStates[coordinate] = cubeInitialState[y][x]

    # Return the state coordinates
    return cubeStates

#############################
##       Main program      ##
#############################

# Read the input file
cubeFile = open("cubeInitialState.txt","r")
cubeInitialState = cubeFile.readlines()

# Get a distionary of cube states
cubeStates = readInitialState(cubeInitialState)
cubeStates4D = readInitialState4D(cubeInitialState)

# Initialize the initial size of the region where activated cubes can be found
minX = 0
maxX = len(cubeInitialState[0]) - 2
minY = -len(cubeInitialState) + 1
maxY = 0
minZ = 0
maxZ = 0
minW = 0
maxW = 0

# Make a dictionary for updated cube states
newCubeStates = {}
newCubeStates4D = {}

# Simulate six time steps of cube activations
for iStep in range(0,6):

    # First, update the ranges from where activated cubes can be found
    minX = minX - 1
    maxX = maxX + 1
    minY = minY - 1
    maxY = maxY + 1
    minZ = minZ - 1
    maxZ = maxZ + 1
    minW = minW - 1
    maxW = maxW + 1

    # Next, go though all the coordinates that might be activated
    for x in range(minX, maxX+1):
        for y in range(minY, maxY+1):
            for z in range(minZ, maxZ+1):

                # Determine the activation of the cube in the current coordinate
                coordinate = "({:d},{:d},{:d})".format(x,y,z)
                try:
                    thisValue = cubeStates[coordinate]
                except KeyError:
                    thisValue = "."

                # Get the number of active neighbors
                nActiveNeighbors = getActiveNeighbors(cubeStates,x,y,z)

                # Determine the new value in the coordinate based on given rules
                newValue = "."

                # If the cube is active and 2 or 3 neighbors are active, it remains active
                if thisValue == "#":
                    if nActiveNeighbors == 2 or nActiveNeighbors == 3:
                        newValue = "#"

                # The the cube is not active exactly 3 neighbors are active, it becomes active
                else:
                    if nActiveNeighbors == 3:
                        newValue = "#"

                # Add the new coordinate to updated dictionary
                newCubeStates[coordinate] = newValue

                for w in range(minW, maxW+1):

                    # Determine the activation of the cube in the current coordinate
                    coordinate = "({:d},{:d},{:d},{:d})".format(x,y,z,w)
                    try:
                        thisValue = cubeStates4D[coordinate]
                    except KeyError:
                        thisValue = "."

                    # Get the number of active neighbors
                    nActiveNeighbors = getActiveNeighbors4D(cubeStates4D,x,y,z,w)

                    # Determine the new value in the coordinate based on given rules
                    newValue = "."

                    # If the cube is active and 2 or 3 neighbors are active, it remains active
                    if thisValue == "#":
                        if nActiveNeighbors == 2 or nActiveNeighbors == 3:
                            newValue = "#"

                    # The the cube is not active exactly 3 neighbors are active, it becomes active
                    else:
                        if nActiveNeighbors == 3:
                            newValue = "#"

                    # Add the new coordinate to updated dictionary
                    newCubeStates4D[coordinate] = newValue

    # After all the states are gone through, copy the new coordinates to state dictionary
    for key in newCubeStates:
        cubeStates[key] = newCubeStates[key]

    for key in newCubeStates4D:
        cubeStates4D[key] = newCubeStates4D[key]

# Calculate the number of active cubes after six simulation steps
nActiveCubes = 0
for key in cubeStates:
    if cubeStates[key] == "#":
        nActiveCubes = nActiveCubes + 1

# Print the answer!
print("After six simulation steps, there are {:d} active cubes.".format(nActiveCubes))

# Calculate the number of active cubes after six simulation steps in 4D
nActiveCubes = 0
for key in cubeStates4D:
    if cubeStates4D[key] == "#":
        nActiveCubes = nActiveCubes + 1

# Print the answer!
print("After six simulation steps in 4D, there are {:d} active cubes.".format(nActiveCubes))
