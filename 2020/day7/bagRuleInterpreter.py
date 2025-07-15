#!/usr/local/bin/python3

# Advent of code puzzle 7-1
# Find out how many bag colors may contain shiny gold bag

# Advent of code puzzle 7-2
# Find out how many bags must be inside a shiny gold bag

# Find if a bag of innerColor is allowed in a bag of outerColor basedon rulebook
def isBagAllowed(rulebook, outerColor, innerColor):

    # Find the rule for outerColor from the dictionary
    try:

        # If the rule is empty list, no other bags are allowed in this bag
        if rulebook[outerColor] == []:
            return False

        # If the list is not empty, check if innerColor is directly allowed in this bag
        for rule in rulebook[outerColor]:
            if rule[0] == innerColor:
                return True

        # If the inner color is not directly allowed, check again for each allowed bags
        isAllowed = False
        for rule in rulebook[outerColor]:
            isAllowed = isAllowed or isBagAllowed(rulebook, rule[0], innerColor)

        return isAllowed


    # If outerColor is not found from the dictionary, it is assumed that it cannot contain other bags
    except KeyError:
        return False

    # We should never be here. Print warning message and return False
    print("There is an error in the isBagAllowed function! Please fix it!!")
    return False

# Find how many bags must be inside a bag of color bagColor based on rulebook
def howManyBags(rulebook, bagColor, multiplier):

    # Find the rule for bagColor from the dictionary
    try:

        # If the rule is empty list, no other bags are needed inside this bag
        if rulebook[bagColor] == []:
            return 0

        # If the list is not empty, check if innerColor is directly allowed in this bag
        totalBags = 0
        for rule in rulebook[bagColor]:
            totalBags = totalBags + rule[1]*multiplier + howManyBags(rulebook, rule[0], rule[1]*multiplier)

        return totalBags


    # If bagColor is not found from the dictionary, return -1 to indicate this
    except KeyError:
        return -1

    # We should never be here. Print warning message and return -2
    print("There is an error in the howManyBags function! Please fix it!!")
    return -2

# Read the input file
bagRuleFile = open("bagRules.txt","r")
allRules = bagRuleFile.readlines()

# Put all the rules into a dictionary:
rulebook = {}
for rule in allRules:

    # Split the rule into the bag for which the rule is (0), and which bags are allowed in (1)
    rulePieces = rule.split(" bags contain ")
    allowedBags = rulePieces[1].split(",")

    # Format the bags that are allowed by the rule into a list
    allowedList = []
    for allowedBag in allowedBags:
        bagPieces = allowedBag.split()
        if(bagPieces[0] != "no"):
            allowedList.append((bagPieces[1] + " " + bagPieces[2],int(bagPieces[0])))

    # Insert the rule to the dictionary
    rulebook[rulePieces[0]] = allowedList

# Find the color of all bags that may contain a shiny gold bag
nBagsThatMayContainShinyGoldBag = 0
for color in rulebook:
    if isBagAllowed(rulebook, color, "shiny gold"):
        nBagsThatMayContainShinyGoldBag = nBagsThatMayContainShinyGoldBag + 1

# Print the answer!
print("There are {:d} colors that may contain a shiny gold bag!".format(nBagsThatMayContainShinyGoldBag))

# Check how many bags are needed inside a shiny golden black
nBagsInsideShinyGoldBag = howManyBags(rulebook,"shiny gold",1)

# Print the answer!
print("There must be {:d} bags inside a shiny gold bag!".format(nBagsInsideShinyGoldBag))
