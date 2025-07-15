#!/usr/local/bin/python3

# Advent of code puzzle 10-1
# Find the joltage distribution of your adapters

# Advent of code puzzle 10-2
# Find the number of configurations your adapters can be used

# Find the maximum difference between two numbers in sortedList
def findMaxDifference(sortedList, groundJoltage, deviceJoltage):

    maxDifference = 0

    for index in range(0, len(sortedList)-1):
        difference = sortedList[index+1] - sortedList[index]
        if difference > maxDifference:
            maxDifference = difference

    if maxDifference < (deviceJoltage - sortedList[len(sortedList)-1]):
        maxDifference = deviceJoltage - sortedList[len(sortedList)-1]
    if maxDifference < (sortedList[0] - groundJoltage):
        maxDifference = sortedList[0] - groundJoltage

    return maxDifference


# Get the distribution of differences between numbers in outputJoltages list
# The ground joltage corresponds to joltage to which the first adapter is attached
# deviceJoltageDifference is the joltage difference between the last adapter and device
def getDifferenceDistribution(outputJoltages, groundJoltage, deviceJoltage):

    # Create a list for holding the distribution of differences
    maxDifference = findMaxDifference(outputJoltages, groundJoltage, deviceJoltage)
    differenceDistribution = [0 for i in range(0,maxDifference+1)]

    # Fill the distribution of joltages
    joltageDifference = outputJoltages[0] - groundJoltage
    differenceDistribution[joltageDifference] = differenceDistribution[joltageDifference]+1

    for index in range(0, len(outputJoltages)-1):
        joltageDifference = outputJoltages[index+1] - outputJoltages[index]
        differenceDistribution[joltageDifference] = differenceDistribution[joltageDifference]+1

    joltageDifference = deviceJoltage - outputJoltages[len(outputJoltages)-1]
    differenceDistribution[joltageDifference] = differenceDistribution[joltageDifference]+1

    return differenceDistribution

# Find number of allowed configuration recursively from a small list
def findNAllowedConfigurations(outputJoltages):

    # If try to remove one or more adapters and see if the configuration is still allowed
    # Critical adapters (first and last index) are never removed
    # This is kind of dirty and not generalizable, but works for this problem
    allowedCount = 1
    groundJoltage = outputJoltages[0]
    deviceJoltage = outputJoltages[len(outputJoltages)-1]
    for i in range(1,len(outputJoltages)-1):
        element = outputJoltages[i]
        newList = [thisJoltage for thisJoltage in outputJoltages]
        newList.remove(element)
        if findMaxDifference(newList, groundJoltage, deviceJoltage) <= 3:
            allowedCount = allowedCount + 1
        for j in range(i+1,len(outputJoltages)-1):
            newList = [thisJoltage for thisJoltage in outputJoltages]
            element = outputJoltages[i]
            newList.remove(element)
            element = outputJoltages[j]
            newList.remove(element)
            if findMaxDifference(newList, groundJoltage, deviceJoltage) <= 3:
                allowedCount = allowedCount + 1
            for k in range(j+1,len(outputJoltages)-1):
                newList = [thisJoltage for thisJoltage in outputJoltages]
                element = outputJoltages[i]
                newList.remove(element)
                element = outputJoltages[j]
                newList.remove(element)
                element = outputJoltages[k]
                newList.remove(element)
                if findMaxDifference(newList, groundJoltage, deviceJoltage) <= 3:
                    allowedCount = allowedCount + 1
                for l in range(k+1,len(outputJoltages)-1):
                    newList = [thisJoltage for thisJoltage in outputJoltages]
                    element = outputJoltages[i]
                    newList.remove(element)
                    element = outputJoltages[j]
                    newList.remove(element)
                    element = outputJoltages[k]
                    newList.remove(element)
                    element = outputJoltages[l]
                    newList.remove(element)
                    if findMaxDifference(newList, groundJoltage, deviceJoltage) <= 3:
                        allowedCount = allowedCount + 1


    return allowedCount



# Find the number of allowed adapter configurations
def findAllAllowedConfigurations(outputJoltages, groundJoltage):

    # Find the list of adapters where the joltage difference to previous or following
    # adapter is 3 jolt. We know that these adapters are needed in all possible configurations
    criticalAdapters = []
    for index in range(1, len(outputJoltages)-1):
        joltageDifferenceNext = outputJoltages[index+1] - outputJoltages[index]
        joltageDifferencePrevious = outputJoltages[index] - outputJoltages[index-1]
        if joltageDifferenceNext == 3 or joltageDifferencePrevious == 3:
            criticalAdapters.append(index)

    # The first case is spacial, it starts from a ground joltage instead of a joltage in the list
    testList = [groundJoltage]
    testList = testList + outputJoltages[0:criticalAdapters[0]+1]
    allowedConfigurations = findNAllowedConfigurations(testList)

    # In the following cases, both starting and ending joltage come from the list
    for index in range(0, len(criticalAdapters)-1):
        testList = outputJoltages[criticalAdapters[index]:criticalAdapters[index+1]+1]
        if index == len(criticalAdapters)-2:
            print(testList)
        allowedConfigurations = allowedConfigurations * findNAllowedConfigurations(testList)

    # The last case is also special. That needs to be added to the total count
    testList = outputJoltages[criticalAdapters[len(criticalAdapters)-1]:outputJoltages[len(outputJoltages)-1]]
    allowedConfigurations = allowedConfigurations * findNAllowedConfigurations(testList)

    return allowedConfigurations

# Read the input file
joltageFile = open("adapterJolts.txt","r")
outputJoltagesRaw = joltageFile.readlines()

# Convert the sequence to numbers
outputJoltages = [int(i) for i in outputJoltagesRaw]

# Sort the list
outputJoltages.sort()

# Find the joltage differences
joltageDifferences = getDifferenceDistribution(outputJoltages, 0, outputJoltages[len(outputJoltages) - 1] + 3)

# Print the answer!
print("The joltage difference distribution is: ")
print(joltageDifferences)
print("1 and 3 jolt differences multiplied is {:d}".format(joltageDifferences[1]*joltageDifferences[3]))

# Find the number of allowed configuration of adapters:
allowedConfigurations = findAllAllowedConfigurations(outputJoltages, 0)
print(outputJoltages)
print("There are {:d} allowed configurations of adapters.".format(allowedConfigurations))
