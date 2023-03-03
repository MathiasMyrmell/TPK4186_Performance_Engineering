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
        self.style = "<link rel='stylesheet' href='style.css'> "
        self.headEnd = "</head>"
        self.bodyStart = "<body>"
        self.body = ""
        self.bodyEnd = "</body>"

        self.documentEnd = "</html>"

    def createHead(self):
        headStart = "<html><head>"
        title = "<title>"+self.name+"</title>"
        headEnd = "</head>"
        self.head = headStart + title +self.style+headEnd

    def createBody(self):
        bodyStart = "<body>"
        bodyTitle = "<h1>"+self.name+"</h1>"
        bodyEnd = "</body>"
        self.body = bodyStart + bodyTitle + self.bodyContent + bodyEnd


    #Task 7
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


    #Task 8
    def createPlot(self, plotContent):
        stockfish = plotContent[0:3]
        stockfishWonLost = plotContent[3:5]

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
                        

        self.bodyContent+="<img src='/project2/figures/plotOfNumberOfMoves.png'>"
        self.bodyContent+="<img src='/project2/figures/plotOfNumberOfMovesWonLost.png'>"
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

    #Task 11
    def createWinnersTable(self,b):
        tables = ""
        for tree in b:
            totWinnerWhite = 0
            totWinnerBlack = 0
            totDraw = 0
            startNode = tree[0]
            leafNodes = tree[1]
            table = "<h3>Winner "+startNode+"</h3><table >"
            tableHead = "<tr> <th colspan='4'>"+startNode+"</tr>"
            tableSubHead = "<tr> <th>Path</th> <th>Winner white</th> <th>Winner black</th> <th>Draw</th></tr>"
            table+=tableHead+tableSubHead
            for lF in leafNodes:
                leafNode = lF[0]
                pastNode = lF[1]
                result = lF[2]
                winnerWhite = result[0]
                winnerBlack = result[1]
                draw = result[2]
                totWinnerWhite += winnerWhite
                totWinnerBlack += winnerBlack
                totDraw += draw
                tableRow = "<tr> <td>"+startNode+"..."+pastNode+","+leafNode+"</td> <td>"+str(winnerWhite)+"</td> <td>"+str(winnerBlack)+"</td> <td>"+str(draw)+"</td> </tr>"
                table = table + tableRow
            rowTot = "<tr> <td>Total</td> <td>"+str(totWinnerWhite)+"</td> <td>"+str(totWinnerBlack)+"</td> <td>"+str(totDraw)+"</td> </tr>"
            table = table + rowTot + "</table>"
            tables+=table+"</br>"+"<img src='/project2/trees/"+startNode+".png'   height = 300px'>"
        self.bodyContent+="<h2>Winners</h2>"
        self.bodyContent+="<p>This table shows the number of times Stockfish has won, drawn and lost, with white pieces, black pieces, for each opening.</p>"
        self.bodyContent+=tables


    #Task 12
    def createOpeningsTable(self, openings, numberOfTimesPlayed):
        tables = ""
        for op in openings:
            startNode = op[0]
            table = "<h3>Opening "+startNode+"</h3><table > <tr colspan = '2'> <th>"+startNode+"</th> </tr> <tr> <th>Opening</th> <th>Number of games</th> </tr>"
            
            for i in range(1, len(op)):
                tableRow  = "<tr> <td>"+startNode+"..."+op[i][0]+","+str(op[i][1])+"</td> <td>"+str(op[i][2])+"</td> </tr>"
                table = table + tableRow
            table = table + "</table></br>"
            tables+=table


        self.bodyContent+="<h2>Openings</h2>"
        self.bodyContent+="<p>This tables shows the openings whom are played more than "+str(numberOfTimesPlayed)+" times.</p>"
        self.bodyContent+=tables

    # Created HTML document
    def createHTMLContent(self):
        self.createHead()
        self.createBody()
        html = self.head + self.title + self.headEnd + self.body + self.documentEnd
        return html

    # writes the HTML document to a file
    def write(self):
        content = self.createHTMLContent()
        hs = open("project2/document/document.html", "w")
        hs.write(content)
        hs.close()