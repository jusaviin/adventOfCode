#!/usr/local/bin/python3

# Advent of code puzzle 9-1
# Compactify the given disk map and calculate check sum

# Advent of code puzzle 9-2
# Similar as before, but move only whole files instead of memory blocks

# Use numpy for efficient index searching
import numpy as np

# Function to decode disk map
def decodeDiskMap(diskMap):
    
    # Go through the disk map and interpret the compressed format
    decodedMap = []
    memoryID = 0
    alternator = False
    for element in diskMap:
        code = int(element)

        # If we are in odd element, add -1 to indicate empty space
        if alternator:
            for i in range(0, code):
                decodedMap.append(-1)
            alternator = False

        # If we are in even element, add memoryID to the memory spaces
        else:
            for i in range(0, code):
                decodedMap.append(memoryID)
            alternator = True
            memoryID = memoryID + 1

    return decodedMap

# Find the first empty space index from an array
def getFirstEmptySpace(decodedMap):
    for i in range(0, len(decodedMap)):
        if decodedMap[i] == -1:
            return i
    return -1

# Find the last space with memory element
def getLastMemorySpace(decodedMap):
    for i in range(len(decodedMap)-1, -1, -1):
        if decodedMap[i] >= 0:
            return i
    return -1

# Find the first empty location with that has certain amount of space
def getFirstEmptyBlockIndex(decodedMap, minSize, maxIndex):
    isGood = False;
    for i in range(0, maxIndex-minSize+1):
        if decodedMap[i] != -1:
            continue
        isGood = True
        for j in range(1, minSize):
            if decodedMap[i+j] != -1:
                isGood = False
                break
        if isGood:
            return i
    return -1

# Function to fragment the disk
def fragmentDisk(decodedMap):

    fragmentedMap = [item for item in decodedMap]
 
    # For fragmenting disk map, we fill empty spaces from the beginning with memory elements from the end
    firstEmpty = getFirstEmptySpace(fragmentedMap)
    lastMemory = getLastMemorySpace(fragmentedMap)

    # Keep swapping elements in the array until all memory elements are before empty spaces
    while lastMemory > firstEmpty:
        fragmentedMap[firstEmpty] = fragmentedMap[lastMemory]
        fragmentedMap[lastMemory] = -1
        firstEmpty = getFirstEmptySpace(fragmentedMap)
        lastMemory = getLastMemorySpace(fragmentedMap)

    return fragmentedMap

# Function to fragment the disk moving full files
def fragmentDiskFullFiles(decodedMap):

    fragmentedMap = np.array([item for item in decodedMap])
    
    # Find the last file index
    lastMemoryID = fragmentedMap.max()

    # Loop over all files and move them to a memory location in a smaller index if there is space
    for memoryID in range(lastMemoryID, 0, -1):

        # Keep the user engaged while the code is running
        if memoryID % 500 == 0:
            print("Fragmenting memory ID {}".format(memoryID))

        memoryLocation = np.where(fragmentedMap == memoryID)[0]
        blockLength = len(memoryLocation)
        emptyIndex = getFirstEmptyBlockIndex(fragmentedMap, blockLength, memoryLocation[0])

        #print("Memory index {} is found in locations {}".format(memoryID, memoryLocation))
        #print("Length of the block is {}".format(blockLength))

        # If we find a block of empty space large enough, do the swap
        if emptyIndex >= 0:
            for i in range(0, blockLength):
                #print("Swapping index {} of the block".format(i))
                #print("Empty indox location is {}".format(emptyIndex+i))
                #print("Memory location is {}".format(memoryLocation[0]+i))
                fragmentedMap[emptyIndex+i] = memoryID;
                fragmentedMap[memoryLocation[0]+i] = -1;

    # After the memory has been fully fragmented, return the fragmented disk map
    return fragmentedMap
                


# Read the input file
diskMapFile = open("diskMap.txt","r")
diskMap = diskMapFile.read().strip()

# Decode the disk map
decodedMap = decodeDiskMap(diskMap)

# Fragment the disk map
fragmentedMap = fragmentDiskFullFiles(decodedMap)

# After fragmenting the map, calculate the checksum
lastMemory = getLastMemorySpace(fragmentedMap)
checksum = 0
for i in range(0, lastMemory+1):
    if fragmentedMap[i] >= 0:
        checksum = checksum + i * fragmentedMap[i]

# Print the checksum to the console
print("Checksum for the fragmented disk is {}".format(checksum))
