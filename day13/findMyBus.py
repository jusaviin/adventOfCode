#!/usr/local/bin/python3

# Advent of code puzzle 13-1
# Find the bus that comes first after arrivat at terminal

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
for busNumber in busesInNotes:
    if busNumber == "x":
        continue
    buses.append(int(busNumber))

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
