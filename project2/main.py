

from game import Game
from player import Player
from chessDataBase import ChessDataBase
from document import Document
import re
import matplotlib.pyplot as plt
import copy

import math


chessGames = []
def loadGame(path):
    if type(path) == str:
        return _loadGamesFromPath(path)
    elif type(path) == ChessDataBase:
        return _loadGamesFromDataBase(path)
    

def _getNumberOfLines(path):
    file = open(path, "r")
    lines = 0
    for line in file:
        lines+=1
    file.close()
    return lines

def _getBreakPoints(path):
    file = open(path, "r")
    breakPoints = []
    for i, line in enumerate(file):
        if "[Event" in line:
            breakPoints.append(i)
    file.close()
    numLinnes = _getNumberOfLines(path)
    breakPoints.append(numLinnes)
    return breakPoints

def _loadGamesFromPath(path):
    game = None
    metadata = None
    movePairs = []
    moves = ""
    file = None
    breakPoints = []
    games = ChessDataBase()
    try:
        file = open(path, "r")
        #Find line where new game starts
        breakPoints = _getBreakPoints(path)
        lines = file.readlines()
        gameNr = 0


        for i in range(len(lines)):#len(lines)
            if i in breakPoints:
                metadata = lines[i:i+13]
                #Move lines from-to
                moveFrom = i+13
                nextStart = breakPoints[gameNr+1]
                moveTo = nextStart
                moves = lines[moveFrom:moveTo-1]

                #Create game
                game = _createGameFromLoad(metadata[4], metadata[5])
                game.setMetaData(metadata)
                movePairs = _createMovesFromLoad(moves)
                game.setMoves(movePairs)
                games.addGame(game)

                #Restart variables
                metadata = []
                moves = ""
                game = None
                gameNr+=1

        file.close()
    except:
        print("could not read file")
    
    return games

def _createGameFromLoad(p1N, p2N):
    p1Name = p1N[8:-3]
    p1 = Player(p1Name)
    p2Name = p2N[8:-3]
    p2 = Player(p2Name)
    game = Game(p1,p2)
    return game

def _createMovesFromLoad(moves):
    s = ""
    for i in moves:
        s+=i.replace("\n"," ")

    #Remove everything except moves
    splitted = s.split(" ")
    for i in range(len(splitted)):
        if "." in splitted[i]:
            splitted[i] = " "
        elif "{" in splitted[i]:
            splitted[i] = " "
        elif '}' in splitted[i]:
            splitted[i] = " "
    
    #Sanitize
    list = []
    for i in splitted:
        if i == " " or i == "":
            continue
        else:
            list.append(i)

    #Create return list
    #Collect moves in pairs per turn
    returnList = []
    for i in range(len(list)-2):
        if i%2 == 0:
            returnList.append((list[i],list[i+1]))
    if(len(list)%2 == 1):
        returnList.append((list[len(list)-1],"None"))
    else:
        returnList.append((list[len(list)-2],list[len(list)-1]))

    return returnList

def _loadGamesFromDataBase(path):
    games = path.getGames()
    for i in games:
        chessGames.append(i)


#Task 7
def statisticsStockfish(database):
    games = database.getGames()
    print("Number of games: ", len(games))
    winnerWhite = 0
    drawWhite = 0
    loserWhite = 0
    winnerBlack = 0
    drawBlack = 0
    loserBlack = 0
    totalWinner = 0
    totalDraw = 0
    totalLoser = 0

    for game in games:
        #Get color of Stockfish
        color = None
        if game.getWhite().getName() == "Stockfish 15 64-bit":
            color = "White"
        elif game.getBlack().getName() == "Stockfish 15 64-bit":
            color = "Black"

        # print(color)
        
        #get winner
        result = game.getWinner()[0]
        winner = game.getWinner()[1]
        
        # print(result, winner)
        
        if result == "1-0":
            if color == "White":
                winnerWhite+=1
            elif color == "Black":
                loserBlack+=1
        elif result == "0-1":
            if color == "White":
                loserWhite+=1
            elif color == "Black":
                winnerBlack+=1
        elif result == "1/2-1/2":
            if color == "White":
                drawWhite+=1
            elif color == "Black":
                drawBlack+=1
        


        # if result == "1/2-1/2":
        #     print("")

    totalWinner = winnerWhite+winnerBlack
    totalDraw = drawWhite+drawBlack
    totalLoser = loserWhite+loserBlack

    print("White: ", winnerWhite, drawWhite, loserWhite)
    print("Black: ", winnerBlack, drawBlack, loserBlack)
    print("Total: ", totalWinner, totalDraw, totalLoser)

    return winnerWhite, drawWhite, loserWhite, winnerBlack, drawBlack, loserBlack, totalWinner, totalDraw, totalLoser

