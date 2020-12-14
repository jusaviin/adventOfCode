#!/usr/local/bin/python3

# Advent of code puzzle 13-1
# Find the bus that comes first after arrivat at terminal

# Advent of code puzzle 13-2
# Find a timestamp from which each bus leaves following a given time interval

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

# Find the timestamp at which cool things happen!
timestamp = 0
notThereYet = True
while notThereYet:
    timestamp = timestamp + buses[0]
    notThereYet = False
    
#    for i in range(1,len(buses)):
#        if (timestamp + timeIntervals[i]) % buses[i] != 0:
#            notThereYet = True
#            break;
        
# Print the answer!
print("Cool things happen at timestamp: {:d}".format(timestamp))
