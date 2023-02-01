import rectStacking
#from itertools import combinations_with_replacement
import permutations


def main():
    bitFieldList = [2, 3, 12, 2, 7, 17]

    bitFieldContainerSizeList = [16, 32]

    finalContainerSizeList = []

    for bitField in bitFieldList:
        isContainerSizeAdded = False
        for bitFieldContainerSize in bitFieldContainerSizeList:
            
            if bitField < bitFieldContainerSize:
                finalContainerSizeList.append(bitFieldContainerSize)    
                isContainerSizeAdded = True 
                break;

        if not isContainerSizeAdded:
            print("ERROR: bitField does not fit any given container size")
            return -1

    #print(str(finalContainerSizeList))
    bitFieldPermutationList = permutations.getPermutationsOfList(bitFieldList)
    #bitFieldPermutationList = list(combinations_with_replacement(bitFieldList, 6))

    for permutation in bitFieldPermutationList:
        
        print(str(permutation))


if __name__ == "__main__":
    main()