#Task 8
def task8(database):
    #All games
    allGames = plotOfNumberOfMoves(copy.copy(database))

    #Stockfish with white
    SW= stockfishWhite(copy.copy(database))


    return allGames, SW
    #All games

def allGames(databse):
    games = database.getGames()
    # for i in range(1):
    #     print(games[i].getNumberOfMoves())

    #Dictionary with number of moves as key and number of games as value
    moves = {}


    for game in games:
        numMoves = game.getNumberOfMoves()
        if numMoves in moves:
            moves[numMoves]+=1
        else:
            moves[numMoves] = 1

def plotOfNumberOfMoves(database):
    #Assuumptions: one turn = two moves
    games = database.getGames()
    # for i in range(1):
    #     print(games[i].getNumberOfMoves())

    #Dictionary with number of moves as key and number of games as value
    moves = {}


    for game in games:
        numMoves = game.getNumberOfMoves()
        if numMoves in moves:
            moves[numMoves]+=1
        else:
            moves[numMoves] = 1

    #Sort dictionary
    sortedDict = {}
    for i in range(len(moves)):
        minValue = min(moves.keys())
        sortedDict[minValue] = moves[minValue]
        moves.pop(minValue)

    yValues = []
    minValue = min(sortedDict.keys())
    maxValue = max(sortedDict.keys())
    for i in sortedDict.keys():#range(minValue, maxValue+1)
        keys = sortedDict.keys()
        value = 0
        for k in keys:
            if k>=i:
                value+=sortedDict[k]
        yValues.append(value)

    #Mean, standard deviation
    mean = 0
    for i in sortedDict.keys():
        mean+=i*sortedDict[i]
    mean = mean/len(games)

    std = 0
    for i in sortedDict.keys():
        std+=(i-mean)**2*sortedDict[i]
    std = round(math.sqrt(std/len(games)),2)

    return sortedDict, yValues, mean, std

def stockfishWhite(database):
    games = database.getGames()
    moves = {}
    for game in games:
        if game.getWhite().getName() == "Stockfish 15 64-bit":
            numMoves = game.getNumberOfMoves()
            if numMoves in moves:
                moves[numMoves]+=1
            else:
                moves[numMoves] = 1
    returnValue = plotOfNumberOfMoves(moves)
    #Sort dictionary
    sortedDict = {}
    for i in range(len(moves)):
        minValue = min(moves.keys())
        sortedDict[minValue] = moves[minValue]
        moves.pop(minValue)

    yValues = []
    minValue = min(sortedDict.keys())
    maxValue = max(sortedDict.keys())
    for i in sortedDict.keys():#range(minValue, maxValue+1)
        keys = sortedDict.keys()
        value = 0
        for k in keys:
            if k>=i:
                value+=sortedDict[k]
        yValues.append(value)

    #Mean, standard deviation
    mean = 0
    for i in sortedDict.keys():
        mean+=i*sortedDict[i]
    mean = mean/len(games)

    std = 0
    for i in sortedDict.keys():
        std+=(i-mean)**2*sortedDict[i]
    std = round(math.sqrt(std/len(games)),2)

    return sortedDict, yValues, mean, std


if __name__ == "__main__":
    path = "project2/datafiles/Stockfish_15_64-bit.commented.2600.pgn"
    p1 = Player("Stockfish")
    p1.setColor("White")
    p2 = Player("Mathias")
    p2.setColor("Black")
    g = Game(p1,p2)
    # g.createBoard()

    g.movePiece(p1,"Pa2a4")

    g.printBoard()

    # g._getMoves()
    # g.saveGame()


    # database = loadGame(path)
    # games = database.getGames()
    # loadGame(database)

    #Task 7
    path100 = "project2/datafiles/stockfishGames100.pgn"
    database = loadGame(path100)
    stat = statisticsStockfish(database)

    moves = task8(database)[1]

    










    #Task 6
    doc = Document()
    doc.createStatTable(stat)
    doc.createPlot(moves)
    doc.write()