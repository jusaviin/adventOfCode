#!/usr/local/bin/python3

# Advent of code puzzle 18-1
# Solve math problems using left to right order of operations

# Advent of code puzzle 18-2
# Solve math problems doing additions before multiplications

# Find the innermost pair of parantheses
def findInnermostParantheses(openParantheses, closeParantheses):

    openIndex = openParantheses[len(openParantheses)-1]
    for closeIndex in closeParantheses:
        if closeIndex > openIndex:
            return(openIndex,closeIndex)

# Solve all the math operations from left to right
def solveLeftToRight(expression):

    operations = expression.split()

    result = int(operations[0])

    # There are only two operations, addition and multiplication
    for i in range(1, len(operations), 2):
        if operations[i] == "+":
            result = result + int(operations[i+1])
        else:
            result = result * int(operations[i+1])

    return result

# Solve all the math operations starting from addition
def solveAdditionFirst(expression):

    operations = expression.split()

    result = int(operations[0])

    newOperations = []

    # Perform all additions
    for i in range(1, len(operations), 2):
        if operations[i] == "+":
            result = result + int(operations[i+1])
        else:
            newOperations.append(result)
            result = int(operations[i+1])

    # If there were no multiplications, return the result
    if len(newOperations) == 0:
        return result

    # If there were at least one multiplication, add current result to newOperations array
    newOperations.append(result)

    # Perform all multiplications
    result = newOperations[0]
    for i in range(1, len(newOperations)):
        result = result * newOperations[i]

    # Return the final result
    return result

# Solve the input math problem using alternative arithmetics
def solveExpression(expression, mathMode):

    # To determine the order of operations, find the positions of parantheses
    openParantheses = []
    closeParantheses = []
    for i in range(0,len(expression)):
        if expression[i] == "(":
            openParantheses.append(i)
        if expression[i] == ")":
            closeParantheses.append(i)

    # If there are no parantheses, evaluate expressions
    if len(openParantheses) == 0:

        # "Left to right" mode
        if mathMode == "leftToRight":
            return solveLeftToRight(expression)

        # "Addition first" mode
        else:
            return solveAdditionFirst(expression)

    # Solve the expression in the innermost parantheses
    innerMostParantheses = findInnermostParantheses(openParantheses, closeParantheses)
    innerResult = solveExpression(expression[innerMostParantheses[0]+1 : innerMostParantheses[1]], mathMode)

    # Replace the innermost parantheses with the expression result
    newExpression = expression[0:innerMostParantheses[0]] + str(innerResult) + expression[innerMostParantheses[1]+1:]

    # Solve again the reduced expression
    return solveExpression(newExpression, mathMode)

#############################
##       Main program      ##
#############################

# Read the input file
homeworkFile = open("homework.txt","r")
allProblems = homeworkFile.readlines()

# Solve all lines and calculate the sum of answers
sum = 0
sum2 = 0
for problem in allProblems:
    sum = sum + solveExpression(problem, "leftToRight")
    sum2 = sum2 + solveExpression(problem, "additionFirst")

# Print the answer!
print("The sum of all problems is {:d}".format(sum))
print("The sum of all problems doing addition first is {:d}".format(sum2))
