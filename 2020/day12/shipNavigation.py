#!/usr/local/bin/python3

# Advent of code puzzle 12-1
# Find the location of the ship after following instructions from navigation computer

# Advent of code puzzle 12-2
# Find the location of the ship after following non-misunderstood instructions

# Check what movement for the ship is required using the given navigation instruction
def decodeInstruction(instruction, currentDirection):

    # First are movement instructions. These move ship to a given direction
    if instruction[0] == "N" or (instruction[0] == "F" and currentDirection == "N"):
        return (0,instruction[1],currentDirection)

    if instruction[0] == "S" or (instruction[0] == "F" and currentDirection == "S"):
        return (0,-instruction[1],currentDirection)

    if instruction[0] == "E" or (instruction[0] == "F" and currentDirection == "E"):
        return (instruction[1],0,currentDirection)

    if instruction[0] == "W" or (instruction[0] == "F" and currentDirection == "W"):
        return (-instruction[1],0,currentDirection)

    # If the ship does not move, it turns.
    directions = ["N","E","S","W"]
    directionIndex = directions.index(currentDirection)

    if instruction[0] == "R":
        directionIndex = directionIndex + int(instruction[1]/90)
        if directionIndex >= len(directions):
            directionIndex = directionIndex - len(directions)

    if instruction[0] == "L":
        directionIndex = directionIndex - int(instruction[1]/90)
        if directionIndex < 0:
            directionIndex = directionIndex + len(directions)

    return (0,0,directions[directionIndex])

# Decode the navigation instruction using waypoint interpretation
def decodeWaypointInstruction(instruction, wayPointNorth, wayPointEast):

    # First in the movement instruction. Moves the ship towars waypoint
    if instruction[0] == "F":
        return (wayPointNorth*instruction[1], wayPointEast*instruction[1], wayPointNorth, wayPointEast)

    # All the other instructions move the waypoint. First the simple movements
    if instruction[0] == "N":
        return (0, 0, wayPointNorth + instruction[1], wayPointEast)

    if instruction[0] == "E":
        return (0, 0, wayPointNorth, wayPointEast + instruction[1])

    if instruction[0] == "S":
        return (0, 0, wayPointNorth - instruction[1], wayPointEast)

    if instruction[0] == "W":
        return (0, 0, wayPointNorth, wayPointEast - instruction[1])

    # Finally the rotations. Check how north changes in the rotation
    directions = ["N","E","S","W"]
    directionIndex = 0

    if instruction[0] == "R":
        directionIndex = directionIndex + int(instruction[1]/90)
        if directionIndex >= len(directions):
            directionIndex = directionIndex - len(directions)

    if instruction[0] == "L":
        directionIndex = directionIndex - int(instruction[1]/90)
        if directionIndex < 0:
            directionIndex = directionIndex + len(directions)

    # If north changes to east, east becomes south
    if directions[directionIndex] == "E":
        return (0, 0, -wayPointEast, wayPointNorth)

    # If north changes to south, east becomes west
    if directions[directionIndex] == "S":
        return (0, 0, -wayPointNorth, -wayPointEast)

    # If north becomes west, east becomes north
    if directions[directionIndex] == "W":
        return (0, 0, wayPointEast, -wayPointNorth)

    # If north stays as north, waypoint does not change
    return (0, 0, wayPointNorth, wayPointEast)

#############################
##       Main program      ##
#############################

# Read the input file
navigationFile = open("shipDirections.txt","r")
navigationInstructionsRaw = navigationFile.readlines()

# Process the raw lines to get an easy-to-use format
navigationInstructions = []
for line in navigationInstructionsRaw:
    command = line[0]
    number = int(line[1:-1])
    navigationInstructions.append((command,number))

# Go through all the navigation instruction and see where we end up
currentPositionNorth = 0
currentPositionEast = 0
currentDirection = "E"
for instruction in navigationInstructions:
    decodedMovement = decodeInstruction(instruction, currentDirection)
    currentPositionNorth = currentPositionNorth + decodedMovement[0]
    currentPositionEast = currentPositionEast + decodedMovement[1]
    currentDirection = decodedMovement[2]

# Print the answer to the problem!
print("The final position of the ship is ({:d},{:d})".format(currentPositionNorth, currentPositionEast))
print("Manhattan distance from beginning is {:d}".format(abs(currentPositionNorth) + abs(currentPositionEast)))

# Go through all the navigation instruction with waypoint interpretation and see where we end up
currentPositionNorth = 0
currentPositionEast = 0
wayPointNorth = 1
wayPointEast = 10
for instruction in navigationInstructions:
    decodedMovement = decodeWaypointInstruction(instruction, wayPointNorth, wayPointEast)
    currentPositionNorth = currentPositionNorth + decodedMovement[0]
    currentPositionEast = currentPositionEast + decodedMovement[1]
    wayPointNorth = decodedMovement[2]
    wayPointEast = decodedMovement[3]

# Print the answer to the problem!
print("Oops! Need to use waypoints!")
print("The final position of the ship is ({:d},{:d})".format(currentPositionNorth, currentPositionEast))
print("Manhattan distance from beginning is {:d}".format(abs(currentPositionNorth) + abs(currentPositionEast)))
