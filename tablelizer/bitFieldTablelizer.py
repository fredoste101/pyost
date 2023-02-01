import json
import argparse

colorWheelList =    [
                        "#81ecec", 
                        "#a29bfe", 
                        "#ffeaa7", 
                        "#55efc4", 
                        "#fd79a8", 
                        "#00cec9", 
                        "#d1d8e0", 
                        "#45aaf2", 
                        "#f7f1e3", 
                        "#ffda79", 
                        "#706fd3", 
                        "#ffcccc", 
                        "#3ae374"
                    ]



class BitFieldCollection:
    def __init__(self):
        self.length         = 0 #Length in bits
        self.bitFieldList   = []
        self.wordLength     = 16
        self.jsonString     = ""
        self.bitPixelsWidth = 40
        self.inlineStyle    = False

        self.classStylesDict =  {
                                    "bitFieldTable":"border:1px solid black; border-collapse: collapse; padding: 0px; table-layout: fixed;",
                                    "bitFieldRow":"border:1px solid black; border-collapse:collapse; padding:0px;",
                                    "bitFieldTableHeader":"border:1px solid black; border-collapse:collapse; padding:0px;",
                                    "tableData":"padding:0px;",
                                    "fieldName":"padding:5px; overflow:hidden; text-overflow:ellipsis; cursor:pointer; white-space:no-wrap;",
                                    "fieldBitsTable":"border-collapse:collapse; table-layout: fixed; width:100%;",
                                    "rowBitNum":"text-align:center;",
                                    "fieldsBitsValue":"text-align:center; padding:5px;",
                                    "fieldsBitsValueLeft":"border-left:1px solid black;"

                                }


    def parseJson(self):
        jsonDict = json.loads(self.jsonString)

        for jsonBitField in jsonDict:
            bitField = BitField()

            bitField.name = jsonBitField["name"]
            bitField.length = jsonBitField["length"]

            if "color" in jsonBitField.keys():
                bitField.color = jsonBitField['color']

            self.bitFieldList.append(bitField)


    def getHtmlString(self, tableOnly = False):
        if tableOnly:
            return "shizzle"

        htmlStartString = self.getHtmlStartString()
        headerString    = self.getHtmlHeaderString()
        bodyString      = self.getHtmlBodyString()
        htmlEndString   = self.getHtmlEndString()

        return htmlStartString + headerString + bodyString + htmlEndString
    
    def getHtmlStartString(self):
        htmlStartStringList = []

        htmlStartStringList.append("<!DOCTYPE html/>")

        htmlStartStringList.append("<html>")

        return "\n".join(htmlStartStringList)


    def initSize(self):
        width = self.wordLength * self.bitPixelsWidth

        self.classStylesDict["bitFieldTable"] = self.classStylesDict["bitFieldTable"] + " width:" + str(width) + "px;"


    def getHtmlHeaderString(self):
        htmlHeaderStringList = []

        htmlHeaderStringList.append("<head>")
        htmlHeaderStringList.append("<meta charset='utf-8' />")
        htmlHeaderStringList.append("<title>BitFieldTablelizer</title>")

        htmlHeaderStringList.append("<style>")
        
        for key in self.classStylesDict:
            htmlHeaderStringList.append("\n." + key + " {" + self.classStylesDict[key] + "}")


        htmlHeaderStringList.append("</style>")

        htmlHeaderStringList.append("</head>")

        return "\n".join(htmlHeaderStringList)

    
    def getHtmlBodyString(self):
        htmlBodyStringList = []

        htmlBodyStringList.append("<body>")
        htmlBodyStringList.append(self.getBitFieldTable())
        htmlBodyStringList.append("</body>")

        return "\n".join(htmlBodyStringList)


    def getBitFieldTable(self):
        bitFieldTableStringList = []

        if self.inlineStyle:
            bitFieldTableStringList.append("<table style='" + self.classStylesDict["bitFieldTable"] + "'>")

        else:
            bitFieldTableStringList.append("<table class='bitFieldTable'>")


        headerRowString = self.getBitFieldTableHeaderString()    

        bitFieldTableStringList.append(headerRowString)

        bitFieldHtmlStringList = []

        rowValue = self.wordLength - 1
        rowValueRight = 0

        if self.inlineStyle:
            bitFieldHtmlStringList.append("<tr style='" + self.classStylesDict["bitFieldRow"] + "'>")

        else:
            bitFieldHtmlStringList.append("<tr class='bitFieldRow'>")


        if self.inlineStyle:
            bitFieldHtmlStringList.append("<td style='" + self.classStylesDict["rowBitNum"] + "'>")

        else:
            bitFieldHtmlStringList.append("<td class='rowBitNum'>")

        bitFieldHtmlStringList.append(str(rowValue) + "</td>")


        rowValue += self.wordLength

        remainingBitsInWord = self.wordLength 

        colorWheelIndex = 0

        shouldCloseRow = True

        for bitFieldIndex, bitField in enumerate(self.bitFieldList):
            if bitField.length >= remainingBitsInWord:
                bitsLeftInField = bitField.length             

                color = colorWheelList[colorWheelIndex]

                if bitField.color:
                    color = bitField.color

                while(bitsLeftInField > 0): 
                    if bitsLeftInField >= remainingBitsInWord:
                        bitFieldHtmlStringList.append(self.getBitFieldHtmlTd(remainingBitsInWord, bitField.name + "(" + str(bitField.length) + ")", color, bitsLeftInField))

                        if self.inlineStyle:
                            bitFieldHtmlStringList.append("<td style='" + self.classStylesDict["rowBitNum"] + "'>")

                        else:
                            bitFieldHtmlStringList.append("<td class='rowBitNum'>")

                        bitFieldHtmlStringList.append(str(rowValueRight) + "</td>")

                        rowValueRight += self.wordLength
                        bitFieldHtmlStringList.append("</tr>")

                        shouldCloseRow = False

                        if bitsLeftInField > remainingBitsInWord or (bitFieldIndex+1) < len(self.bitFieldList):
                            
                            if self.inlineStyle:
                                bitFieldHtmlStringList.append("<tr style='" + self.classStylesDict["bitFieldRow"] + "'>")

                            else:
                                bitFieldHtmlStringList.append("<tr class='bitFieldRow'>")

                            shouldCloseRow = True

                            if self.inlineStyle:
                                bitFieldHtmlStringList.append("<td style='" + self.classStylesDict["rowBitNum"] + "'>")

                            else:
                                bitFieldHtmlStringList.append("<td class='rowBitNum'>")
                            
                            bitFieldHtmlStringList.append(str(rowValue) + "</td>")
                            rowValue += self.wordLength

                        bitsLeftInField     = bitsLeftInField - remainingBitsInWord

                        remainingBitsInWord = self.wordLength 

                    else:
                        bitFieldHtmlStringList.append(self.getBitFieldHtmlTd(bitsLeftInField, bitField.name + "(" + str(bitField.length) + ")", color, bitsLeftInField))
                        remainingBitsInWord -= bitsLeftInField
                        bitsLeftInField = 0    
                        
                colorWheelIndex += 1

            else:
                color = colorWheelList[colorWheelIndex]
                if bitField.color:
                    color = bitField.color

                bitFieldHtmlStringList.append(self.getBitFieldHtmlTd(bitField.length, bitField.name + "(" + str(bitField.length) + ")", color, bitField.length))
                remainingBitsInWord -= bitField.length
                colorWheelIndex += 1

            colorWheelIndex = 0 if colorWheelIndex >= len(colorWheelList) else colorWheelIndex

        if shouldCloseRow:
            bitFieldHtmlStringList.append("</tr>")

        bitFieldTableStringList.append("".join(bitFieldHtmlStringList))
        bitFieldTableStringList.append("</table>")

        return "".join(bitFieldTableStringList) 


    def getBitFieldTableHeaderString(self):
        headerRowStringList = []

        if self.inlineStyle:
            headerRowStringList.append("<tr style='" + self.classStylesDict["bitFieldRow"] + "'>")
        else:
            headerRowStringList.append("<tr class='bitFieldRow'>")

        if self.inlineStyle:
            headerRowStringList.append("<th style='" + self.classStylesDict["bitFieldTableHeader"] + "'>") 
        else:
            headerRowStringList.append("<th class='bitFieldTableHeader'>") 

        headerRowStringList.append("&nbsp;</th>") 

        for i in range(self.wordLength)[::-1]:
            if self.inlineStyle:
                headerRowStringList.append("<th style='" + self.classStylesDict["bitFieldTableHeader"] + "'>") 
            else:
                headerRowStringList.append("<th class='bitFieldTableHeader'>") 
            
            headerRowStringList.append(str(i) + "</th>") 

        if self.inlineStyle:
            headerRowStringList.append("<th style='" + self.classStylesDict["bitFieldTableHeader"] + "'>") 
        else:
            headerRowStringList.append("<th class='bitFieldTableHeader'>") 

        headerRowStringList.append("&nbsp;</th>") 


        headerRowStringList.append("</tr>")
        
        return "".join(headerRowStringList)


    def getBitFieldHtmlTd(self, fieldLength, name, color, startBit):
        """
            Get the <td> content for a field. this is both name, 
            and bits numbered for that field.
        """
        
        tdContentStringList = []

        tdContentStringList.append("<td title=" + name + " style='text-align:center; border:1px solid black; background-color:" + color + ";' colspan=" + str(fieldLength) + ">")

        if self.inlineStyle:
            tdContentStringList.append("<div style='" + self.classStylesDict["fieldName"] + "'>")
        else:
            tdContentStringList.append("<div class='fieldName'>")

        tdContentStringList.append(name + "</div>")

        if self.inlineStyle:
            tdContentStringList.append("<table style='" + self.classStylesDict["fieldBitsTable"] + "'>")
        else:
            tdContentStringList.append("<table class='fieldBitsTable'>")

        isFirstField = True

        for i in range(fieldLength):
            if isFirstField:
                if self.inlineStyle:
                    tdContentStringList.append("<td style='" + self.classStylesDict["fieldsBitsValue"] + "'>")
                else:
                    tdContentStringList.append("<td class='fieldsBitsValue'>")
                
                isFirstField = False

            else:
                if self.inlineStyle:
                    tdContentStringList.append("<td style='" + self.classStylesDict["fieldsBitsValue"] + " " + self.classStylesDict["fieldsBitsValueLeft"] + "'>")
                else:
                    tdContentStringList.append("<td class='fieldsBitsValue fieldsBitsValueLeft'>")

            tdContentStringList.append(str(startBit - i - 1) + "</td>")
                
        tdContentStringList.append("</table>")

        tdContentStringList.append("</td>")

        return "".join(tdContentStringList) 


    def getHtmlEndString(self):
        htmlEndStringList = []

        htmlEndStringList.append("</html>")

        return "\n".join(htmlEndStringList)


