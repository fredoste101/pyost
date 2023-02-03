
from ..eprint.eprint import eprint
from ..termColor.termColor import TermColor

import datetime

import inspect
        

class Verboser:
    """
        Use to print different messages.

        Functions info, warning, error, success and debug are basic messages that can be written.
        info and debug can be divided into levels (0, 1, 2,...) which must be enabled separetly. 
    """

    __infoLevelSet    = set()           #to enable certain info-prints of given level, must add that level (int) to this list
    __debugLevelSet   = set()           #same as info but for debug

    enableError        = True           #Errors are enabled per default 
    enableWarning      = False 
    enableSuccess      = False
    inColor            = False          #Print with color-codes
    withTime           = True           #Each pring will include a isoformat time 
    termColor          = TermColor()        

    withCalleInfo      = False

    saveToHistory      = False          #If True will not print messages to terminal directly, but instead
                                        #append them to a historyList, that can be printed later on.
    __messageHistoryStringList = []

    __infoNameSet       = set()
    __debugNameSet      = set()
    __warningNameSet    = set()
    __errorNameSet      = set()

    __supressAll = False
    

    @staticmethod
    def supressAll():
        Verboser.__supressAll = True


    @staticmethod
    def unSupressAll():
        Verboser.__supressAll = False


    @staticmethod
    def addInfoLevel(level):
        if type(level) is int:
            Verboser.__infoLevelSet.add(level)

        elif type(level) is str:
            Verboser.__infoNameSet.add(level)


    @staticmethod
    def removeInfoLevel(level):
        if type(level) is int:
            if level in Verboser.__infoLevelSet:
                Verboser.__infoLevelSet.remove(level)

        elif type(level) is str:
            if level in Verboser.__infoNameSet:
                Verboser.__infoNameSet.remove(level)


    @staticmethod
    def getTimeStringNow():
        return str(datetime.datetime.now().isoformat(sep=" ")) 


    @staticmethod
    def info(msg, level=0):

        if type(level) is int:
            if level in Verboser.__infoLevelSet:
                Verboser.printString(msg, 
                                     "INFO" + str(level), 
                                     Verboser.termColor.BLUE)

        elif type(level) is str:
            if level in Verboser.__infoNameSet:
                Verboser.printString(msg, level + " INFO", Verboser.termColor.BLUE)

        else:
            raise Exception("Non allowed type: " + str(type(level)))


    @staticmethod
    def printString(msg, typeString, colorCode, stderr=False):

        if Verboser.__supressAll:
            return

        stringList = []

        stringList.append(typeString)

        if Verboser.withTime:
            stringList.append(" [" + Verboser.getTimeStringNow() + "]")

        if Verboser.withCalleInfo:
            callerInfo = inspect.getframeinfo(inspect.stack()[2][0])
            stringList.append(" " + callerInfo.filename + ":" + callerInfo.function + ":" + str(callerInfo.lineno))


        stringList.append(": " + msg)

        string = "".join(stringList)

        if Verboser.inColor: 
            string = colorCode + string + Verboser.termColor.RESET 

        if Verboser.saveToHistory:
            Verboser.__messageHistoryStringList.append(string)
            
        else:
            if stderr:
                eprint(string)
            else:
                print(string)


    @staticmethod
    def success(msg):
        if Verboser.enableSuccess:
            Verboser.printString(msg, "SUCCESS", Verboser.termColor.GREEN)
         

    @staticmethod
    def error(msg):
        """
            Prints an error. 
            Error is printed to stderr
        """

        if Verboser.enableError:
            Verboser.printString(msg, "ERROR", Verboser.termColor.RED, stderr=True)

            
    @staticmethod
    def warning(msg):
        if Verboser.enableWarning:
            Verboser.printString(msg, "WARNING", Verboser.termColor.YELLOW) 


    @staticmethod
    def debug(msg, level=0):
        if type(level) is int:
            if level in Verboser.__debugLevelSet:
                    Verboser.printString(msg, "DEBUG" + str(level), Verboser.termColor.MAGENTA)

        elif type(level) is str:
            if level in Verboser.__debugNameSet:
                    Verboser.printString(msg, level + " DEBUG", Verboser.termColor.MAGENTA)


    @staticmethod
    def addDebugLevel(level):
        if type(level) is int:
            Verboser.__debugLevelSet.add(level)

        elif type(level) is str:
            Verboser.__debugNameSet.add(level)
        

    @staticmethod
    def removeDebugLevel(level):
        if type(level) is int:
            if level in Verboser.__debugLevelSet:
                Verboser.__debugLevelSet.remove(level)

        elif type(level) is str:
            if level in Verboser.__debugNameSet:
                Verboser.__debugNameSet.remove(level)
         


    @staticmethod
    def getMessageHistory():
        return Verboser.__messageHistoryStringList


    @staticmethod
    def printMessageHistory():
        for message in Verboser.__messageHistoryStringList:
            print(message)
    

    @staticmethod
    def clearMessageHistory():
        Verboser.__messageHistoryStringList = [] 

