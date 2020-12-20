#!/usr/local/bin/python3

# Advent of code puzzle 16-1
# Find the error rate in neighboring tickets

# Advent of code puzzle 16-1
# Determine which field is which

from ticket import Ticket

# Decode lines for ticket validation numbers
def findTicketValidationNumbers(ticketInfo):

    # Create an empty dictionary for holding the validation information
    validationNumbers = {}

    # From each line in the ticketInfo, extract the validationNumbers
    for infoLine in ticketInfo:
        tokens = infoLine.split(": ")
        ranges = tokens[1].split(" or ")
        allowedRanges = []
        for range in ranges:
            numbers = range.split("-")
            allowedRanges.append((int(numbers[0]),int(numbers[1])))

        # Add the valid ragnes to the dictionary
        validationNumbers[tokens[0]] = allowedRanges

    return validationNumbers

#############################
##       Main program      ##
#############################

# Read the input file
ticketFile = open("ticketNumbers.txt","r")
ticketInfo = ticketFile.readlines()

# Find empty lines from ticket file. Different types of information are stored in different sections
emptyLines = []
for i in range(0,len(ticketInfo)):

    # If there is empty line, the information given for one passport ends and the new begins from next line
    if(ticketInfo[i] == "\n"):
        emptyLines.append(i)

# Extract different pieces of information from the file
validationNumbers = findTicketValidationNumbers(ticketInfo[0:emptyLines[0]])
myTicket = Ticket(ticketInfo[emptyLines[1]-1])

# Calculate error rate and tabulate valid tickets
thisErrorRate = 0
errorRate = 0
validTickets = []
for infoLine in ticketInfo[emptyLines[1]+2:len(ticketInfo)]:
    thisTicket = Ticket(infoLine)
    thisErrorRate = thisTicket.errorRate(validationNumbers)
    if thisTicket.isValid(validationNumbers):
        validTickets.append(thisTicket)
    errorRate = errorRate + thisErrorRate

# Assume that my own ticket is valid
validTickets.append(myTicket)

# Print the answer!
print("Total error rate in nearby tickets is {:d}".format(errorRate))

# Find all possible indices for each rule
possibleIndices = {}
for key in validationNumbers:
    allIndices = [i for i in range(0,len(validationNumbers))]
    possibleIndices[key] = allIndices
    for thisTicket in validTickets:
        notGood = thisTicket.impossibleIndices(validationNumbers[key])
        for index in notGood:
            try:
                possibleIndices[key].remove(index)
            except ValueError:
                dummy = "Nothing needs to happen here"

# If there is only one possible index for a rule, remove that from other rules
# Continue until there is only one possible index left
maxLenght = 20
skipKeys = []
while maxLenght > 1:
    for key in possibleIndices:

        # If we have already applied a rule for a key, this is skipped in future iterations
        if skipKeys.count(key) > 0:
            continue

        # If there is only one possibility for an index for a key, remove this as a possibility from other keys
        if len(possibleIndices[key]) == 1:
            skipKeys.append(key)
            removedIndex = possibleIndices[key][0]
            for innerKey in possibleIndices:
                if skipKeys.count(innerKey) > 0:
                    continue

                try:
                    possibleIndices[innerKey].remove(removedIndex)
                except ValueError:
                    dummy = "Nothing needs to happen here"


    # After we have gone through all the keys, define maximum possible index array length
    maxLenght = 0
    for key in possibleIndices:
        if len(possibleIndices[key]) > maxLenght:
            maxLenght = len(possibleIndices[key])

# The answer to the question is to multiply from my ticket the destination fields
checkSum = myTicket.getValue(possibleIndices["departure location"][0]) * myTicket.getValue(possibleIndices["departure station"][0]) * myTicket.getValue(possibleIndices["departure platform"][0]) * myTicket.getValue(possibleIndices["departure track"][0]) * myTicket.getValue(possibleIndices["departure date"][0]) * myTicket.getValue(possibleIndices["departure time"][0])
print("The answer to the sencond part is {:d}".format(checkSum))
