import unittest
from buffer import Buffer
from batch import Batch

class TestContainer(unittest.TestCase):
    @staticmethod
    def exBuffer() -> Buffer:
        return Buffer("Test", 120)
   
    def test_getName(self):
        buffer = self.exBuffer()
        self.assertEqual(buffer.getName(), "Test")

    def test_getMaxCapacity(self):
        buffer = self.exBuffer()
        self.assertEqual(buffer.getMaxCapacity(), 120)
    
    def test_getBatches(self):
        buffer = self.exBuffer()
        self.assertEqual(buffer.getBatches(), [])
    
    def test_getCurrentLoad(self):
        buffer = self.exBuffer()
        self.assertEqual(buffer.getCurrentLoad(), 0)
    
    def test_setNextTask(self):
        buffer = self.exBuffer()
        buffer.setNextTask("Test")
        self.assertEqual(buffer.nextTask, "Test")

    def test_setPreviousTask(self):
        buffer = self.exBuffer()
        buffer.setPreviousTask("Test")
        self.assertEqual(buffer.previousTask, "Test")

    def test_addBatch(self):
        buffer = self.exBuffer()
        batch = Batch(1, 20)
        buffer.addBatch(batch)
        self.assertEqual(buffer.getBatches(), [batch])
        self.assertEqual(buffer.getCurrentLoad(), 20)
    
    def test_removeBatch(self):
        buffer = self.exBuffer()
        batch = Batch(1, 20)
        buffer.addBatch(batch)
        buffer.removeBatch(batch)
        self.assertEqual(buffer.getBatches(), [])
        self.assertEqual(buffer.getCurrentLoad(), 0)
    
    def test_removeBatchException(self):
        buffer = self.exBuffer()
        batch = Batch(1, 20)
        with self.assertRaises(Exception):
            buffer.removeBatch(batch)
    
  


if __name__ == '__main__':
    unittest.main()