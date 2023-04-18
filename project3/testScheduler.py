import unittest
from scheduler import Scheduler

class TestContainer(unittest.TestCase):
    @staticmethod
    def exScheduler() -> Scheduler:
        return Scheduler()

    def test_addAction(self):
        scheduler = self.exScheduler()
        scheduler.addAction(1)
        self.assertEqual(scheduler.getActions(), [1])
    
    def test_removeAction(self):
        scheduler = self.exScheduler()
        scheduler.addAction(1)
        scheduler.removeAction(1)
        self.assertEqual(scheduler.getActions(), [])
    
    def test_getActions(self):
        scheduler = self.exScheduler()
        scheduler.addAction(1)
        self.assertEqual(scheduler.getActions(), [1])

if __name__ == '__main__':
    unittest.main()