#Task 6
import matplotlib.pyplot as plt

class Document:
    def __init__(self, name):
        self.name = name
        self.head = None
        self.body = None
        self.bodyContent = ""

        self.headStart = "<html><head>"
        self.title = "<title>ChessGame</title>"
        self.headEnd = "</head>"
        self.bodyStart = "<body>"
        self.body = ""
        self.bodyEnd = "</body>"

        self.documentEnd = "</html>"

    def createHead(self):
        headStart = "<html><head>"
        title = "<title>"+self.name+"</title>"
        headEnd = "</head>"
        self.head = headStart + title + headEnd

    def createBody(self):
        bodyStart = "<body>"
        bodyTitle = "<h1>"+self.name+"</h1>"
        bodyEnd = "</body>"
        self.body = bodyStart + bodyTitle + self.bodyContent + bodyEnd



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
        self.bodyContent += "<h1>Statistics</h1>"
        self.bodyContent += "<h2>Results</h2>"
        self.bodyContent += "<p>This table show the number of times Stockfish has won, drawn and lost, with white pieces, black pieces and in total.</p>"
        self.bodyContent += strTable

    def createPlot(self, plotContent):
        stockfish = plotContent[0:3]
        stockfishWonLost = plotContent[3:5]
        print("len of stockfish: ", len(stockfish))
        print("len of stockfishWonLost: ", len(stockfishWonLost))

        meanValues = []
        stdValues = []

        colors = ['g', 'r', 'b']
        i=0
        f = plt.figure(1)
        for plot in stockfish:
            plt.plot(plot[0].keys(), plot[1], color=colors[i])
            plt.xlabel("Number of moves",fontsize='13')	
            plt.ylabel("Number of games",fontsize='13')

            meanValues.append(plot[2])
            stdValues.append(plot[3])

            i+=1
        plt.legend(["All games", "Stockfish White", "Stockfish Black"])
        f.savefig("project2/figures/plotOfNumberOfMoves.png")
        
        i=0
        g = plt.figure(2)
        for plot in stockfishWonLost:
            plt.plot(plot[0].keys(), plot[1], color=colors[i])
            plt.xlabel("Number of moves",fontsize='13')	
            plt.ylabel("Number of games",fontsize='13')

            meanValues.append(plot[2])
            stdValues.append(plot[3])

            i+=1
        plt.legend(["Won games", "Lost games"])
        g.savefig("project2/figures/plotOfNumberOfMovesWonLost.png")
        

        self.bodyContent+="<h2>Number of moves</h2>"
        self.bodyContent+="<p>These two plots show some interesting statistics of the games played.</p>"
        self.bodyContent+="<p>In the first plot, we see that if stockfish is Black, it uses more turns than if white.</p>"
        self.bodyContent+="<p>But sometimes these games take much longer time.</p>"
        self.bodyContent+="<p>In the secound plot we see that </p>"
        self.bodyContent+="<p></p>"
        self.bodyContent+="<p></p>"
        self.bodyContent+="<p></p>"
        self.bodyContent+="<p></p>"
                        

        self.bodyContent+="<img src='figures/plotOfNumberOfMoves.png'>"
        self.bodyContent+="<img src='figures/plotOfNumberOfMovesWonLost.png'>"
        self.bodyContent+="<p>In the table below Mean number of moves and the standard deviation of the three plots is shown</p>"
        self.bodyContent+=self._createMeanAndStdTable(meanValues, stdValues)

    def _createMeanAndStdTable(self, mean, std):
        strTable = "<table><tr><th></th><th>Mean moves</th><th>STD</th></tr>"

        typeOfPlot = ["All games", "Stockfish White", "Stockfish Black", "Won games", "Lost games"]
        for i in range(0,5):
            values = "<tr><td>" +typeOfPlot[i]+ "</td><td>"+str(mean[i])+ "</td><td>"+str(std[i])+ "</td></tr>"
            strTable = strTable + values

       
        strTable = strTable + "</table>"
        return strTable

    def createHTMLContent(self):
        self.createHead()
        self.createBody()
        html = self.head + self.title + self.headEnd + self.body + self.documentEnd
        return html

    def write(self):
        content = self.createHTMLContent()
        hs = open("project2/document.html", "w")
        hs.write(content)
        hs.close()