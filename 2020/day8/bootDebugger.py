#!/usr/local/bin/python3

# Advent of code puzzle 8-1
# Find the accumulator value before entering infinite loop

# Advent of code puzzle 8-2
# Find the accumulator value after fixing the infinite loop

# Find the accumulator value when the code finishes or loops
def findAccumulatorAtFinish(bootList, switchIndex):

    currentLine = 0
    visitedLines = []
    accumulator = 0

    # Go though lines until all lines are done
    while currentLine < len(bootList):

        # If we have already been at this line, return the value of accumulator and the information that the program did not finish
        if visitedLines.count(currentLine) == 1:
            return (accumulator,False)

        # Number to be added to current line number
        lineAdder = 1

        # Find the commend in current line
        command = bootList[currentLine][0]
        number = bootList[currentLine][1]

        # Switch exactly one nop or jmp command to the other
        if currentLine == switchIndex:
            if command == "jmp":
                command = "nop"
            elif command == "nop":
                command = "jmp"

        # Do the action prompted by the command
        if command == "acc":
            accumulator = accumulator + number
        elif command == "jmp":
            lineAdder = number

        # Add current line to the visited lines list and move to the next line
        visitedLines.append(currentLine)
        currentLine = currentLine + lineAdder

    # If the program finishes natularly, return the value of the accumulator and information that the program did finish
    return (accumulator,True)

# Read the input file
debugFile = open("bootSequence.txt","r")
bootSequence = debugFile.readlines()

# Put the boot sequence in an easy-to-use list
bootList = []
for line in bootSequence:
    commands = line.split()
    bootList.append((commands[0],int(commands[1])))

# Get the accumulator value when infinite loop starts
accumulatorAtInfiniteLoop = findAccumulatorAtFinish(bootList, -1)[0]
print("When infinite loop starts, the value of accumulator is {:d}".format(accumulatorAtInfiniteLoop))

# Try to swap exactly one command and see if the program finishes
for iCommand in range(0,len(bootList)):
    (accumulatorAtFinish,finished) = findAccumulatorAtFinish(bootList, iCommand)
    if finished:
        print("Program finishes when changing the command in line {:d}!".format(iCommand))
        print("The value of accumulator in this case is {:d}".format(accumulatorAtFinish))
