#!/usr/local/bin/python3

# Advent of code puzzle 14-1
# Find the location of robots and calculate the security score based on that

# Advent of code puzzle 14-2
# Find the time step in which most of the robots arrange themselves into a Christmas tree position

# Check if there is unusually high density of robots in this time step
def checkHighDensity(robotsInBox, nRobots):
    
    # If any quadrant or middle region has more than 40% of total robots, we have a region of high density
    for nRobotInBox in robotsInBox:
        if nRobotInBox / nRobots > 0.4:
            return True

    # If there are more than 70% of robots in any two adjacent quadrants, we also have regions of high density
    # Quadrants are numbered as:  0 2
    #                             1 3
    if (robotsInBox[0] + robotsInBox[1]) / nRobots > 0.7:
        return True
    if (robotsInBox[0] + robotsInBox[2]) / nRobots > 0.7:
        return True
    if (robotsInBox[3] + robotsInBox[1]) / nRobots > 0.7:
        return True
    if (robotsInBox[3] + robotsInBox[1]) / nRobots > 0.7:
        return True

    # If none of these conditions hold, we are unlikely to have a Christmas tree formation in the system
    return False

# Find a cluster around the seed location
def findCluster(robotLocations, clusterSeed):

    # Add all robots at the cluster seed to the current cluster
    thisCluster = []

    # Remove all duplicate entries from the robot location list
    while clusterSeed in robotLocations:
        seedLocation = robotLocations.index(clusterSeed)
        robotLocations.pop(seedLocation)
        thisCluster.append(clusterSeed)

    # Check all four main directions and see if cluster continues there
    if (clusterSeed[0] + 1, clusterSeed[1]) in robotLocations:
        thisCluster = thisCluster + findCluster(robotLocations, (clusterSeed[0] + 1, clusterSeed[1]))
    if (clusterSeed[0] - 1, clusterSeed[1]) in robotLocations:
        thisCluster = thisCluster + findCluster(robotLocations, (clusterSeed[0] - 1, clusterSeed[1]))
    if (clusterSeed[0], clusterSeed[1] + 1) in robotLocations:
        thisCluster = thisCluster + findCluster(robotLocations, (clusterSeed[0], clusterSeed[1] + 1))
    if (clusterSeed[0], clusterSeed[1] - 1) in robotLocations:
        thisCluster = thisCluster + findCluster(robotLocations, (clusterSeed[0], clusterSeed[1] - 1))

    # Return the list of all the robots in the cluster
    return thisCluster
      

# Find the largest cluster from a list of locations
def findLargestCluster(robotLocations):

    # Loop over robot locations until all locations have been mapped to a cluster of robots
    thisCluster = []
    largestCluster = []

    while len(robotLocations) > 0:
        
        # Find the cluster that starts from the first location in the list
        thisCluster = findCluster(robotLocations, robotLocations[0])

        # If this cluster has more robots then any previous cluster, this is the largest one
        if len(thisCluster) > len(largestCluster):
            largestCluster = thisCluster

    # When all therobots are clustered, return the largest cluster
    return largestCluster


# Check if the robots are in a Christmas tree shape
def checkChristmasTreeShape(robotLocations):

    # Christmas tree shape means that there is a single robot in the top row, three below that, five below that and so on
    # Christmas tree can be of any size, as long as it follows that pattern
    # Overlap of robots does not matter, as long as together they will form a Christmas tree shape

    # Start by removing duplicates and sorting the robot locations by the y-coordinate
    sortedRobotLocations = list(set(robotLocations))
    sortedRobotLocations = sorted(sortedRobotLocations, key=lambda point: (point[1], point[0]))
    distinctLocations = len(sortedRobotLocations)

    # Check if the count of different locations matches expected counts from the Christmas tree
    treeGrower = 3
    treeSize = 1
    outline = []

    # Keep trying new tree sizes until we find a good one
    # Remember also indices of entries that make the outline of the tree
    while treeSize != distinctLocations:
        
        # If the expected size is larger than the number of distinct locations, this cannot be a Christmas tree shape
        if treeSize > distinctLocations:
            return False

        # Grow the tree to the next possible size and try again
        outline.append(treeSize)
        treeSize = treeSize + treeGrower
        outline.append(treeSize - 1)
        treeGrower = treeGrower + 2

    # If we survive the while loop without returning False, we have good amount of robot locations
    # Next we need to check the shape of the tree 

    # Check the location of the crown of the Christmas tree
    crownX = sortedRobotLocations[0][0]
    crownY = sortedRobotLocations[0][1]

    # Go through the entries in the outline of the tree and check if they are in expected locations
    adderX = -1
    adderY = 1
    isEven = True
    for outlineSpot in outline:

        # Check that the next outline location is in correct index
        if sortedRobotLocations[outlineSpot] != (crownX + adderX, crownY + adderY):
            return False

        # If this is true, update the expected index location
        if isEven:
            adderX = adderX * -1
            isEven = False
        else:
            adderX = (adderX + 1) * -1
            adderY = adderY + 1
            isEven = True
        
    # If all the entries in the outline of the tree are good, we have a Christmas tree!
    return True