class BitField:
    def __init__(self):
        self.name   = "" 
        self.length = 0
        self.color  = None



def main():
    #jsonString = '[{"name":"test", "length":10}, {"name":"test2", "length":34}, {"name":"test3", "length":6, "color":"red"}]'

    #bitFieldList = jsonStringToBitFieldList(jsonString) 

    argParser = argparse.ArgumentParser(description="Program to visualize struct packing of bit fields.\nInput is a json-file with format: [ {\"name\":<name>, \"length\":<length> <optional color>}* ]", 
                                        epilog="Output is an html-string")


    argParser.add_argument("--json", 
                           help="File containing json that represent the bitfields in structs", 
                           type=str, 
                           metavar="<jsonFile>", 
                           dest="jsonFile", 
                           required=True)


    argParser.add_argument("--wordLength", 
                           help="Word length of data output", 
                           type=int, metavar="<length>", 
                           dest="wordLength", 
                           required=False, 
                           default=16)

    argParser.add_argument("--bitPixelSize", 
                           help="Size in pixels each bit will take. If wordLength is 10, total table size will be approx: wordLength * numPixels", 
                           type=int, metavar="<numPixels>", 
                           dest="numPixels", 
                           required=False, 
                           default=40)
    
    
    argParser.add_argument("--onlyTable", 
                           help="Get only table html-tags. no wrapper around with <html>, <body> and such.", 
                           action="store_true",
                           default=False,
                           dest="onlyTable",
                           required=False)


    arguments = argParser.parse_args() 

    jsonFile = open(arguments.jsonFile, "r")

    jsonString      = jsonFile.read()


    bitFieldCollection = BitFieldCollection()

    bitFieldCollection.jsonString = jsonString

    bitFieldCollection.parseJson()

    bitFieldCollection.wordLength = arguments.wordLength
    bitFieldCollection.bitPixelsWidth = arguments.numPixels

    htmlString = ""

    bitFieldCollection.initSize()

    if arguments.onlyTable:
        bitFieldCollection.inlineStyle = True
        htmlString = bitFieldCollection.getBitFieldTable()

    else:
        htmlString = bitFieldCollection.getHtmlString()

    print(htmlString)
    

if __name__ == "__main__":
    main()
