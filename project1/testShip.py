from ships import Ship
from container import Container
import unittest

class TestContainer(unittest.TestCase):
    @staticmethod
    def exShip() -> Ship:
        ship = Ship(8, 4, 4)
        ship.createDecks()
        return ship

    def test_getLength(self):
        self.assertEqual(self.exShip().getLength(), 8)

    def test_getWidth(self):
        self.assertEqual(self.exShip().getWidth(), 4)

    def test_getHeight(self):
        self.assertEqual(self.exShip().getHeight(), 4)
    
    def test_getContainers(self):
        self.assertEqual(self.exShip().getContainers(), [])

    def test_addContainer(self):
        ship = self.exShip()
        container = Container(20, 1)
        ship.addContainer(container)
        self.assertEqual(ship.getContainers(), [container])
    
    def test_removeContainer(self):
        ship = self.exShip()
        container = Container(20, 1)
        ship.addContainer(container)
        ship.removeContainer(container)
        self.assertEqual(ship.getContainers(), [])
    
    def test__findPlacement(self):
        ship = self.exShip()
        container = Container(20, 1)
        ship.addContainer(container)
        self.assertEqual(ship._findPlacement(container), ((1, 0, 1),))
    
    def test__occupiedUnder(self):
        ship = self.exShip()
        container = Container(20, 1)
        ship.addContainer(container)
        self.assertEqual(ship._occupiedUnder((1, 0, 1)), True)

    def test_loadShip(self):
        ship = self.exShip()
        container = Container(20, 1)
        ship.loadShip([container])
        self.assertEqual(ship.getContainers(), [container])

if __name__ == '__main__':
    unittest.main()

    


