#!/usr/local/bin/python3

# Advent of code puzzle 4-1
# Find all XMAS strings from the matrix

# Advent of code puzzle 4-2
# Find MAS strings in X formation

# Check if XMAS is written in the defined direction
def findXmas(array, iRow, iColumn, rowOffset, columnOffset):

    # Check if theword XMAS can fit in the array in the desired direction
    if (iRow + 3*rowOffset) < 0: 
        return 0
    if (iRow + 3*rowOffset) >= len(array): 
        return 0
    if (iColumn + 3*columnOffset) < 0:
        return 0
    if (iColumn + 3*columnOffset) >= len(array[iRow]):
        return 0

    # If XMAS can fit in the desired direction, check the letters
    if not array[iRow + rowOffset][iColumn + columnOffset] == "M":
        return 0
    if not array[iRow + 2*rowOffset][iColumn + 2*columnOffset] == "A":
        return 0
    if not array[iRow + 3*rowOffset][iColumn + 3*columnOffset] == "S":
        return 0

    # If we reach this point, we have found XMAS!
    return 1

# Check all directions from the found "X" letter that could spell XMAS
def countXmas(array, iRow, iColumn):
    xmasCount = findXmas(array, iRow, iColumn, -1, -1)
    xmasCount = xmasCount + findXmas(array, iRow, iColumn, -1, 0)
    xmasCount = xmasCount + findXmas(array, iRow, iColumn, -1, 1)
    xmasCount = xmasCount + findXmas(array, iRow, iColumn, 0, -1)
    xmasCount = xmasCount + findXmas(array, iRow, iColumn, 0, 1)
    xmasCount = xmasCount + findXmas(array, iRow, iColumn, 1, -1)   
    xmasCount = xmasCount + findXmas(array, iRow, iColumn, 1, 0)
    xmasCount = xmasCount + findXmas(array, iRow, iColumn, 1, 1)
    return xmasCount

# Read the input file
xmasFile = open("wordSearchInput.txt","r")
xmasArray = xmasFile.readlines()

# Find the number ow rows and columns in the matrix
nRows = len(xmasArray)
nColumns = len(xmasArray[0])

# Loop over each letter in the matrix and check how many XMAS
# strings start from that letter
xmasCount = 0
for iRow in range(0, nRows):
    for iColumn in range(0, nColumns):
       
        # The first letter of XMAS is X
        if xmasArray[iRow][iColumn] == "X":
            xmasCount = xmasCount + countXmas(xmasArray, iRow, iColumn)

print("XMAS can be found {} times".format(xmasCount))

# Then do the loop again for X shaped MAS strings
xShapedMasCount = 0
mCount = 0
sCount = 0

# The letter A cannot be in the first or last row or column to be in the center of X shape
for iRow in range(1, nRows-1):
    for iColumn in range(1, nColumns-1):

        # The middle letter of the X-shape is A
        if xmasArray[iRow][iColumn] == "A":
        
            # Check the corners of the X-shape have correct letter
            mCount = 0
            sCount = 0
            topLeftLetter = xmasArray[iRow-1][iColumn-1]
            if topLeftLetter == "M":
                mCount = mCount + 1
            elif topLeftLetter == "S":
                sCount = sCount + 1
            topRightLetter = xmasArray[iRow-1][iColumn+1]
            if topRightLetter == "M":
                mCount = mCount + 1
            elif topRightLetter == "S":
                sCount = sCount + 1
            bottomLeftLetter = xmasArray[iRow+1][iColumn-1]
            if bottomLeftLetter == "M":
                mCount = mCount + 1
            elif bottomLeftLetter == "S":
                sCount = sCount + 1
            bottomRightLetter = xmasArray[iRow+1][iColumn+1]
            if bottomRightLetter == "M":
                mCount = mCount + 1
            elif bottomRightLetter == "S":
                sCount = sCount + 1

            # To create X shape, we need to have 2 M:s and 2 S:s
            if mCount == 2:
                if sCount == 2:

                # To have proper MAS strings, opposite corners cannot be the same letter
                    if topLeftLetter != bottomRightLetter:
                        xShapedMasCount = xShapedMasCount + 1


print("There are {} X shaped MAS strings".format(xShapedMasCount))
    
