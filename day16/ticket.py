class Ticket:
    """ Class containing information present in a ticket"""

    def __init__(self, configString = None):
        """ Constructor """
        self.information = []

        if(configString != None):
            self.addInformation(configString)


    def addInformation(self,configString):
        """ Add information to passport. Must be in format key1:value1 key2:value2 ... keyN:valueN"""

        # Split the string on commas
        values = configString.split(",")

        # Loop over key-value pairs
        for value in values:
            self.information.append(int(value))

    def errorRate(self, rules):
        """ Get the ticket error rate based on given rules """

        myErrorRate = 0
        for value in self.information:
            isValid = False
            for key in rules:
                for(minBound, maxBound) in rules[key]:
                    if value >= minBound and value <= maxBound:
                        isValid = True
                        break

                if isValid:
                    break

            if not isValid:
                myErrorRate = myErrorRate + value

        return myErrorRate

    def isValid(self, rules):
        """ Get if the ticket is valid based on given rules """

        for value in self.information:
            isValid = False
            for key in rules:
                for(minBound, maxBound) in rules[key]:
                    if value >= minBound and value <= maxBound:
                        isValid = True
                        break

                if isValid:
                    break

            if not isValid:
                return False

        return True

    def possibleIndices(self, rule):
        """ For a given rule, check which indices fulfill that """

        validIndices = []
        for index in range(0,len(self.information)):
            value = self.information[index]
            for(minBound, maxBound) in rule:
                if value >= minBound and value <= maxBound:
                    validIndices.append(index)

        return validIndices

    def impossibleIndices(self, rule):
        """ For a given rule, check which indices cannot obey that rule """

        invalidIndices = []
        for index in range(0,len(self.information)):
            value = self.information[index]
            isValid = False
            for(minBound, maxBound) in rule:
                if value >= minBound and value <= maxBound:
                    isValid = True

            if not isValid:
                invalidIndices.append(index)

        return invalidIndices

    def getValue(self, index):
        """ For a value from the given index """
        return self.information[index]

    def print(self):
        """ Print the ticket information """
        print(self.information)
