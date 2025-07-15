#!/usr/local/bin/python3

# Advent of code puzzle 3-1
# Count the trees in toboggan path

# Advent of code puzzle 3-2
# Check different paths and multiply the found trees

# Count the three in path when for each nDown steps down you take nRight steps right
def countTreesInPath(tobogganMap, nRight, nDown, treeChar):
    
    # Keep in track the current horizontal position
    horizontalPosition = 0
    maxPosition = len(tobogganMap[0])-1 # Need to ignore newline characters. Thus -1 in the end
    
    # Initializa a counter for trees
    treeCounter = 0
    
    # Go through the toboggan path
    for height in range(nDown,len(tobogganMap),nDown):
        
        # Calculate the new horizontal position
        horizontalPosition = horizontalPosition + nRight
        if(horizontalPosition >= maxPosition):
            horizontalPosition = horizontalPosition - maxPosition
        
        # Check if there is a tree in the current position
        if(tobogganMap[height][horizontalPosition] == treeChar):
            treeCounter = treeCounter+1
            
    # Return the number of encountered trees in the path
    return treeCounter

# Read the input file
tobogganFile = open("tobogganMap.txt","r")
tobogganMap = tobogganFile.readlines()

# Count the trees
nTrees = countTreesInPath(tobogganMap, 3, 1, "#")

# Print the answer
print("There are {:d} trees in the path.".format(nTrees))

# Check several paths
allTrees = []
allTrees.append(countTreesInPath(tobogganMap, 1, 1, "#"))
allTrees.append(countTreesInPath(tobogganMap, 3, 1, "#"))
allTrees.append(countTreesInPath(tobogganMap, 5, 1, "#"))
allTrees.append(countTreesInPath(tobogganMap, 7, 1, "#"))
allTrees.append(countTreesInPath(tobogganMap, 1, 2, "#"))

# Multiply them all together
treeProduct = 1
for treeNumber in allTrees:
    treeProduct = treeProduct * treeNumber
print("Product of all paths is {:d}".format(treeProduct))
