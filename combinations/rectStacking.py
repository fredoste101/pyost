import copy

def stackRectangles(placesLeft, 
              currentStack, 
              boxValueList, 
              finalStackList):
    """
        Stacking rectangles.

        Get all possible ways to stack a number of rectangles with sides boxValueList=[x1, x2, ... xK]
        in a place with placesLeft=N length-units.

        result will be placed in finalStackList

        Example usage:
        stackRectangles(10, [], [1,2,3], resultStackList)

        will stack rectangles with sides 1, 2, and 3 length units,
        in a location with 10 length units.
        so one possible way to stack would be: [1, 2, 3, 1, 1, 1, 1] for example.
        All these possible ways to stack is returned in finalStackList
    """

    if placesLeft == 0:
        finalStackList.append(currentStack)

    else:
        for boxValue in boxValueList:
            if placesLeft >= boxValue:
                newCopy = copy.deepcopy(currentStack) 
    
                newCopy.append(boxValue)
                stackRectangles(placesLeft - boxValue, 
                          newCopy,
                          boxValueList, 
                          finalStackList) 
        
    
def main():
    boxValueList = [16, 32]
    finalStackList = []
    stackRectangles(160, [], boxValueList, finalStackList)
    print(str(finalStackList))


if __name__ == "__main__":
    main()
