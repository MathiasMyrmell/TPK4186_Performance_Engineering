

from game import Game
from player import Player
from chessDataBase import ChessDataBase
from document import Document
import re
import matplotlib.pyplot as plt
import copy
import openpyxl

import math



# #Task 2
def importGame(path, number):
    game = None
    try:
        file = open(path, "r")
        #Find line where new game starts
        breakPoints = _getBreakPoints(path)
        lines = file.readlines()
        gameNr = 1

        for i in range(len(lines)):#len(lines)
            if i in breakPoints and gameNr == number:
                metadata = lines[i:i+13]
                # #Move lines from-to
                moveFrom = i+13
                nextStart = breakPoints[gameNr]
                moveTo = nextStart
                moves = lines[moveFrom:moveTo-1]
                #Create game
                game = _createGameFromLoad(metadata[4], metadata[5])
                game.setMetaData(metadata)
                movePairs = _createMovesFromLoad(moves)
                game.setMoves(movePairs)
            if i in breakPoints:
                gameNr+=1
           
        file.close()
    except:
        print("could not read file")
    
    return game

# #Task 3
def saveGame(path, game):
    print()
    try:
        file = open(path, "r")
        file.close()
    except:
        print("could not read file")
    try:
        #Open file in append mode
        file = open(path, "a")
        #Add metadata
        metadata = game._getMetaData()
        file.write(metadata)

        #Add moves
        moves = game._getMoves()
        # file.write(moves)
        for line in moves:
            print(line)
            file.write(line+"\n")
        file.flush()
        file.close()
    except:
        print("could not append to file")
    return 0


# #Task 4
#Load games
def loadGames(path):
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
    chessGames = []
    for i in games:
        chessGames.append(i)
    return chessGames

#Save games
def saveGames(dataBase, games):
    for game in games:
        dataBase.addGame(game)

# #Task 5
#Load data from Excel file
def loadFromExcel(path):
    print()

#Save data to Excel file
def saveToExcel(game):
    workbook = openpyxl.Workbook()
    ws = workbook.active
    ws.title = "Chess"
    metaNameColumn = "B"
    metaValueColumn = "C"
    metaData = game.getMetaData()
    if len(metaData)==12:
        metaDataNames = ["Event", "Site", "Date", "Round", "White", "Black", "Result", "ECO", "Opening", "PlyCount", "WhiteElo", "BlackElo"]
    elif len(metaData)==13:
        metaDataNames = ["Event", "Site", "Date", "Round", "White", "Black", "Result", "ECO", "Opening", "Variation", "PlyCount", "WhiteElo", "BlackElo"]

    # print("len(metaDataNames): ", len(metaDataNames))
    # print("len(metaData): ", len(metaData))

    lineCount = 1
    #Add metadata
    for i in range(len(metaDataNames)):
        name = metaDataNames[i]
        value = metaData[i]
        if type(value) == Player:
            value = value.getName()
        metaNamePlacement = metaNameColumn+str(i+1)
        metaValuePlacement = metaValueColumn+str(i+1)
        ws[metaNamePlacement] = name
        ws[metaValuePlacement] = value
        lineCount+=1

    #Add moves
    moves = game.getMoves()
    print("moves: ", moves)
    turnCount = 1
    lineCount+=1
    turnColumn = "B"
    whiteColumn = "C"
    blackColumn = "D"
    ws[turnColumn+str(lineCount)] = "Turn"
    ws[whiteColumn+str(lineCount)] = "White"
    ws[blackColumn+str(lineCount)] = "Black"
    lineCount+=1
    for i in range(lineCount,lineCount+len(moves)):
        turn = turnCount
        white = moves[turnCount-1][0]
        black = moves[turnCount-1][1]

        ws[turnColumn+str(i)] = turn
        ws[whiteColumn+str(i)] = white
        ws[blackColumn+str(i)] = black
        turnCount+=1

    workbook.save("project2/DataFiles/Chess.xlsx")


# #Task 7
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

