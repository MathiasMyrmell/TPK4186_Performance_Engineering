import unittest
from chessDataBase import ChessDataBase
from game import Game

class TestContainer(unittest.TestCase):
    @staticmethod
    def exDataBase() -> ChessDataBase:
        return ChessDataBase()
    

    
    def test_addGame(self):
        game = Game("White", "Black")
        dB = self.exDataBase()
        dB.addGame(game)
        self.assertEqual(dB.getGames(), [game])



if __name__ == '__main__':
    unittest.main()