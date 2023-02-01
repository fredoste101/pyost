import json
import argparse

WORD_SIZE = 16

colorWheelList = ["#81ecec", "#a29bfe", "#ffeaa7", "#55efc4", "#fd79a8", "#00cec9"]

class BitFieldCollection:
    def __init__(self):
        self.length = 0 #Length in bits
        self.bitFieldList = []
        

class BitField:
    def __init__(self):
        self.name = "" 
        self.length = 0
        self.color = None
       
class Var:
    def __init__(self):
        pass 

class Struct:
    def __init__(self):
        self.name = ""
        self.varList = [] 


def getHtmlStartString():
    htmlStartStringList = []

    htmlStartStringList.append("<!DOCTYPE html/>")

    htmlStartStringList.append("<html>")

    return "\n".join(htmlStartStringList)


def getHtmlEndString():
    htmlEndStringList = []

    htmlEndStringList.append("</html>")

    return "\n".join(htmlEndStringList)


def getHtmlHeaderString():
    htmlHeaderStringList = []

    htmlHeaderStringList.append("<head>")
    htmlHeaderStringList.append("<meta charset='utf-8' />")
    htmlHeaderStringList.append("<title>BitFieldTablelizer</title>")
    htmlHeaderStringList.append("<style>table, tr, th {border:1px solid black; border-collapse:collapse;} table {table-layout: fixed; width:600px;}</style>")
    htmlHeaderStringList.append("</head>")

    return "\n".join(htmlHeaderStringList)


def getBitFieldTableHeaderString():
    headerRowStringList = []
    headerRowStringList.append("<tr>")

    for i in range(WORD_SIZE):
       headerRowStringList.append("<th>" + str(i) + "</th>") 

    headerRowStringList.append("</tr>")
    return "\n".join(headerRowStringList)


def getBitFieldHtmlTd(fieldLength, name, color):
    return "<td style='text-align:center; border:1px solid black; background-color:" + color + ";' colspan=" + str(fieldLength) + ">" + name + "</td>"


def getBitFieldTable(bitFieldList):
    bitFieldTableStringList = []

    bitFieldTableStringList.append("<table class='bitFieldTable'>")

    headerRowString = getBitFieldTableHeaderString()    

    bitFieldTableStringList.append(headerRowString)

    bitFieldHtmlStringList = []

    bitFieldHtmlStringList.append("<tr>")

    changeRow = False

    remainingBitsInWord = WORD_SIZE 

    colorWheelIndex = 0

    for bitField in bitFieldList:
        if bitField.length >= remainingBitsInWord:
            bitsLeftInField = bitField.length             

            color = colorWheelList[colorWheelIndex]
            if bitField.color:
                color = bitField.color

            while(bitsLeftInField > 0): 
                if bitsLeftInField >= remainingBitsInWord:
                    bitFieldHtmlStringList.append(getBitFieldHtmlTd(remainingBitsInWord, bitField.name + "(" + str(bitField.length) + ")", color))
                    bitFieldHtmlStringList.append("</tr><tr>")
                    bitsLeftInField     = bitsLeftInField - remainingBitsInWord
                    remainingBitsInWord = WORD_SIZE 
                else:
                    bitFieldHtmlStringList.append(getBitFieldHtmlTd(bitsLeftInField, bitField.name, color))
                    remainingBitsInWord -= bitsLeftInField
                    bitsLeftInField = 0    
                    
            colorWheelIndex += 1
        else:
            color = colorWheelList[colorWheelIndex]
            if bitField.color:
                color = bitField.color

            bitFieldHtmlStringList.append(getBitFieldHtmlTd(bitField.length, bitField.name + "(" + str(bitField.length) + ")", color))
            remainingBitsInWord -= bitField.length
            colorWheelIndex+=1

        colorWheelIndex = 0 if colorWheelIndex >= len(colorWheelList) else colorWheelIndex


    bitFieldHtmlStringList.append("</tr>")

    bitFieldTableStringList.append("\n".join(bitFieldHtmlStringList))
    bitFieldTableStringList.append("</table>")

    return "\n".join(bitFieldTableStringList) 


def getHtmlBodyString(bitFieldList):
    htmlBodyStringList = []

    htmlBodyStringList.append("<body>")
    htmlBodyStringList.append(getBitFieldTable(bitFieldList))
    htmlBodyStringList.append("</body>")

    return "\n".join(htmlBodyStringList)


def jsonStringToBitFieldList(jsonString):
    jsonDict = json.loads(jsonString)
    
    bitFieldList = []
    for jsonBitField in jsonDict:
        bitField = BitField()

        bitField.name = jsonBitField["name"]
        bitField.length = jsonBitField["length"]
        if "color" in jsonBitField.keys():
            bitField.color = jsonBitField['color']

        bitFieldList.append(bitField)
        

    return bitFieldList 


def main():
    jsonString = '[{"name":"test", "length":10}, {"name":"test2", "length":34}, {"name":"test3", "length":6, "color":"red"}]'

    bitFieldList = jsonStringToBitFieldList(jsonString) 

    argParser = argparse.ArgumentParser(description="Program to visualize struct packing of bit fields.\nInput is a json-file with format: [ {\"name\":<name>, \"length\":<length> <optional color>}* ]", epilog="Output is a html-file")

    argParser.add_argument("--json", help="File containing json that represent the bitfields in structs", type=str, metavar="<jsonFile>", dest="jsonFile", required=True)

    arguments = argParser.parse_args() 

    jsonFile = open(arguments.jsonFile, "r")

    jsonString = jsonFile.read()

    bitFieldList = jsonStringToBitFieldList(jsonString)

    htmlStartString = getHtmlStartString()
    headerString    = getHtmlHeaderString()
    bodyString      = getHtmlBodyString(bitFieldList)
    htmlEndString   = getHtmlEndString()

    print(htmlStartString)
    print(headerString)
    print(bodyString)
    print(htmlEndString)
    

if __name__ == "__main__":
    main()
