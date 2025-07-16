#!/usr/local/bin/python3

# Advent of code puzzle 3-1
# Find all instances of mul(X,Y) and print the sum of multiplications

# Advent of code puzzle 3-2
# do() enables multiplication, don't() disables it

# Read the input file
corruptedMemoryFile = open("corruptedMemory.py","r")
corruptedMemory = corruptedMemoryFile.read()

# For exclusion purposes, add do() to the and of memory
# This way the regular expression that finds exclusion regions
# also works at the end of the file
corruptedMemory = corruptedMemory + "do()"

# Input for testing
#testInput = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))don't()bloblobdo()do()do()don't()mul(6,9)do()mul(5,6)don't()mul(10,10)do()"

# Compile a regular expression that finds all instances of mul(x,y)
import re
multiplicityFinder = re.compile(r'mul\([0-9]{1,3},[0-9]{1,3}\)')

# Compile a regular expression that finds a number
numberFinder = re.compile('[0-9]+')

# Compile a regular expression that finds excluded region
# Note: (?s) in the beginning makes * match also end of line
# Note: the ? (.*?) makes the wild card non-greedy
# Note: We needed to add do() to the end of the file such that we
#       find also cases where don't is the last command in the file
exclusionFinder = re.compile(r'(?s)don\'t\(\)(.*?)do\(\)')

# Find excluded area from the regular expression
removedParts = exclusionFinder.findall(corruptedMemory)

# Remove the excluded area from the string
cleanedMemory = corruptedMemory

for exclusion in removedParts:
    cleanedMemory = cleanedMemory.replace(exclusion, "")

# Find all instances of multiplications
allMultiplications = multiplicityFinder.findall(cleanedMemory)

# Perform all multiplications
multiplicationSum = 0
for multiplication in allMultiplications:
    numbers = numberFinder.findall(multiplication)
    product = int(numbers[0]) * int(numbers[1])
    multiplicationSum = multiplicationSum + product

print("Sum of all multiplications is {}".format(multiplicationSum))
