
from pyost.eprint.eprint import eprint
from pyost.termColor.termColor import TermColor

import datetime
        

class Verboser:
    """
        Use to print different messages.

        Functions info, warning, error, success and debug are basic messages that can be written.
        info and debug can be divided into levels (0, 1, 2,...) which must be enabled separetly. 
    """



    def __init__(self):
        self.__infoLevelList    = []        #to enable certain info-prints of given level, must add that level (int) to this list
        self.__debugLevelList   = []        #same as info but for debug

        self.enableError        = True      #Errors are enabled per default 
        self.enableWarning      = False 
        self.enableSuccess      = False
        self.inColor            = False     #Print with color-codes
        self.withTime           = False     #Each pring will include a isoformat time 
        self.termColor          = TermColor()        

        self.saveToHistory      = False #If True will not print messages to terminal directly, but instead
                                        #append them to a historyList, that can be printed later on.
        self.__messageHistoryStringList = []

        self.__verboseDict = {} # "nameOfTrace": {"color":"<color>"}


    def addInfoLevel(self, level):
        if type(level) != int:
            raise Exception("level must be of type int")
        
        if level not in self.__infoLevelList:
            self.__infoLevelList.append(level)


    def removeInfoLevel(self, level):
        if level in self.__infoLevelList:
            self.__infoLevelList.remove(level)


    def getTimeStringNow(self):
        return str(datetime.datetime.now().isoformat(sep=" ")) 


    def info(self, msg, level=0):
        for enabled in self.__infoLevelList:
            if enabled == level:
                self.printString(msg, "INFO" + str(level), self.termColor.BLUE)

          
    def printString(self, msg, typeString, colorCode):
        if self.withTime:
            string = typeString + " [" + self.getTimeStringNow() + "]: " + msg

        else:
            string = typeString + ": " + msg

        if self.inColor: 
            string = colorCode + string + self.termColor.RESET 

        if self.saveToHistory:
            self.__messageHistoryStringList.append(string)
            
        else:
            print(string)


    def success(self, msg):
        if self.enableSuccess:
            self.printString(msg, "SUCCESS", self.termColor.GREEN)
         

    def error(self, msg):
        if self.enableError:
            string = "ERROR: " + msg
            if self.withTime:
                string = "ERROR [" + self.getTimeStringNow() + "]: " + msg

            if self.inColor:
                string = self.termColor.RED + string + self.termColor.RESET 

            eprint(string)
            

    def warning(self, msg):
        if self.enableWarning:
            self.printString(msg, "WARNING", self.termColor.YELLOW) 


    def debug(self, msg, level=0):
        for enabled in self.__debugLevelList:
            if enabled == level:
                self.printString(msg, "DEBUG" + str(level), self.termColor.MAGENTA)


    def addDebugLevel(self, level):
        if type(level) != int:
            raise Exception("level must be of int type")

        if level not in self.__debugLevelList:
            self.__debugLevelList.append(level)        
        

    def removeDebugLevel(self, level):
        self.__debugLevelList.remove(level) 


    def getMessageHistory(self):
        return self.__messageHistoryStringList


    def printMessageHistory(self):
        for message in self.__messageHistoryStringList:
            print(message)
    

    def clearMessageHistory(self):
        self.__messageHistoryStringList = [] 

