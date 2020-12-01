#!/usr/local/bin/python3

# Advent of code puzzle 1-1
# Find two numbers that add up to 2020 and multiply them

# Advent of code puzzle 1-2
# Find three numbers that add up to 2020 and multiply them

# Find two numbers from an array that add to a given number and return their product
def findSumProduct(array, sum):
    
    # Transform all the numbers to integers
    intArray = [int(i) for i in array]
    
    # Calculate sums of all the numbers and return the product of first instanvce that adds up to a given sum
    for i in range(0,len(intArray)):
        for j in range(i+1,len(intArray)):
            if(intArray[i]+intArray[j] == sum):
                return intArray[i]*intArray[j]
            
    # If no numbers sum up to the given sum, return -1
    return -1
    
# Find three numbers from an array that add to a given number and return their product
def findSumProduct3(array, sum):
    
    # Transform all the numbers to integers
    intArray = [int(i) for i in array]
    
    # Calculate sums of all the numbers and return the product of first instanvce that adds up to a given sum
    for i in range(0,len(intArray)):
        for j in range(i+1,len(intArray)):
            for k in range(j+1,len(intArray)):
                if(intArray[i]+intArray[j]+intArray[k] == sum):
                    return intArray[i]*intArray[j]*intArray[k]
            
    # If no numbers sum up to the given sum, return -1
    return -1

# Read the input file
numberFile = open("numberInput1.txt","r")
numberArray = numberFile.readlines()

# Find the product of two numbers adding up to 2020
product2020 = findSumProduct(numberArray,2020)

# Find the product of three numbers adding up to 2020
productOfThree = findSumProduct3(numberArray,2020)

# Print the products to console!
print("Product of two: {:d}".format(product2020))
print("Product of three: {:d}".format(productOfThree))
