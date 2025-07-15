#!/usr/local/bin/python3

# Advent of code puzzle 5-1
# Find highest seat ID from boarding passes

# Advent of code puzzle 5-2
# Find my sead ID, the one missing from the list

# Find the row/column number from given string
# It is assumed that there are 2^len(seatString) rows
# Basically we are converting a binary number to decimal
def findSeat(seatString, minIndex):
    
    # Find the number of possible seats where the seat can be
    nSeats = 2**len(seatString)
    
    # If the seat is on the back, move the minimum possible seat index
    if(seatString[0] == "B" or seatString[0] == "R"):
        minIndex = minIndex + (nSeats/2)
        
    # If there is only one possible index left, return that
    if(nSeats/2 == 1):
        return minIndex
        
    # If there are several possible indices left, do the search again
    return findSeat(seatString[1:], minIndex)


# Read the input file
boardingPassFile = open("boardingPasses.txt","r")
boardingPasses = boardingPassFile.readlines()

# Find the row and column from boarding pass information
seats = []
for boardingPass in boardingPasses:
    row = findSeat(boardingPass[0:7],0)
    column = findSeat(boardingPass[7:10],0)
    seats.append((row,column))

# Find the largest and smallest seat ID:s among boarding pass information. Also tabulate all ID:s
bigID = 0
smallID = 1000
allIDs = []
for row,column in seats:
    thisID = row*8 + column
    if(thisID > bigID):
        bigID = thisID
        
    if(thisID < smallID):
        smallID = thisID
        
    allIDs.append(thisID)

# Check the largest and smallest seat ID
print("Largest ID number is: {:.0f}".format(bigID))
print("Smallest ID number is: {:.0f}".format(smallID))

# Find the missing ID. That must be my seat!
mySeat = -1
for seat in range(int(smallID),int(bigID)):

    seatFound = False
    
    # Check if the current seat ID is in the list of boarding passes
    for idNumber in allIDs:
        if(seat == idNumber):
            seatFound = True
            break
    
    # If the seat is missing from the list, it must be my seat!
    if not seatFound:
        mySeat = seat
        break

# Print my seat ID :)
print("My seat ID is: {:.0f}".format(mySeat))
