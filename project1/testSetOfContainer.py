from ships import Ship
from container import Container
from setOfContainers import setOfContainers
import unittest

class TestContainer(unittest.TestCase):
    @staticmethod
    def exSCon() -> setOfContainers:
        liste = []
        return setOfContainers(liste)
    
    def test_getContainerList(self):
        self.assertEqual(self.exSCon().getContainerList(), [])
    
    def test_addContainer(self):
        sCon = self.exSCon()
        container = Container(20, 1)
        sCon.addContainer(container)
        self.assertEqual(sCon.getContainerList(), [container])
    
    def test_removeContainer(self):
        sCon = self.exSCon()
        container = Container(20, 1)
        sCon.addContainer(container)
        sCon.removeContainer(container)
        self.assertEqual(sCon.getContainerList(), [])
    
    def test_getContainersByIndex(self):
        sCon = self.exSCon()
        container = Container(20, 1)
        sCon.addContainer(container)
        self.assertEqual(sCon.getContainerByIndex(0), container)
    
    def test_getContainersById(self):
        sCon = self.exSCon()
        container = Container(20, 1)
        sCon.addContainer(container)
        self.assertEqual(sCon.getContainerById(1), container)

if __name__ == '__main__':

    unittest.main()