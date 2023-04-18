import unittest
from batch import Batch

class TestContainer(unittest.TestCase):
    @staticmethod
    def exBatch() -> Batch:
        return Batch(1,50)
    
    def test_getId(self):
        batch = self.exBatch()
        self.assertEqual(batch.getId(), 1)
    
    def test_getNumWafers(self):
        batch = self.exBatch()
        self.assertEqual(batch.getNumWafers(), 50)


if __name__ == '__main__':
    unittest.main()