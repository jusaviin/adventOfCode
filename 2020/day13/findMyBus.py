#!/usr/local/bin/python3

# Advent of code puzzle 13-1
# Find the bus that comes first after arrivat at terminal

# Advent of code puzzle 13-2
# Find a timestamp from which each bus leaves following a given time interval

# Find the list of timestamps corresponding to times when buses leave in given intervals
def findCoolTimes(buses, timeIntervals, maxBus, allowedTimes):

    # Find the timestamp that is equivalent to the initial situation
    # The next time stamp all the buses leave at the same time is the product of all bus numbers
    # For the bigIncrement, we assume that the timestamps for allowed bus leaving times have been solven for n-1 buses
    maximumTimestamp = 1
    bigIncrement = 1
    for index in range(0,maxBus):
        maximumTimestamp = maximumTimestamp * buses[index]

        if(index == maxBus - 2):
            bigIncrement = maximumTimestamp

    # Loop over all the possible timestamps that can lead to buses leaving at given intervals
    timestamp = 0
    timestampBig = -bigIncrement
    coolTimes = []
    while  timestamp < maximumTimestamp:

        # In previous iteration we have checked all possibilities in bigIncrement time interval
        timestampBig = timestampBig + bigIncrement

        # Only check allowed times known from previous iteration
        for checkTime in allowedTimes:
            coolTime = True
            timestamp = timestampBig + checkTime

            # All the buses must leave with defined intervals from each other for time to be cool
            for index in range(0,maxBus):
                if (timestamp + timeIntervals[index]) % buses[index] != 0:
                    coolTime = False
                    break

        # If the buses leave with given intervals, remember the time
        if coolTime:
            coolTimes.append(timestamp)

    # Return an array of timestamps leading to buses leaving on allowed time intervals
    return coolTimes


#############################
##       Main program      ##
#############################

# Read the input file
busFile = open("busSchedule.txt","r")
busNotes = busFile.readlines()

# Extract the information from my notes
arrivalTime = int(busNotes[0])

busesInNotes = busNotes[1].split(",")
buses = []
timeIntervals = []
originalIndex = -1
for busNumber in busesInNotes:
    originalIndex = originalIndex + 1
    if busNumber == "x":
        continue
    buses.append(int(busNumber))
    timeIntervals.append(originalIndex)

# Now that we know arrival time and bus schedules, check the waiting times for each
waitingTimes = []
for busNumber in buses:
    thisWait = busNumber - (arrivalTime % busNumber)
    waitingTimes.append(thisWait)

# Find the shortest waiting time
shortestTime = arrivalTime
for time in waitingTimes:
    if time < shortestTime:
        shortestTime = time
shortestIndex = waitingTimes.index(shortestTime)

# Print the answer
print("The shortest wait is {:d} minutes for bus {:d}".format(waitingTimes[shortestIndex], buses[shortestIndex]))
print("When you multiply these numbers, you get {:d}".format(waitingTimes[shortestIndex]*buses[shortestIndex]))

# To find the times when buses leave with specified intervals, start narrowing down
# the possible intervals for a smaller group and use this information to restrict
# the options for a larger group. This way the computation time stays reasonable
coolTimes = [0]
for busIndex in range(2, len(buses)+1):

    coolTimes = findCoolTimes(buses, timeIntervals, busIndex, coolTimes)

# Print the answer!
print("Cool things happen at timestamp: {:d}".format(coolTimes[0]))
