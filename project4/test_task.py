import unittest

from task import Task

class TestTask(unittest.TestCase):
    @staticmethod
    def exTask() -> Task:
        return Task(1, "Task", "A", "Test", [1,2,3])

    def test_setDurations(self):
        task = self.exTask()
        task.setDurations([2, 4, 6])
        self.assertEqual(task.getDurations(), [2, 4, 6])
    
    def test_setDuration(self):
        task = self.exTask()
        duration = task.getDurations()[1]
        task.setDuration(duration)
        self.assertEqual(task.getDuration(), duration)
    

    
    def test_setPredecessors(self):
        task = self.exTask()
        pre1 = Task(2, "Task", "B", "Pre1", [1,2,3])
        pre2 = Task(3, "Task", "C", "Pre2", [3,6,9])
        task.setPredecessors([pre1, pre2])
        self.assertEqual(task.getPredecessors(), [pre1, pre2])
    
    def test_getSuccessors(self):
        task = self.exTask()
        suc1 = Task(4, "Task", "D", "Suc1", [1,2,3])
        suc2 = Task(5, "Task", "E", "Suc2", [3,6,9])
        task.successors.append(suc1)
        task.successors.append(suc2)
        self.assertEqual(task.getSuccessors(), [suc1, suc2])
    
    def test_getType(self):
        task = self.exTask()
        self.assertEqual(task.getType(), "Task")

    def test_getCode(self):
        task = self.exTask()
        self.assertEqual(task.getCode(), "A")
    
    def test_getDuration(self):
        task = self.exTask()
        self.assertEqual(task.getDuration(), 2)

    def test_getDurations(self):
        task = self.exTask()
        self.assertEqual(task.getDurations(), [1,2,3])


    
if __name__ == '__main__':
    unittest.main()
    
