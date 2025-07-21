#!/usr/local/bin/python3

# Advent of code puzzle 13-1
# Find the cheapest way to win the most prizes from the claw machines

# Advent of code puzzle 13-2
# Do the same with shifted prize coordinates

def solveClawMachine(buttonAX, buttonAY, buttonBX, buttonBY, prizeX, prizeY):
    
    # Correct the coordinate position for prizes
    prizeX = prizeX + 10000000000000
    prizeY = prizeY + 10000000000000

    # The pair of equations to solve is
    # a*Ax + b*Bx = Px
    # a*Ay + b*By = Py
    # => a = (Px - b*Bx) / Ax
    # => ((Px - b*Bx) / Ax) * Ay + b*By = Py
    # => (Px * Ay / Ax) - (b * Bx * Ay / Ax) + b * By = Py
    # => b (By - Bx * Ay / Ax) = Py - (Px * Ay / Ax)
    # => b = (Py - (Px * Ay / Ax)) / (By - Bx * Ay / Ax)
    # => b = (Py * Ax - Px * Ay) / (By * Ax - Bx * Ay)

    # Solving the equation analytically gives floating point numbers as the result
    floatPushB = (prizeY * buttonAX - prizeX * buttonAY) / (buttonBY * buttonAX - buttonBX * buttonAY)
    floatPushA = (prizeX - floatPushB * buttonBX) / buttonAX

    # As you can only push buttons integer amount of times, round these to nearest integer
    nPushB = round(floatPushB)
    nPushA = round(floatPushA)

    # In principle we could get a negative result. This is not allowed
    if nPushA < 0 or nPushB < 0:
        return 0

    # Check that the integer result works
    if nPushA * buttonAX + nPushB * buttonBX != prizeX:
        return 0

    if nPushA * buttonAY + nPushB * buttonBY != prizeY:
        return 0

    # If integer result works, return the amount of tokens in takes to win the prize
    return nPushA * 3 + nPushB

# Read the input file
clawMachineFile = open("clawMachines.txt","r")
clawMachineInstructions = clawMachineFile.read().splitlines()

# We need to find the parameters for each claw machine from the input file
# Do this and check how many tokens each claw machine requires to win the prize
nTokens = 0
for clawMachine in clawMachineInstructions:
    if "A" in clawMachine:
        numberString = clawMachine.split("+")
        xString = numberString[1].split(",")
        buttonAX = int(xString[0])
        buttonAY = int(numberString[2])

    if "B" in clawMachine:
        numberString = clawMachine.split("+")
        xString = numberString[1].split(",")
        buttonBX = int(xString[0])
        buttonBY = int(numberString[2])

    if "Prize" in clawMachine:
        numberString = clawMachine.split("=")
        xString = numberString[1].split(",")
        prizeX = int(xString[0])
        prizeY = int(numberString[2])

        # Since the order is always buttonA, buttonB, prize, at this point we can solve this claw machine
        nTokens = nTokens + solveClawMachine(buttonAX, buttonAY, buttonBX, buttonBY, prizeX, prizeY)

                
print("You need {} tokens to win all possible prizes".format(nTokens))
