import copy
import itertools

debug = False

def debugPrint(msg):
    if debug:
        print(msg)

class Field:
    def __init__(self):
        self.name   = ""
        self.length = 0



def constructPermutation(stackList, startIndex, subPermutation, finalPermutationList):
    """
        Constructs all permutations and stores them in finalPermutationList

    """

    debugPrint("stackList=" + str(stackList) + " startIndex=" + str(startIndex) + " subPermutation=" + str(subPermutation))

    numPopped = 0 

    stackListNow = copy.deepcopy(stackList)

    if len(stackList[startIndex]) > 0:
        element = stackListNow[startIndex].pop() 
        subPermutation.append(element)
        numPopped += 1 

        for nextStartIndex in range(len(stackListNow)):
            numPopped += constructPermutation(stackListNow, 
                                              nextStartIndex, 
                                              copy.copy(subPermutation),
                                              finalPermutationList) 

        if numPopped == 1:
            finalPermutationList.append(subPermutation)
            #print("DONE:" + str(subPermutation))

    if numPopped == 0:
        debugPrint("\nDEAD END\n")

    return numPopped


def constructUniqueStacksFromList(valueList):
    stackList = []

    for value in valueList:

        valueInStack = False 

        for stack in stackList:
            if value in stack:
                stack.append(value)  
                valueInStack = True
                break
    
        if not valueInStack:
            newStack = []
            newStack.append(value)
            stackList.append(newStack)

    return stackList


def getPermutationsOfList(valueList):
    permutationList = []

    
    stackList = constructUniqueStacksFromList(valueList)

    for startIndex in range(len(stackList)):
        debugPrint("\nNEXT TOP\n")
        constructPermutation(copy.deepcopy(stackList), 
                             startIndex, 
                             [], 
                             permutationList)

    return permutationList


def main():

    #valueList = [1, 4, 1, 9, 8, 9, 1, 4]
    valueList = [1, 1, 3]
    
    permutationList = getPermutationsOfList(valueList)

    print(str(list(itertools.permutations(valueList)))) 

    print(str(permutationList))


if __name__ == "__main__":
    main()
