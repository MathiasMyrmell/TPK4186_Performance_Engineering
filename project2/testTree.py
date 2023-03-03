import unittest
from tree import Tree
from node import Node
from game import Game

class TestContainer(unittest.TestCase):
    @staticmethod
    def exTree() -> Tree:
        game = Game("White", "Black")
        game.setMoves(["(f4, e5)"])
        return Tree(game)
    
    def test_setRoot(self):
        tree = self.exTree()
        node = Node("White", "f4", None, self)
        tree.setRoot(node)
        self.assertEqual(tree.getRoot(), node)
    
    def test_setTreeStructure(self):
        tree = self.exTree()
        tree.setTreeStructure(["f4", "e5"])
        self.assertEqual(tree.getTreeStructure(), ["f4", "e5"])



if __name__ == '__main__':
    unittest.main()