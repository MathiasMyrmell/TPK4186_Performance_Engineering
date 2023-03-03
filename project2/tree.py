#Task 9
from node import Node

class Tree:
    def __init__(self, game):
        self.root = None
        self.structure = []
        self.initilizingNewTree(game)
        self.structureTimesPlayed = []
        self.winnerFromLeaf = []
        self.timesPlayedLeaf = []


    def getRoot(self):
        return self.root
    
    def setRoot(self, node):
        self.root = node

    def setTreeStructure(self, structure):
        self.structure = structure

    def getTreeStructure(self):
        return self.structure
    
    def initilizingNewTree(self, game):
        moves = self.moves(game)
        self.setRoot(Node("White", moves[0], None, self))
        self.getRoot().setLevel(0)
        self.getRoot().addGame(moves[1:])

    def addNewGameToTree(self, game):
        moves = self.moves(game)
        self.getRoot().addGame(moves[1:])
    
    #Task 11
    def removeNodesUnderGivenDepth(self, depth):
        self.getRoot().removeNodesUnderDepth(depth)
    
    def getWinnersFromLeafs(self):
        winners = self.getRoot().getWinnersFromLeafs()
        winners = self.getWinnerFromLeaf()
        return winners

    def setWinnerFromLeaf(self, winner):
        self.winnerFromLeaf.append(winner)
                
    def getWinnerFromLeaf(self):
        return self.winnerFromLeaf

    #Task 12
    def getTimesPlayedLeaf(self):
        timesPlayed = self.getRoot().getTimesPlayedLeaf()
        timesPlayed = self.getTimesPlayed()
        return timesPlayed
    
    def setTimesPlayedLeaf(self, timesPlayed):
        self.timesPlayedLeaf.append(timesPlayed)

    def getTimesPlayed(self):
        return self.timesPlayedLeaf

        
    # Help function to change format of moves
    def moves(self, g1):
        moves = []
        for move in g1.getMoves():
            moves.append(move[0])
            moves.append(move[1])
        return moves
    
    #Create tree structure
    def createTreeStructure(self):
        self.setTreeStructure(self.getRoot().getStructure())
        return self.getTreeStructure()
    
if __name__ == "__main__":
    tree = Tree()

