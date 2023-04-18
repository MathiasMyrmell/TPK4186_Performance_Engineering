import unittest
from action import Action
from batch import Batch
from buffer import Buffer
from task import Task

class TestContainer(unittest.TestCase):
    @staticmethod
    def exAction() -> Action:
        batch = Batch(1, 20)
        inputBuffer = Buffer("Input", 120)
        outputBuffer = Buffer("Output", 120)
        task = Task(1, "Task", 1)
        return Action("Action", batch, 0, 1, inputBuffer, task, outputBuffer)
    
    def test_getName(self):
        action = self.exAction()
        self.assertEqual(action.getName(), "Action")

    def test_getBatch(self):
        action = self.exAction()
        batch = Batch(1, 20)
        action.batch = batch
        self.assertEqual(action.getBatch(), batch)

    def test_getInputBuffer(self):
        action = self.exAction()
        buffer = Buffer("Input", 120)
        action.inputbuffer = buffer
        self.assertEqual(action.getInputbuffer(), buffer)
    
    def test_getTask(self):
        action = self.exAction()
        task = Task(1, "Task", 1)
        action.task = task
        self.assertEqual(action.getTask(), task)
    
    def test_getOutputBuffer(self):
        action = self.exAction()
        buffer = Buffer("Output", 120)
        action.outputbuffer = buffer
        self.assertEqual(action.getOutputbuffer(), buffer)
    
    def test_getStatus(self):
        action = self.exAction()
        self.assertEqual(action.getStatus(), 0)

    def test_getFinishTime(self):
        action = self.exAction()
        self.assertEqual(action.getFinishTime(), 1)
    
    def test_setNextAction(self):
        action = self.exAction()
        action.setNextAction("Test")
        self.assertEqual(action.nextAction, "Test")
    
    def test_setStatus(self):
        action = self.exAction()
        action.setStatus(1)
        self.assertEqual(action.status, 1)

    def test_getNextAction(self):
        action = self.exAction()
        action.setNextAction("Test")
        self.assertEqual(action.getNextAction(), "Test")
    
    def test_getStatus(self):
        action = self.exAction()
        action.setStatus(1)
        self.assertEqual(action.getStatus(), 1)

if __name__ == '__main__':
    unittest.main()