
class Tablelizer(object):
    """
        Class for turning a list of lists (matrix)
        into a table of given type. 
    """
    
    def __init__(self):
        self.headerList     = []
        self.dataRowList    = []
        self.margin = 2
        self.terminalConfig =   {
                                    "columnMarginSize":1, 
                                    "rowSeparatorChar":"-", 
                                    "cornerChar":"+", 
                                    "columnSeparatorChar":"|",
                                    "align":"left",
                                    "header":True,
                                    "plain":False
                                }

        self.maxSizeList = []


    def setMaxSizeList(self):
        self.maxSizeList = []
        numColumns = len(self.headerList)

        for index in range(numColumns):
            self.maxSizeList.append(0)

        for index, header in enumerate(self.headerList):
            if len(header) > self.maxSizeList[index]:
                self.maxSizeList[index] = len(header)

        for row in self.dataRowList:
            for index, column in enumerate(row):
                if len(column) > self.maxSizeList[index]:
                    self.maxSizeList[index] = len(column)



class TablelizerTerminal(Tablelizer):
    def __init__(self):
        self.config = {
                            "columnMarginSize":1, 
                            "rowSeparatorChar":"-", 
                            "cornerChar":"+", 
                            "columnSeparatorChar":"|",
                            "align":"left",
                            "header":True,
                            "plain":False
                      }

    
    def getString(self):
        """
            Get string for terminal output.
        """
        tableStringList = []

        self.setMaxSizeList()

        

        if self.config["header"]:
            tableStringList.append(self.getRowSeparatorString())
            tableStringList.append(self.getHeaderString())

        tableStringList.append(self.getRowSeparatorString())

        tableStringList.append(self.getDataRowString())


        return "".join(tableStringList)


    def getHeaderString(self):
        headerRowStringList = []

        separatorChar = self.config["columnSeparatorChar"]

        if self.config["plain"]:
            separatorChar = ""

        headerRowStringList.append(separatorChar)

        for header, size in zip(self.headerList, self.maxSizeList):
            fillerLeft  = ""
            fillerRight = ""
            
            if self.config["align"] == "left":
                fillerRight = " " * (size - len(header))
            elif self.config["align"] == "right":
                fillerLeft  = " " * (size - len(header))
            elif self.config["align"] == "center":
                fillerRight = " " * (((size - len(header))/2))
                fillerLeft  = fillerRight

            

            headerRowStringList.append(" " * self.config["columnMarginSize"] + fillerLeft + 
                                       header + 
                                       fillerRight + " " * self.config["columnMarginSize"] + separatorChar)

        return "".join(headerRowStringList) + "\n"


    def getDataRowString(self):
        dataRowStringList  = []

        separatorChar = self.config["columnSeparatorChar"]

        if self.config["plain"]:
            separatorChar = ""

        for row in self.dataRowList:
            
            dataRowStringList.append(separatorChar)
            for data, size in zip(row, self.maxSizeList):
                fillerLeft  = ""
                fillerRight = ""
            
                if self.config["align"] == "left":
                    fillerRight = " " * (size - len(data))
                elif self.config["align"] == "right":
                    fillerLeft  = " " * (size - len(data))
                elif self.config["align"] == "center":
                    fillerRight = " " * (((size - len(data)) / 2))
                    fillerLeft  = fillerRight


                

                dataRowStringList.append(" " * self.config["columnMarginSize"] + fillerLeft + data + fillerRight + 
                                       " " * self.config["columnMarginSize"] + separatorChar)


            dataRowStringList.append("\n" + self.getRowSeparatorString())


        return "".join(dataRowStringList)


    def getRowSeparatorString(self):
        if self.config["plain"]:
            return ""

        rowSeparatorStringList = []

        rowSeparatorStringList.append(self.config["cornerChar"])

        for size in self.maxSizeList:
            rowSeparatorStringList.append(((size + self.config["columnMarginSize"] * 2) * self.config["rowSeparatorChar"]) + 
                                          self.config["cornerChar"])

        return "".join(rowSeparatorStringList) + "\n"


class TablelizerHtml(Tablelizer):
    def __init__(self):
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