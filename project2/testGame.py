import unittest
from game import Game

class TestContainer(unittest.TestCase):
    @staticmethod
    def exGame() -> Game:
        return Game("Stockfish", "Magnus Carlsen")
    def test_setMetaData(self):
        metadata =['[Event "CCRL 40/15"]\n', '[Site "CCRL"]\n', '[Date "2022.12.19"]\n', '[Round "857.2.659"]\n', '[White "Rebel 16 64-bit"]\n', '[Black "Stockfish 15 64-bit"]\n', '[Result "1/2-1/2"]\n', '[ECO "E58"]\n', '[Opening "Nimzo-Indian"]\n', '[PlyCount "165"]\n', '[WhiteElo "3397"]\n', '[BlackElo "3511"]\n']
        game = self.exGame()
        game.setMetaData(metadata)
        self.assertEqual(game.getEvent(), "CCRL 40/15")
        self.assertEqual(game.getSite(), "CCRL")
        self.assertEqual(game.getDate(), "2022.12.19")
        self.assertEqual(game.getRound(), "857.2.659")
        self.assertEqual(game.getWhite(), "Stockfish")
        self.assertEqual(game.getBlack(), "Magnus Carlsen")
        self.assertEqual(game.getResult(), "1/2-1/2")
        self.assertEqual(game.getECO(), "E58")
        self.assertEqual(game.getOpening(), "Nimzo-Indian")
        self.assertEqual(game.getPlyCount(), "165")
        self.assertEqual(game.getWhiteElo(), "3397")
        self.assertEqual(game.getBlackElo(), "3511")

    def test_getWinner(self):
        metadata =['[Event "CCRL 40/15"]\n', '[Site "CCRL"]\n', '[Date "2022.12.19"]\n', '[Round "857.2.659"]\n', '[White "Rebel 16 64-bit"]\n', '[Black "Stockfish 15 64-bit"]\n', '[Result "1/2-1/2"]\n', '[ECO "E58"]\n', '[Opening "Nimzo-Indian"]\n', '[PlyCount "165"]\n', '[WhiteElo "3397"]\n', '[BlackElo "3511"]\n']
        game = self.exGame()
        game.setMetaData(metadata)
        self.assertEqual(game.getWinner()[1], "Draw")



if __name__ == '__main__':
    unittest.main()