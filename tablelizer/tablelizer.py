
from itertools import zip_longest

class Tablelizer(object):
    """
        Class for turning a list of lists (matrix)
        into a table of given type. 
    """
    
    def __init__(self):
        self.headerList     = []
        self.dataRowList    = []

        self.maxColumnWidthList = []



class TablelizerTerminal(Tablelizer):

    def __init__(self):

        super(TablelizerTerminal, self).__init__()

        self.config = {
                            "columnMarginSize":     1, 
                            "rowSeparatorChar":     "-", 
                            "cornerChar":           "+", 
                            "columnSeparatorChar":  "|",
                            "align":                "right", #{left, center, right}
                            "header":               True,
                            "plain":                False #No formatting ascii at all
                      }

        self.columnConfig = []


    def __lineyfy(self, stringList):
        """
            Turn a list of strings, into a list of list of strings,
            split on \n. Basically turns each string into a list of lines
        """
        linesList = []

        for string in stringList:
            linesList.append(string.split("\n"))

        return linesList
            
        

    def __setMaxSizeList(self):

        self.maxColumnWidthList = []

        numColumns = len(self.headerList)

        for index in range(numColumns):
            self.maxColumnWidthList.append(0)

        #TODO: incorporate \n so to check max column size with newlines included
        #MAYBETODO: make it posssible to define some chars not to count, I.E Terminal codes for colors :D



        for index, header in enumerate(self.headerList):
            
            if len(header) > self.maxColumnWidthList[index]:
                self.maxColumnWidthList[index] = len(header)

        for row in self.dataRowList:
            for index, column in enumerate(row):
                columnLength = self.__getStringColumnWidth(column)

                if columnLength > self.maxColumnWidthList[index]:
                    self.maxColumnWidthList[index] = columnLength
    

    def __getStringColumnWidth(self, string):
        stringRows = string.split("\n")

        maxSize = 0

        for row in stringRows:
            if len(row) > maxSize:
                maxSize = len(row)

        return maxSize


    def getString(self):
        """
            Get string for terminal output.
        """

        #TODO: check that header and each row have the same number of columns

        tableStringList = []

        self.__setMaxSizeList()

        if self.config["header"]:
            tableStringList.append(self.getRowSeparatorString())
            tableStringList.append(self.getHeaderString())

        tableStringList.append(self.getRowSeparatorString())

        tableStringList.append(self.getDataRowString())


        return "".join(tableStringList)


    def __getAlignedString(self, string, size):
        """
            Align string based on "align" attribute in config.
            Also add margin on each side, based on "columnMarginSize" attribute.
        """
        alignedString = ""

        if self.config["align"] == "left":
            alignedString = string.ljust(size)

        elif self.config["align"] == "right":
            alignedString = string.rjust(size)

        elif self.config["align"] == "center":
            alignedString = string.center(size)

        return self.config["columnMarginSize"] * " " + alignedString + self.config["columnMarginSize"] * " "


    def getHeaderString(self):
        headerRowStringList = []

        separatorChar = self.config["columnSeparatorChar"]

        if self.config["plain"]:
            separatorChar = ""

        headerRowStringList.append(separatorChar)

        for header, size in zip(self.headerList, self.maxColumnWidthList):

            alignedString = self.__getAlignedString(header, size)

            headerRowStringList.append(alignedString)
            headerRowStringList.append(separatorChar)

        return "".join(headerRowStringList) + "\n"


    def getDataRowString(self):
        dataRowStringList  = []

        separatorChar = self.config["columnSeparatorChar"]

        if self.config["plain"]:
            separatorChar = ""

        for row in self.dataRowList:
        
            lineList = self.__lineyfy(row)

            for stringTuple in zip_longest(*lineList):

                dataRowStringList.append(separatorChar)

                for data, size in zip(stringTuple, self.maxColumnWidthList):
                    if data == None:
                        alignedString = self.__getAlignedString("", size)

                        dataRowStringList.append(alignedString)
                        dataRowStringList.append(separatorChar)
                    else:
                        alignedString = self.__getAlignedString(data, size)

                        dataRowStringList.append(alignedString)
                        dataRowStringList.append(separatorChar)

                dataRowStringList.append("\n")
            

            #for data, size in zip(row, self.maxColumnWidthList):

            #    alignedString = self.__getAlignedString(data, size)

            #    dataRowStringList.append(alignedString)
            #    dataRowStringList.append(separatorChar)

            dataRowStringList.append(self.getRowSeparatorString())

        return "".join(dataRowStringList)


    def getRowSeparatorString(self):
        if self.config["plain"]:
            return ""

        rowSeparatorStringList = []

        rowSeparatorStringList.append(self.config["cornerChar"])

        for size in self.maxColumnWidthList:
            rowSeparatorStringList.append(((size + self.config["columnMarginSize"] * 2) * self.config["rowSeparatorChar"]) + 
                                          self.config["cornerChar"])

        return "".join(rowSeparatorStringList) + "\n"


