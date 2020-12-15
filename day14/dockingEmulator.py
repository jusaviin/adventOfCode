#!/usr/local/bin/python3

# Advent of code puzzle 14-1
# Calculate the sum of memory registers after docking program has run

# Advent of code puzzle 14-2
# Calculate the sum of memory registers after docking program has run using ruleset 2

# Get the bit in bitIndex of an integer
def checkBit(integerValue, bitIndex):

    # Explanation on what is happening here
    #  1) (1 << bitIndex): Move bit 1 to the index we need to check.
    #     For example 1 << 3 would produce a mask 1000
    #  2) integerValue & (1 << bitIndex): Do a bitwise and for the checked number.
    #     As every other bit in the mask is zero, in the and only the one in checked
    #     index can be one after the operation is done
    #  3) >> bitIndex: Move the obtained 1 or zero to position 0. For example,
    #     a check result 1000 >> 3 would produce 1 and the bit is moved 3 spaces.
    return (integerValue & (1 << bitIndex)) >> bitIndex

# Apply bit mask to given value
def applyMask(value, mask):
    newValue = ""

    # It is assumed that everything larger that can be kept in 36 bit register is overflowing
    for i in range(0,36):

        # Ones and zeros in the mask are kept as is
        if mask[i] == "0" or mask[i] == "1":
            newValue = newValue + mask[i]

        # Other values are taken as in the input value
        else:
            newValue = newValue + str(checkBit(value,35-i))

    # Convert the binary number to integer and return the value
    return int(newValue,2)

# Find all the registers that are written using rule 2
def getAllRegisters(memoryRegister, mask):

    allRegisters = [""]

    # The memory register is 36 bits deep
    for i in range(0,36):

        # If mask has X, both 0 and 1 are filled to the register address list
        if mask[i] == "X":
            registersWithZero = [register for register in allRegisters]
            for iRegister in range(0,len(registersWithZero)):
                registersWithZero[iRegister] = registersWithZero[iRegister] + "0"
            for iRegister in range(0,len(allRegisters)):
                allRegisters[iRegister] = allRegisters[iRegister] + "1"
            allRegisters = allRegisters + registersWithZero

        # Ones are read directly from the mask
        elif mask[i] == "1":
            for iRegister in range(0,len(allRegisters)):
                allRegisters[iRegister] = allRegisters[iRegister] + mask[i]

        # For value 0, the bit from register address is retained
        else:
            for iRegister in range(0,len(allRegisters)):
                allRegisters[iRegister] = allRegisters[iRegister] + str(checkBit(memoryRegister,35-i))

    # Once we have decoded the mask, we need to get materialize the floating X:s
    return allRegisters

# Interpret a line from the docking program
def interpretLine(line, mask):

    # Split the command and value
    tokens = line.split(" = ")

    # If the command in mask, update the bitmask
    if tokens[0] == "mask":
        return (tokens[1], -1, -1)

    # If the command in memory update, find register and value
    memoryCommand = tokens[0].split("[")
    memoryRegister = int(memoryCommand[1][0:-1])
    memoryValue = int(tokens[1])

    # Before setting the value to register, we need to apply bitmask
    memoryValue = applyMask(memoryValue, mask)

    # Return the register and value after applying mask
    return(mask, memoryRegister, memoryValue)

# Interpret a line from the docking program using ruleset 2
def interpretLineRule2(line, mask):

    # Split the command and value
    tokens = line.split(" = ")

    # If the command in mask, update the bitmask
    if tokens[0] == "mask":
        return (tokens[1], {})

    # If the command in memory update, find register and value
    memoryCommand = tokens[0].split("[")
    memoryRegister = int(memoryCommand[1][0:-1])
    memoryValue = int(tokens[1])

    # Find the list of memory registers allowed by the mask:
    allRegisters = getAllRegisters(memoryRegister, mask)

    # Add the same memory value to all registers in the list
    memoryDictionary = {}
    for register in allRegisters:
        memoryDictionary[register] = memoryValue

    # Return the unchanged mask and the memory dictionary
    return (mask, memoryDictionary)

#############################
##       Main program      ##
#############################

# Read the input file
programFile = open("dockingProgram.txt","r")
dockingProgram = programFile.readlines()

# Initialize a memory array
memory = {}
mask = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

# Loop over the operations and execute them
for line in dockingProgram:
    (mask, memoryRegister, memoryValue) = interpretLine(line, mask)
    if memoryRegister >= 0:
        memory[memoryRegister] = memoryValue

# Calculate the sum of values in the memory
sum = 0
for register in memory:
    sum = sum + memory[register]

# Print the answer!
print("In the end, the sum of values in memory is {:d}".format(sum))

# Repeat the exercise with rule 2:
newMemory = {}
newMask = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

# Loop over the operations and execute them
for line in dockingProgram:
    (mask, memoryDictionary) = interpretLineRule2(line, mask)
    for register in memoryDictionary:
        newMemory[register] = memoryDictionary[register]

# Calculate the sum of values in the memory
sum = 0
for register in newMemory:
    sum = sum + newMemory[register]

# Print the answer!
print("In the end, the sum of values in memory using rule 2 is {:d}".format(sum))
