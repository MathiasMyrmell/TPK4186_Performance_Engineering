import unittest
from task import Task
from buffer import Buffer
from unit import Unit
from batch import Batch

class TestContainer(unittest.TestCase):
    @staticmethod
    def exTask() -> Task:
        return Task(1, "Test", 1)
    
    def test_getId(self):
        task = self.exTask()
        self.assertEqual(task.getId(), 1)

    def test_getName(self):
        task = self.exTask()
        self.assertEqual(task.getName(), "Test")

    def test_getInputbuffer(self):
        task = self.exTask()
        self.assertEqual(task.getInputbuffer(), None)

    def test_getOutputBuffer(self):
        task = self.exTask()
        self.assertEqual(task.getOutputBuffer(), None)
    
    def test_getUnit(self):
        task = self.exTask()
        self.assertEqual(task.getUnit(), None)
    
    def test_getInProduction(self):
        task = self.exTask()
        self.assertEqual(task.getInProduction(), False)
    
    def test_setInputbuffer(self):
        task = self.exTask()
        buffer = Buffer("Output", 120)
        task.setInputbuffer(buffer)
        self.assertEqual(task.getInputbuffer(), buffer)
    
    def test_setOutputBuffer(self):
        task = self.exTask()
        buffer = Buffer("Output", 120)
        task.setOutputBuffer(buffer)
        self.assertEqual(task.getOutputBuffer(), buffer)
    
    def test_setUnit(self):
        task = self.exTask()
        task.setUnit(1)
        self.assertEqual(task.getUnit(), 1)
    
    def test_setInProduction(self):
        task = self.exTask()
        task.setInProduction(True)
        self.assertEqual(task.getInProduction(), True)
    
    def test_setInProduction(self):
        task = self.exTask()
        task.setInProduction(True)
        self.assertEqual(task.getInProduction(), True)
    
    def test_calculateProcessingTime(self):
        task = self.exTask()
        batch = Batch(1, 20)
        self.assertEqual(task.calculateProcessingTime(batch), 20.0)

    def test_endProduction(self):
        task = self.exTask()
        task.setInProduction(True)
        unit = Unit("Test", [1, 2, 3])
        task.setUnit(unit)
        task.endProduction()
        self.assertEqual(task.getInProduction(), False)

    def test_canAcceptBatch(self):
        task = self.exTask()
        batch = Batch(1, 20)
        unit = Unit("Test", [1, 2, 3])
        task.setUnit(unit)
        buffer = Buffer("Output", 120)
        task.setOutputBuffer(buffer)
        self.assertEqual(task.canAcceptBatch(batch), True)
    


if __name__ == '__main__':
    unittest.main()