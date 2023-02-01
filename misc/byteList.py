
class ByteList:
    """
        Class representing a number of bytes (8-bit values),
        as a ASCII string [0-F]. From this we can parse into (unsigned) integer values.
    """
    def __init__(self):
        self.__byteIndex    = 0
        self.__bitIndex     = 0
        self.stringList     = []    #List of strings for example ["00", "F1", "39", "A0", ...]. Each string representing a byte of data in hex


    def parseItems(self, itemList):
        """
            parsing a bunch of items with form
            [{name:<name>, size:<size>}, ...]
            size is number of bits in field
            and returns a dict of 
            {fieldname:value, ...}
        """     

        for item in itemList:
            item["value"] = self.parseItem(item["size"])


    def parseItem(self, numberOfBits):
        """
            parsing next item in byteStringList, with a given number of bits 
            returns the value parsed as an int


            This is a mess... seems to work though...
        """        

        bitsLeft = numberOfBits

        value = 0

        while (bitsLeft > 0 and self.__byteIndex < len(self.stringList)):
            currentByteValue = int(self.stringList[self.__byteIndex], 16)

    
            if self.__bitIndex > 0:
                #get a binary string with at least 8 chars
                binaryString = bin(currentByteValue)[2:]                    
                    
                binaryString = ("0" * (8 - len(binaryString))) + str(binaryString)


                if bitsLeft >= 8 - self.__bitIndex:
                    #we can take rest
                    bitsLeft -= (8 - self.__bitIndex)

                    value += int(binaryString[self.__bitIndex:8], 2) << bitsLeft 
                
                    self.__byteIndex += 1
                    self.__bitIndex   = 0
                else:
                    tmpValue = int(binaryString[self.__bitIndex : (self.__bitIndex + bitsLeft)], 2)
                    self.__bitIndex += bitsLeft 
                    bitsLeft = 0
                    value += tmpValue << bitsLeft

                    
            else:
                #We are at start of current byte 

                if bitsLeft >= 8:
                    value           += currentByteValue << bitsLeft - 8 
                    bitsLeft        -= 8 
                    self.__byteIndex  += 1

                else:

                    bitIndexInByte = 7 

                    #check if we want only subset of current byte. TODO: is this right? off-by-one mayhaps?
                    if bitsLeft < 8 - self.__bitIndex:
                        bitIndexInByte = self.__bitIndex + bitsLeft 

                    #get a binary string with at least 8 chars
                    binaryString = bin(currentByteValue)[2:]                    
                    
                    binaryString = ("0" * (8 - len(binaryString))) + str(binaryString)

                    #take out the bit-chars that we want from this binary string
                    binaryString = binaryString[self.__bitIndex:bitIndexInByte] 

                    #Set new __bitIndex and calculate how many bits are left 
                    tmpBitIndex = self.__bitIndex 

                    self.__bitIndex += bitsLeft

                    bitsLeft -= (bitIndexInByte - tmpBitIndex)  

                    value += int(binaryString, 2) << bitsLeft

                    if self.__bitIndex >= 8:
                        self.__bitIndex   = 0
                        self.__byteIndex += 1



        return value 