# Read the input file
robotConfigurationFile = open("robotConfiguration.txt","r")
encryptedRobotConfigurations = robotConfigurationFile.read().splitlines()

# Define the size of the lobby the robots are patrolling
lobbyWidth = 101    # Test = 11, Full = 101
lobbyHeight = 103   # Test = 7,  Full = 103

# The configuration file tells the robot location and speed at start
# Decode the configuration from the input file
robotConfigurations = []
for configuration in encryptedRobotConfigurations:
    locationAndSpeed = configuration.split()

    # Get the location of the robot
    bothNumbers = locationAndSpeed[0].split("=")
    number = bothNumbers[1].split(",")
    locationX = int(number[0])
    locationY = int(number[1])

    # Get the velocity of the robot
    bothNumbers = locationAndSpeed[1].split("=")
    number = bothNumbers[1].split(",")
    speedX = int(number[0])
    speedY = int(number[1])

    robotConfigurations.append((locationX, locationY, speedX, speedY))

# Once the robot configurations have been decoded, check the security sum at timestep 100
robotsInQuadrant = [0, 0, 0, 0]
quadrantLimitX = int(lobbyWidth/2)
quadrantLimitY = int(lobbyHeight/2)
for configuration in robotConfigurations:

    # Determine where the robot is in 100 time steps
    newLocationX = (configuration[0] + configuration[2]*100)%lobbyWidth
    newLocationY = (configuration[1] + configuration[3]*100)%lobbyHeight

    # Add the robot location to the quadrant the robot is now located
    if newLocationX < quadrantLimitX:
        if newLocationY < quadrantLimitY:
            robotsInQuadrant[0] = robotsInQuadrant[0] + 1
        elif newLocationY > quadrantLimitY:
            robotsInQuadrant[1] = robotsInQuadrant[1] + 1
    elif newLocationX > quadrantLimitX:
        if newLocationY < quadrantLimitY:
            robotsInQuadrant[2] = robotsInQuadrant[2] + 1
        elif newLocationY > quadrantLimitY:
            robotsInQuadrant[3] = robotsInQuadrant[3] + 1

# Once all the robots have been moved and their final quadrant is determined, calculate the security score
securityScore = 1
for nRobots in robotsInQuadrant:
    securityScore = securityScore * nRobots
print("The final security score is {}".format(securityScore))

# Then, loop over different configurations until we find a Christmas tree shape
timeStep = -1
christmasTreeShape = False
nRobots = len(robotConfigurations)
middleBoxLowLimit = int(lobbyHeight/4)
middleBoxUpLimit = int(lobbyHeight - lobbyWidth/4)
middleBoxLeftLimit = int(lobbyWidth/4)
middleBowRightLimit = int(lobbyWidth - lobbyWidth/4)
while not christmasTreeShape:
    robotLocations = []
    robotsInBox = [0, 0, 0, 0, 0]

    # Update the time step
    timeStep = timeStep + 1

    # We know from website that the answer is smaller than 1000000 time steps
    if(timeStep > 1000000):
        break

    # Keep the user entertained
    if timeStep%100000 == 0:
        print("We are in time step {}".format(timeStep))
    
    # Determine where the all the robots are in the current time step
    for configuration in robotConfigurations:
        newLocationX = (configuration[0] + configuration[2]*timeStep)%lobbyWidth
        newLocationY = (configuration[1] + configuration[3]*timeStep)%lobbyHeight
        robotLocations.append((newLocationX, newLocationY))

        # Add the robot location to the boxes where the robot is now located
        if newLocationX < quadrantLimitX:
            if newLocationY < quadrantLimitY:
                robotsInBox[0] = robotsInBox[0] + 1
            elif newLocationY > quadrantLimitY:
                robotsInBox[1] = robotsInBox[1] + 1
        elif newLocationX > quadrantLimitX:
            if newLocationY < quadrantLimitY:
                robotsInBox[2] = robotsInBox[2] + 1
            elif newLocationY > quadrantLimitY:
                robotsInBox[3] = robotsInBox[3] + 1
        
        if newLocationX > middleBoxLeftLimit:
            if newLocationX < middleBowRightLimit:
                if newLocationY > middleBoxLowLimit:
                    if newLocationY < middleBoxUpLimit:
                        robotsInBox[4] = robotsInBox[4] + 1

    # Clustering is very slow, so check if there are areas with higher density of robots before clustering
    #highRobotDensity = checkHighDensity(robotsInBox, nRobots)
    #if not highRobotDensity:
    #    continue

    # Find the largest cluster of robots among all the robots and check if more than half the robots belong to it
    largestCluster = findLargestCluster(robotLocations)
    if(len(largestCluster) < nRobots/2):
        continue

    # Print if we find a big cluster
    print("Big cluster found in time step {}".format(timeStep))

    # Check if we have obtained a Christmas tree shape
    christmasTreeShape = checkChristmasTreeShape(largestCluster)


print("Christmas tree is obtained in time step {}".format(timeStep))

