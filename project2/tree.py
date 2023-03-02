#Task 9
from node import Node

class Tree:

    def __init__(self, game):
        self.root = None
        self.structure = []
        self.initilizingNewTree(game)

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
        # print("adding new tree")
        self.setRoot(Node("White", moves[0], None))
        # print("root: ", self.getRoot().getNodeValue())
        # print("pastNode: ", self.getRoot().getPastNode())
        # print("moves:1", moves[1:])
        self.getRoot().addGame(moves[1:])




    def addNewGameToTree(self, game):
        # print("adding new game to tree")
        moves = self.moves(game)
        # print("moves: ", moves)
        self.getRoot().addGame(moves[1:])
        
        

    
    # def addGame(self, g1):
    #     moves = self.moves(g1)
    #     if self.getRoot().getNodeValue() == moves[0]:
    #         print("adding to tree with root: ", self.getRoot().getNodeValue())
    #         moves = moves[1:]
    #         self.getRoot().addGame(moves, False)
    #     else:
    #         print("adding new tree")
    #         self.getRoot().addGame(moves, True)
    #     # # self.getRoot().setNodeValue(moves[0])
    #     # # if self.getRoot().getNodeValue() == moves[0]:
    #     # #     self.getRoot().addGame(moves, False)
    #     # # else:
    #     # #     self.getRoot().addGame(moves, True)
    #     # self.getRoot().addGame(moves, True)
    



    def moves(self, g1):
        moves = []
        for move in g1.getMoves():
            # print("moveW: ", move[0])
            # print("moveB: ", move[1])
            moves.append(move[0])
            moves.append(move[1])
        # print("moves: ", moves)
        return moves
    

    def createTreeStructure(self):
        self.setTreeStructure(self.getRoot().getStructure())
        return self.getTreeStructure()

if __name__ == "__main__":
    tree = Tree()