# #Task 8
def createPlots(database):
    #All games
    AG = _allGames(copy.copy(database))

    #Stockfish with white
    SW= _stockfishWhite(copy.copy(database))

    #Stockfish with black
    SB = _stockfishBlack(copy.copy(database))

    #Stockfish winning
    SW = _stockfishWinning(copy.copy(database))

    #Stockfish losing
    SL = _stockfishLosing(copy.copy(database))

    return AG, SW, SB, SW, SL
    #All games

def _allGames(database):
    games = database.getGames()
    moves = {}

    for game in games:
        numMoves = game.getNumberOfMoves()
        if numMoves in moves:
            moves[numMoves]+=1
        else:
            moves[numMoves] = 1
    
    return _plotOfNumberOfMoves(games,moves)

def _stockfishWhite(database):
    games = database.getGames()
    moves = {}
    for game in games:
        if game.getWhite().getName() == "Stockfish 15 64-bit":
            numMoves = game.getNumberOfMoves()
            if numMoves in moves:
                moves[numMoves]+=1
            else:
                moves[numMoves] = 1
    return _plotOfNumberOfMoves(games,moves)

def _stockfishBlack(database):
    games = database.getGames()
    moves = {}
    for game in games:
        if game.getBlack().getName() == "Stockfish 15 64-bit":
            numMoves = game.getNumberOfMoves()
            if numMoves in moves:
                moves[numMoves]+=1
            else:
                moves[numMoves] = 1
    return _plotOfNumberOfMoves(games,moves)    

def _stockfishWinning(database):
    games = database.getGames()
    moves = {}
    for game in games:
        if game.getWinner()[1] == "Stockfish 15 64-bit":
            numMoves = game.getNumberOfMoves()
            if numMoves in moves:
                moves[numMoves]+=1
            else:
                moves[numMoves] = 1
    return _plotOfNumberOfMoves(games,moves)

def _stockfishLosing(database):
    games = database.getGames()
    moves = {}
    for game in games:
        if game.getWinner()[1] != "Stockfish 15 64-bit" and game.getWinner()[1] != "Draw":
            numMoves = game.getNumberOfMoves()
            if numMoves in moves:
                moves[numMoves]+=1
            else:
                moves[numMoves] = 1
    return _plotOfNumberOfMoves(games,moves)

def _plotOfNumberOfMoves(games, moves):
    #Assuumptions: one turn = two moves

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
    mean = round(mean/len(sortedDict.values()),2)

    std = 0
    for i in sortedDict.keys():
        std+=(i-mean)**2*sortedDict[i]
    std = round(math.sqrt(std/len(games)),2)

    return sortedDict, yValues, mean, std



# #Task 9
"project2/datafiles/games.txt"


if __name__ == "__main__":
    path = "project2/datafiles/Stockfish_15_64-bit.commented.2600.pgn"

    # #Task 1
    # p1 = Player("Stockfish")
    # p1.setColor("White")
    # p2 = Player("Mathias")
    # p2.setColor("Black")
    # g = Game(p1,p2)
    # g.createBoard()

    # g.movePiece(p1,"Pa2a4")


    # #Task 2
    #Parh for task 5
    pathtask5 = "project2/datafiles/games.txt"
    g2 = importGame(pathtask5,3)
    # print(g2)

    # #Task 3
    # saveGame("project2/datafiles/games.txt",g)

    # #Task 4
    #Load from file
    # games = loadGames(path)

    #Save to database
    # database = ChessDataBase()
    # listOfGames = games.getGames()
    # saveGames(database,listOfGames)

    # #Task 5
    saveToExcel(g2)

   

    # #Task 7
    # database = loadGames(path)
    # stat = statisticsStockfish(database)

  
    # #Task 8
    # moves = createPlots(database)
  
  
    # #Task 9

    # #Task 10

    # #Task 11

    # #Task 12

    
    # #Task 6
    # doc = Document("Stockfish")
    # doc.createStatTable(stat)
    # doc.createPlot(moves)
    # doc.write()




    