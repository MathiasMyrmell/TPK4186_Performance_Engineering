
import matplotlib.pyplot as plt

class Document:
    def __init__(self):
        self.headStart = "<html><head>"
        self.title = "<title>ChessGame</title>"
        self.headEnd = "</head>"
        self.bodyStart = "<body>"
        self.body = ""
        self.bodyEnd = "</body>"

        self.documentEnd = "</html>"



    def createTable(self):
        strTable = "<table><tr><th>Char</th><th>ASCII</th></tr>"

        for num in range (33,48):
            symb = chr(num)
            strRW = "<tr><td>" + symb + "</td><td>"+str(num)+"</td></tr>"
            strTable = strTable + strRW

        strTable = strTable + "</table></html>"
        self.body = strTable

    def createStatTable(self, tableContent):
        strTable = "<table><tr><th></th><th>Win</th><th>Draw</th><th>Loss</th></tr>"
        white = "<tr><td>White</td>"
        for i in range(0,3):
            white+="<td>"+str(tableContent[i])+"</td>"
        white+="</tr>"

        black = "<tr><td>Black</td>"
        for i in range(3,6):
            black+="<td>"+str(tableContent[i])+"</td>"
        black+="</tr>"

        tot = "<tr><td>Total</td>"
        for i in range(6,9):
            tot+="<td>"+str(tableContent[i])+"</td>"
        tot+="</tr>"
        strTable = strTable + white + black + tot + "</table>"
        self.body += strTable

    def createPlot(self, plotContent):
        sortedDict = plotContent[0]
        yValues = plotContent[1]
        mean = plotContent[2]
        std = plotContent[3]

        #Plot
        plt.plot(sortedDict.keys(), yValues, color='g')
        plt.xlabel("Number of moves",fontsize='13')	
        plt.ylabel("Number of games",fontsize='13')
        plt.savefig("project2/figures/plotOfNumberOfMoves.png")

        self.body+="<img src='figures/plotOfNumberOfMoves.png'>"
        self.body+=self._createMeanAndStdTable(mean, std)
        # plt.show()

    def _createMeanAndStdTable(self, mean, std):
        strTable = "<table><tr><th>Mean moves</th><th>STD</th></tr>"
        values = "<tr><td>" +str(mean)+ "</td><td>"+str(std)+ "</td></tr>"
       
        strTable = strTable + values + "</table>"
        return strTable

    def createHTMLContent(self):
        html = self.headStart + self.title + self.headEnd + self.bodyStart + self.body + self.bodyEnd + self.documentEnd
        return html

    def write(self):
        content = self.createHTMLContent()
        hs = open("project2/document.html", "w")
        hs.write(content)
        hs.close()