class TablelizerHtml(Tablelizer):
    def __init__(self):
        super(TablelizerHtml, self).__init__()
        self.footerList = []
        self.config =   {
                            "tableStyle":"",
                            "theaderStyle":""
                        }
   

    def getString(self):
        """
            Get HTML string with <table>-tags and such.
        """
        htmlStringList = []

        htmlStringList.append("<table>")

        htmlStringList.append(self.getHeaderString())

        htmlStringList.append(self.getBodyString())

        htmlStringList.append(self.getFooterString())


        htmlStringList.append("</table>")

        return "".join(htmlStringList)


    def getHeaderString(self):
        headerStringList = []

        headerStringList.append("<thead>")
        headerStringList.append("<tr>")

        for header in self.headerList:
            headerStringList.append("<th>")
            headerStringList.append(header)
            headerStringList.append("</th>")
        
        headerStringList.append("</tr>")
        headerStringList.append("</thead>")

        return "".join(headerStringList)


    def getBodyString(self):
        bodyStringList = []

        bodyStringList.append("<tbody>")

        for row in self.dataRowList:
            bodyStringList.append("<tr>")
            for data in row:
                bodyStringList.append("<td>")
                bodyStringList.append(data)
                bodyStringList.append("</td>")

            bodyStringList.append("</tr>")

        bodyStringList.append("</tbody>")

        return "".join(bodyStringList)


    def getFooterString(self):
        footerStringList = []

        footerStringList.append("<tfoot>")

        for footer in self.footerList:
            footerStringList.append("<td>")
            footerStringList.append(footer)
            footerStringList.append("</td>")

        footerStringList.append("</tfoot>")

        return "".join(footerStringList)


class TablelizerMediaWiki(Tablelizer):

    def __init__(self):
        super(TablelizerMediaWiki, self).__init__()
        self.classList = ["wikitable"]


    def getString(self):
        tableStringList = []

        tableStringList.append("{|")

        tableStringList.append(" class=\"")

        for className in self.classList:
            tableStringList.append(className + " ")

        tableStringList.append("\" ")
            

        tableStringList.append(self.getHeaderString())

        tableStringList.append(self.getBodyString())

        tableStringList.append("\n|}")

        return "".join(tableStringList)


    def getHeaderString(self):
        headerStringList = []

        headerStringList.append("\n|-\n")

        isFirstHeader = True

        for header in self.headerList:
            if isFirstHeader:
                headerStringList.append("! ")
                isFirstHeader = False
            else:
                headerStringList.append(" !! ")
            
            headerStringList.append(header)



        return "".join(headerStringList)


    def getBodyString(self):
        bodyStringList = []

        for row in self.dataRowList:
            bodyStringList.append("\n|-\n")
            isFirstData = True
            for data in row:
                if isFirstData:
                    bodyStringList.append("| ")
                    isFirstData = False
                else:
                    bodyStringList.append(" || ")

                bodyStringList.append(data)       

        return "".join(bodyStringList)         



if __name__ == "__main__":
    t = TablelizerTerminal()
    t.headerList = ["1", "2"]

    t.dataRowList = [["abcdefg", "b"], ["c", "d"]]

    print(t.getString())


    t.config["align"] = "right"

    print(t.getString())

    t.config["align"] = "center"

    print(t.getString())

    t.config["header"] = False

    print(t.getString())

    t.config["header"]  = True
    t.config["plain"]   = True
    t.config["align"]   = "right"

    print(t.getString())


    htmlTable = TablelizerHtml()

    htmlTable.headerList = ["1", "2"]

    htmlTable.dataRowList = [["a", "b"], ["c", "d"]]

    print(htmlTable.getString())


    wt = TablelizerMediaWiki()

    wt.headerList = ["1", "2"]
    wt.dataRowList = [["a", "b"], ["c", "d"]]

    print(wt.getString())