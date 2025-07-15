import re  # Regular expression module needed for some value checks

class Passport:
    """ Class containing information present in a passport"""

    requiredFields = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]
    optionalFields = ["cid"]

    def __init__(self, configString = None):
        """ Constructor """
        self.information = {}
        
        if(configString != None):
            self.addInformation(configString)
                    

    def addInformation(self,configString):
        """ Add information to passport. Must be in format key1:value1 key2:value2 ... keyN:valueN"""
        
        # Split the string on spaces
        valuePairs = configString.split()
        
        # Loop over key-value pairs
        for pair in valuePairs:
            input = pair.split(":")
            self.information[input[0]] = input[1]
            
    def isValid(self):
        """ Check if all the required fields are present in the passport """
        
        for key in self.requiredFields:
            if key in self.information:
                if(self.information[key] == ""):
                    return False
            else:
                return False
                
        return True
        
    def isValidStrict(self):
        """ Check if all the required fields are present in the passport and they have sensible input """
        
        # First check that all required fields exist
        if(self.isValid()):
        
            # If all required fields exist, do sanity checks for each field
            
            # byr (Birth Year) - four digits; at least 1920 and at most 2002.
            try:
                birthYear = int(self.information["byr"])
                
                if(birthYear < 1920):
                    return False
                    
                if(birthYear > 2002):
                    return False
                
            except ValueError:
                # If field is not integer, it is invalid
                return False
            
            
            # iyr (Issue Year) - four digits; at least 2010 and at most 2020.
            try:
                issueYear = int(self.information["iyr"])
                
                if(issueYear < 2010):
                    return False
                    
                if(issueYear > 2020):
                    return False
                
            except ValueError:
                # If field is not integer, it is invalid
                return False
            
            
            # eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
            try:
                expirationYear = int(self.information["eyr"])
                
                if(expirationYear < 2020):
                    return False
                    
                if(expirationYear > 2030):
                    return False
                
            except ValueError:
                # If field is not integer, it is invalid
                return False
            
            
            # hgt (Height) - a number followed by either cm or in:
            # If cm, the number must be at least 150 and at most 193.
            # If in, the number must be at least 59 and at most 76.
            heightString = self.information["hgt"]
            
            # Height in centimeters
            if(heightString[-2:] == "cm"):
                
                try:
                    heightNumber = int(heightString[0:-2])
                
                    if(heightNumber < 150):
                        return False
                    
                    if(heightNumber > 193):
                        return False
                
                except ValueError:
                    # If field is not integer, it is invalid
                    return False
            
            # Height in inches
            elif(heightString[-2:] == "in"):
                
                try:
                    heightNumber = int(heightString[0:-2])
                
                    if(heightNumber < 59):
                        return False
                    
                    if(heightNumber > 76):
                        return False
                
                except ValueError:
                    # If field is not integer, it is invalid
                    return False
             
            # Unknown unit or wrong format
            else:
                return False
            
            
            # hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
            hairColorString = self.information["hcl"]
            
            rule = re.compile('^#[a-f0-9]{6}$')
            
            if not rule.match(hairColorString):
                return False
            
            
            # ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth
            eyeColor = self.information["ecl"]
            
            validEyeColors = ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]
            
            validColorFound = False
            
            for color in validEyeColors:
                if(eyeColor == color):
                    validColorFound = True
                    break
                    
            if not validColorFound:
                return False
                
                
            # pid (Passport ID) - a nine-digit number, including leading zeroes.
            passportID = self.information["pid"]
            
            rule = re.compile('^[0-9]{9}$')
            
            if not rule.match(passportID):
                return False
            
        
        else:
            return False
                
        return True
        
    def isEmpty(self):
        """ Check if there is any information in the passport """
        
        if(len(self.information) == 0):
            return True
        return False
        
    def print(self):
        """ Print the passport information """
        print(self.information)
        
    
