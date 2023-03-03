#Task 4


class ChessDataBase():

    def __init__(self):
        self.games = []
        self.dataBase = []

    def addGame(self, game):
        self.games.append(game)

    def getGames(self):
        return self.games
    
    
