#!/usr/local/bin/python3

# Advent of code puzzle 2-1
# Count valid passwords from the list

# Advent of code puzzle 2-2
# Count valid passwords from the list, different rule

# Count all the valid passwords from the list
def countValidPasswords(passwordList):
    
    # Remember the number of valid passwords
    validPasswords = 0
    
    # Go through all the entries in the list
    for entry in passwordList:
        
        # Split each line into separate tokens
        tokens = entry.split()
        
        # The first token contains the number of times a character must appear in the password
        numbers = tokens[0].split('-')
        
        # Transform all the numbers to integers
        numbers = [int(i) for i in numbers]
        
        # Count the amount of required character in the password
        charCount = tokens[2].count(tokens[1][0])
        
        # If the password meets quality requirements, increment valid password counter by one
        if not(charCount < numbers[0] or charCount > numbers[1]):
            validPasswords = validPasswords + 1
            
    return validPasswords

# Count all the valid passwords from the list using rule 2
def countValidPasswordsRule2(passwordList):
    
    # Remember the number of valid passwords
    validPasswords = 0
    
    # Go through all the entries in the list
    for entry in passwordList:
        
        # Split each line into separate tokens
        tokens = entry.split()
        
        # The first token contains the number of times a character must appear in the password
        numbers = tokens[0].split('-')
        
        # Transform all the numbers to integers
        numbers = [int(i) for i in numbers]
        
        # Get the character used for validation
        validatedCharacter = tokens[1][0]
        
        # Check if the validated character is in the required position of the password string
        if(tokens[2][numbers[0]-1] == validatedCharacter and tokens[2][numbers[1]-1] != validatedCharacter):
            validPasswords = validPasswords + 1
        
        if(tokens[2][numbers[0]-1] != validatedCharacter and tokens[2][numbers[1]-1] == validatedCharacter):
            validPasswords = validPasswords + 1
            
    return validPasswords

# Read the input file
passwordFile = open("passwordInput.txt","r")
passwordArray = passwordFile.readlines()

# Count the valid passwords
validPasswords = countValidPasswords(passwordArray)
validPasswords2 = countValidPasswordsRule2(passwordArray)

# Print the number to console
print("Valid passwords using rule 1: {:d}".format(validPasswords))
print("Valid passwords using rule 2: {:d}".format(validPasswords2))
