import unittest
from container import Container

class TestContainer(unittest.TestCase):
    @staticmethod
    def exContainer() -> Container:
        return Container(20, 1)
    
    def test_getidNr(self):
        self.assertEqual(self.exContainer().getidNr(), 1)

    def test_getLength(self):
        self.assertEqual(self.exContainer().getLength(), 20)
    
    def test_getStartWeight(self):
        self.assertEqual(self.exContainer().getStartWeight(), 2000)
    
    def test_getMaxCargoWeight(self):
        self.assertEqual(self.exContainer().getMaxCargoWeight(), 20000)
    
    def test_getCargoWeight(self):
        self.assertEqual(self.exContainer().getCargoWeight(), 0)
    
    def test_setCargoWeight(self):
        container = self.exContainer()
        container.setCargoWeight(1000)
        self.assertEqual(container.getCargoWeight(), 1000)
    
    def test_getTotalWeight(self):
        self.assertEqual(self.exContainer().getTotalWeight(), 2000)
    
    def test_setTotalWeight(self):
        container = self.exContainer()
        container.setCargoWeight(1000)
        self.assertEqual(container.getTotalWeight(), 3000)
    

if __name__ == '__main__':
    unittest.main()