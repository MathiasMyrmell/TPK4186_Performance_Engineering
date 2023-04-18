import unittest
from unit import Unit
from task import Task


class TestContainer(unittest.TestCase):
    @staticmethod
    def exUnit() -> Unit:
        return Unit("Test", [1, 2, 3])
    def test_getName(self):
        unit = self.exUnit()
        self.assertEqual(unit.getName(), "Test")

    def test_addTaskToUnit(self):
        unit = self.exUnit()
        task1 = Task(1, "Task 1", 1)
        task2 = Task(2, "Task 2", 2)
        task3 = Task(3, "Task 3", 3)
        unit.addTask(task1)
        unit.addTask(task2)
        unit.addTask(task3)
        self.assertEqual(unit.getTasks(), [task1, task2, task3])

    def test_setInProduction(self):
        unit = self.exUnit()
        unit.setInProduction(True)
        self.assertEqual(unit.getInProduction(), True)
    
    def test_getTaskById(self):
        unit = self.exUnit()
        task1 = Task(1, "Task 1", 1)
        task2 = Task(2, "Task 2", 2)
        task3 = Task(3, "Task 3", 3)
        unit.addTask(task1)
        unit.addTask(task2)
        unit.addTask(task3)
        self.assertEqual(unit._getTaskById(1), task1)
        self.assertEqual(unit._getTaskById(2), task2)
        self.assertEqual(unit._getTaskById(3), task3)
        self.assertEqual(unit._getTaskById(4), None)


if __name__ == '__main__':
    unittest.main()