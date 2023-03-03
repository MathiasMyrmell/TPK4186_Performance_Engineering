from player import Player
import copy
import math

class Game:

    def __init__(self, white, black):
        self.event = None
        self.site = None
        self.date = None
        self.round = None
        self.white = white
        self.black = black
        self.result = None
        self.ECO = None
        self.opening = None
        self.plycount = None
        self.whiteElo = None
        self.blackElo = None
        
        self.turn = 1
        self.whomsTurn = "White"
        self.pieceName = {
            "K" : "King",
            "Q" :"Queen",
            "R" : "Rook",
            "B" : "Bishop",
            "N" : "Knight",
            "P" : "Pawn"
        }

        self.board = None
        self.createBoard()
        self.moves = []

    def setMetaData(self, metadata):
        self.event = metadata[0][8:-3]
        self.site = metadata[1][7:-3]
        self.date = metadata[2][7:-3]
        self.round = metadata[3][8:-3]
        self.result = metadata[6][9:-3]
        self.ECO = metadata[7][6:-3]
        self.opening = metadata[8][10:-3]
        self.plycount = metadata[9][11:-3]
        self.whiteElo = metadata[10][11:-3]
        self.blackElo = metadata[11][11:-3]
    
    def setMetaDataExcel(self, metadata):
        self.event = metadata[0][6:]
        self.site = metadata[1][5:]
        self.date = metadata[2][5:]
        self.round = metadata[3][6:]
        self.result = metadata[6][7:]
        self.ECO = metadata[7][4:]
        self.opening = metadata[8][8:]
        self.plycount = metadata[9][9:]
        self.whiteElo = metadata[10][9:]
        self.blackElo = metadata[11][9:]
    
    def getMetaData(self):
        return [self.event, self.site, self.date, self.round, self.white, self.black, self.result, self.ECO, self.opening, self.plycount, self.whiteElo, self.blackElo]
   
    def getEvent(self):
        return self.event
    
    def getSite(self):
        return self.site
    
    def getDate(self):
        return self.date
    
    def getRound(self):
        return self.round
    
    def getWhite(self):
        return self.white
    
    def getBlack(self):
        return self.black
    
    def getResult(self):
        return self.result
    
    def getECO(self):
        return self.ECO
    
    def getOpening(self):
        return self.opening
    
    def getPlyCount(self):
        return self.plycount
    
    def getWhiteElo(self):
        return self.whiteElo
    
    def getBlackElo(self):
        return self.blackElo

    def getMoves(self):
        return self.moves


    # Meant for task 1, but it was not completet
    def getTurn(self):
        return self.turn

    def getWhomsTurn(self):
        return self.whomsTurn
    
    def getPieceName(self):
        return self.pieceName

    def getWinner(self):
        result = self.getResult()
        if result == "1/2-1/2":
            return self.getResult(),"Draw"
        elif result == "1-0":
            return self.getResult(),self.getWhite().getName()
        elif result == "0-1":
            return self.getResult(), self.getBlack().getName()

    def getNumberOfMoves(self):
        moves = self.getMoves()
        numMoves = (len(moves) - 1)* 2
        for move in moves[-1]:
            if move == '1-0' or move == "0-1" or move == "1/2-1/2" or move == "None":
                pass
            else:
                numMoves += 1
        return numMoves

    def getNameOfPiece(self,piece):
        pieceNames = self.getPieceName()
        if(piece not in pieceNames):
            print("invalid piece")
        else:
            return pieceNames[piece]

    def createBoard(self):
        board = {
            "a8" : "bR",
            "b8" : "bN",
            "c8" : "bB",
            "d8" : "bQ",
            "e8" : "bK",
            "f8" : "bB",
            "g8" : "bN",
            "h8" : "bR",
            "a7" : "bP",
            "b7" : "bP",
            "c7" : "bP",
            "d7" : "bP",
            "e7" : "bP",
            "f7" : "bP",
            "g7" : "bP",
            "h7" : "bP",
            "a6" : "",
            "b6" : "",
            "c6" : "",
            "d6" : "",
            "e6" : "",
            "f6" : "",
            "g6" : "",
            "h6" : "",
            "a5" : "",
            "b5" : "",
            "c5" : "",
            "d5" : "",
            "e5" : "",
            "f5" : "",
            "g5" : "",
            "h5" : "",
            "a4" : "",
            "b4" : "",
            "c4" : "",
            "d4" : "",
            "e4" : "",
            "f4" : "",
            "g4" : "",
            "h4" : "",
            "a3" : "",
            "b3" : "",
            "c3" : "",
            "d3" : "",
            "e3" : "",
            "f3" : "",
            "g3" : "",
            "h3" : "",
            "a2" : "wP",
            "b2" : "wP",
            "c2" : "wP",
            "d2" : "wP",
            "e2" : "wP",
            "f2" : "wP",
            "g2" : "wP",
            "h2" : "wP",
            "a1" : "wR",
            "b1" : "wN",
            "c1" : "wB",
            "d1" : "wQ",
            "e1" : "bK",
            "f1" : "wB",
            "g1" : "wN",
            "h1" : "wR",

        }
        self.setBoard(board)
    
    def setBoard(self,board):
        self.board = board
    
    def getBoard(self):
        return copy.copy(self.board)
    
    def setMoves(self,moves):
        self.moves = moves
   
    def printBoard(self):
        board = self.getBoard()
        keys = board.keys()
        returnString ="-----------------------------------------"+"\n""|"
        for k in keys:
            if(board[k]==""):
                returnString+="    "+"|"
            else:
                returnString+=" "+board[k]+" "+"|"
            if(k[0]=="h"):
                returnString +="\n"+"-----------------------------------------"+"\n"+"|"
                
        print(returnString[:-1])
    # Meant for task 1, but it was not completet
    
    # _getMetaData and _getMoves only used for __str__ 
    def _getMetaData(self):
        event = "[Event"+" "+"\""+str(self.getEvent())+"\""+"]"+"\n"
        site = "[Site"+" "+"\""+str(self.getSite())+"\""+"]"+"\n"
        date = "[Date"+" "+"\""+str(self.getDate())+"\""+"]"+"\n"
        round = "[Round"+" "+"\""+str(self.getRound())+"\""+"]"+"\n"
        white = "[White"+" "+"\""+str(self.getWhite().getName())+"\""+"]"+"\n"
        black = "[Black"+" "+"\""+str(self.getBlack().getName())+"\""+"]"+"\n"
        result = "[Result"+" "+"\""+str(self.getResult())+"\""+"]"+"\n"
        eco = "[ECO"+" "+"\""+str(self.getECO())+"\""+"]"+"\n"
        opening = "[Opening"+" "+"\""+str(self.getOpening())+"\""+"]"+"\n"
        plyCount = "[PlyCount"+" "+"\""+str(self.getPlyCount())+"\""+"]"+"\n"
        whiteELo = "[WhiteElo"+" "+"\""+str(self.getWhiteElo())+"\""+"]"+"\n"
        blackElo = "[BlackElo"+" "+"\""+str(self.getBlackElo())+"\""+"]"+"\n"
        returnString = event+site+date+round+white+black+result+eco+opening+plyCount+whiteELo+blackElo+"\n"
        return returnString
    
    def _getMoves(self):
        moves = self.getMoves()
        returnString = ""
        for i in range(len(moves)):
            turn = str(i+1)
            time = "{+0.00/1 0s}"

            returnString += turn + ". " + moves[i][0] +" "+time +" " + moves[i][1] + " "+time+" "
        returnString += "\n"

        newReturnString = ""
        numLines = math.ceil(len(returnString)/79) #79 is was width of the provided svg file  
        for i in range(numLines):
            newReturnString+=returnString[i*79:(i+1)*79]

        return newReturnString


    def __str__(self):
        
        returnString = self._getMetaData()+self._getMoves()
        return returnString
    
if __name__ == "__main__":
    p1 = Player("Magnus Carlsen")
    p2 = Player("Fabiano Caruana")
    g1 = Game(p1,p2)
    g1.createBoard()
    g1.printBoard()