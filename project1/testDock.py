from ships import Ship
from container import Container
from dock import Dock
import unittest

class TestContainer(unittest.TestCase):
    @staticmethod
    def exDock() -> Dock:
        return Dock()
    
    def test_dockShip(self):
        dock = self.exDock()
        ship = Ship(8, 4, 4)
        ship.createDecks()
        dock.dockShip(ship)
        self.assertEqual(dock.getShip(), ship)
    
    def test_undockShip(self):
        dock = self.exDock()
        ship = Ship(8, 4, 4)
        ship.createDecks()
        dock.dockShip(ship)
        dock.undockShip()
        self.assertEqual(dock.getShip(), None)

    def test_unloadShip(self):
        dock = self.exDock()
        ship = Ship(8, 4, 4)
        ship.createDecks()
        container = Container(20, 1)
        ship.loadShip([container])
        dock.dockShip(ship)
        dock.unloadShip(1)
        self.assertEqual(dock.getShip().getContainers(), [])

if __name__ == '__main__':
    unittest.main()

    


