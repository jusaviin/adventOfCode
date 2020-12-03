#!/usr/local/bin/python3

# Advent of code puzzle 4-1
# Count the valid passports in a passport file

# Advent of code puzzle 4-2
# Count the valid passports in a passport file with additional constraints

from passport import Passport

# Read the input file
passportFile = open("passports.txt","r")
passportInfo = passportFile.readlines()

# Read all passport information from the file
passportArray = []
myPassport = Passport()
for infoLine in passportInfo:

    # If there is empty line, the information given for one passport ends and the new begins from next line
    if(infoLine == "\n"):
        passportArray.append(myPassport)
        myPassport = Passport()
        
    # When there is no empty line, add the information to current passport
    else:
        myPassport.addInformation(infoLine)

# If the remaining passport is not empty, add it to array
if not(myPassport.isEmpty()):
    passportArray.append(myPassport)

# Calculate the number of valid passport
nValidPassports = 0
for myPassport in passportArray:
    if(myPassport.isValid()):
        nValidPassports = nValidPassports + 1
        
# Print the number of valid passports
print("There are {:d} valid passports".format(nValidPassports))

# Calculate the number of valid passport with additional constraints
nValidPassportsStrict = 0
for myPassport in passportArray:
    if(myPassport.isValidStrict()):
        nValidPassportsStrict = nValidPassportsStrict + 1
        
# Print the number of valid passports
print("There are {:d} strictly valid passports".format(nValidPassportsStrict))
