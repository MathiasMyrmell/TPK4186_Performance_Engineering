import unittest
from simulator import Simulator
from batch import Batch

class TestContainer(unittest.TestCase):
    @staticmethod
    def exSimulator() -> Simulator:
        return Simulator()
    
    def test_getTime(self):
        simulator = self.exSimulator()
        self.assertEqual(simulator.getTime(), 0)
    
    def test_getUnits(self):
        simulator = self.exSimulator()
        self.assertEqual(simulator.getUnits(), [])

    def test_getInfo(self):
        simulator = self.exSimulator()
        self.assertEqual(simulator.getInfo(), [0, 0, 0, 0, 0])

    def test_getProductionline(self):
        simulator = self.exSimulator()
        self.assertEqual(simulator.getProductionline(), [])
    
    def test_getScheduler(self):
        simulator = self.exSimulator()
        self.assertEqual(simulator.getScheduler(), None)
    
    def test_updateTime(self):
        simulator = self.exSimulator()
        simulator.updateTime()
        self.assertEqual(simulator.getTime(), 0.1)

    def test_createBatches(self):
        simulator = self.exSimulator()
        self.assertEqual(simulator.createBatches(100, 50), [Batch(1, 50), Batch(2, 50)])
    
    def test_createLoadToInputBufferAction(self):
        simulator = self.exSimulator()
        simulator.createBatches(100, 50)
        simulator.createLoadToInputBufferAction()
        self.assertEqual(simulator.batches, [])

    def test_atInterval(self):
        simulator = self.exSimulator()
        self.assertEqual(simulator._atInterval(), True)

    def test_spaceInInputBuffer(self):
        simulator = self.exSimulator()
        self.assertEqual(simulator._spaceInInputBuffer(Batch(1, 50)), True)
    
    def test_executeLoadToInputBufferAction(self):
        simulator = self.exSimulator()
        simulator.createBatches(100, 50)
        simulator.createLoadToInputBufferAction()
        self.assertEqual(simulator.batches, [])

    def test_isFinished(self):
        simulator = self.exSimulator()
        self.assertEqual(simulator.isFinished(), False)




if __name__ == '__main__':
    unittest.main()