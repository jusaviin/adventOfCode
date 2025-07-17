#!/usr/local/bin/python3

# Advent of code puzzle 5-1
# Check that page ordering follows the page ordering rules

# Advent of code puzzle 5-2
# Correct the cases where rules are not properly followed

# Read the input file
pageOrderFile = open("pageRules.txt","r")

# First we need to separate the rules and ordered pages
pageOrderRules = []
pageOrderPrints = []

addToRules = True
for line in pageOrderFile:

    # There is an empty line in the file that separeted rules from prints
    if line == "\n":
        addToRules = False
        continue

    # Note: strip removes new line and other invisible characters
    if addToRules:
        pageOrderRules.append(line.strip())
    else:
        pageOrderPrints.append(line.strip())

# Now that we have our orders ready, create all rules that would violate the prints and check that no violating rules exist in the rules table
checkSum = 0
correctedCheckSum = 0
for thisPrint in pageOrderPrints:
    isGoodPrint = True
    printedPages = thisPrint.split(",")
    for iEarlyPage in range(0, len(printedPages)):
        for iLatePage in range(iEarlyPage+1, len(printedPages)):
            violatingRule = printedPages[iLatePage] + "|" + printedPages[iEarlyPage]
            # If we found a rule that violates the order, this is a bad print and we can stop checking the remaining pages
            if violatingRule in pageOrderRules:
                isGoodPrint = False
                break

        # If we have already found a violating rule, no need to check the rest
        if not isGoodPrint:
            break

    # If no page ordering rules are violated, add the middle page number to checksum
    if isGoodPrint:
        checkSum = checkSum + int(printedPages[int(len(printedPages)/2)])
    
    # If the print is not good, fix the ordering 
    else:
        adjustmentMade = True

        # Keep going through the rules until no more adjustments need to be made
        while adjustmentMade:
            adjustmentMade = False
        
            for iEarlyPage in range(0, len(printedPages)):
                for iLatePage in range(iEarlyPage+1, len(printedPages)):
                    violatingRule = printedPages[iLatePage] + "|" + printedPages[iEarlyPage]
                    # If we found a rule that violates the order, swap the location of the two numbers in the array
                    if violatingRule in pageOrderRules:
                        swapper = printedPages[iEarlyPage]
                        printedPages[iEarlyPage] = printedPages[iLatePage]
                        printedPages[iLatePage] = swapper
                        adjustmentMade = True

        # When no more adjustments are made, the print order has been fixed
        # We can now calculate check sum
        correctedCheckSum = correctedCheckSum + int(printedPages[int(len(printedPages)/2)])

# Print the answers to the console
print("Checksum for correct orders is {}".format(checkSum))
print("Checksum for incorrect orders after correction is {}".format(correctedCheckSum))
