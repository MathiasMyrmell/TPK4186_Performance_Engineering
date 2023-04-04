
from buffer import Buffer
from batch import Batch
from unit import Unit
from task import Task

class Productionline:

    def __init__(self):
        self.units = []
        self.tasks = []
        self.buffers = []
        self.finished = False
        self.createLine()
    
    #Get list of units
    def getUnits(self):
        return self.units

    #Get list of tasks
    def getTasks(self):
        return self.tasks
    
    #Get list of buffers
    def getBuffers(self):
        return self.buffers
    
    #Get finished status
    def isFinished(self, productionGoal):
        numWafersProduced = self.buffers[-1].currentLoad
        lastTaskInProduction = self.tasks[-1].getInProduction()

        if (numWafersProduced == productionGoal) and not lastTaskInProduction:
            return True
        return False
    
    #Set finished status
    # def setFinished(self, finished):
    #     self.finished = finished

    #Get buffer by name
    def getBuffer(self, name):
        for buffer in self.buffers:
            if(buffer.getName() == name):
                return buffer
        return None

    #Get task by name
    def getTask(self, name):
        for task in self.tasks:
            if(task.getName() == name):
                return task
        return None


    #Initialize the production line
    def createLine(self):
        print("Creating production line...")
        #Create batches

        #Create units
        self._createUnits()

        #Create Tasks
        self._createTasks()

        #Create Buffers
        self._createBuffers()

        #Link tasks to buffers
        self._linkTasksToBuffers()

        #Add Tasks to units
        self._addTasksToUnits()

        print("Production line created")



    def _createUnits(self):
        self.units.append(Unit("Unit 1"))
        self.units.append(Unit("Unit 2"))
        self.units.append(Unit("Unit 3"))
        print("\t Units created")

    def _createTasks(self):
        self.tasks.append(Task("Task 1",0.5))
        self.tasks.append(Task("Task 2",3.5))
        self.tasks.append(Task("Task 3",1.2))
        self.tasks.append(Task("Task 4",3))
        self.tasks.append(Task("Task 5",0.8))
        self.tasks.append(Task("Task 6",0.5))
        self.tasks.append(Task("Task 7",1))
        self.tasks.append(Task("Task 8",1.9))
        self.tasks.append(Task("Task 9",0.3))
        print("\t Tasks created")

    def _createBuffers(self):
        self.buffers.append(Buffer("Input buffer", float('inf')))
        self.buffers.append(Buffer("Buffer 1",120))
        self.buffers.append(Buffer("Buffer 2",120))
        self.buffers.append(Buffer("Buffer 3",120))
        self.buffers.append(Buffer("Buffer 4",120))
        self.buffers.append(Buffer("Buffer 5",120))
        self.buffers.append(Buffer("Buffer 6",120))
        self.buffers.append(Buffer("Buffer 7",120))
        self.buffers.append(Buffer("Buffer 8",120))
        self.buffers.append(Buffer("Output buffer",float('inf')))
        print("\t Buffers created")
    
    def _linkTasksToBuffers(self):
        #Task 1
        task1 = self.tasks[0]
        inputBuffer = self.buffers[0]
        buffer1 = self.buffers[1]
        task1.setPreviousBuffer(inputBuffer)
        task1.setNextBuffer(buffer1)
        #Task 2
        task2 = self.tasks[1]
        buffer1 = self.buffers[1]
        buffer2 = self.buffers[2]
        task2.setPreviousBuffer(buffer1)
        task2.setNextBuffer(buffer2)
        #Task 3
        task3 = self.tasks[2]
        buffer2 = self.buffers[2]
        buffer3 = self.buffers[3]
        task3.setPreviousBuffer(buffer2)
        task3.setNextBuffer(buffer3)
        #Task 4
        task4 = self.tasks[3]
        buffer3 = self.buffers[3]
        buffer4 = self.buffers[4]
        task4.setPreviousBuffer(buffer3)
        task4.setNextBuffer(buffer4)
        #Task 5
        task5 = self.tasks[4]
        buffer4 = self.buffers[4]
        buffer5 = self.buffers[5]
        task5.setPreviousBuffer(buffer4)
        task5.setNextBuffer(buffer5)
        #Task 6
        task6 = self.tasks[5]
        buffer5 = self.buffers[5]
        buffer6 = self.buffers[6]
        task6.setPreviousBuffer(buffer5)
        task6.setNextBuffer(buffer6)
        #Task 7
        task7 = self.tasks[6]
        buffer6 = self.buffers[6]
        buffer7 = self.buffers[7]
        task7.setPreviousBuffer(buffer6)
        task7.setNextBuffer(buffer7)
        #Task 8
        task8 = self.tasks[7]
        buffer7 = self.buffers[7]
        buffer8 = self.buffers[8]
        task8.setPreviousBuffer(buffer7)
        task8.setNextBuffer(buffer8)
        #Task 9
        task9 = self.tasks[8]
        buffer8 = self.buffers[8]
        outputBuffer = self.buffers[9]
        task9.setPreviousBuffer(buffer8)
        task9.setNextBuffer(outputBuffer)

        print("\t Tasks linked to buffers")

    def _addTasksToUnits(self):
        #Unit 1
        unit1 = self.units[0]
        task1 = self.tasks[0]
        task3 = self.tasks[2]
        task6 = self.tasks[5]
        task9 = self.tasks[8]
        unit1.addTask(task1)
        unit1.addTask(task3)
        unit1.addTask(task6)
        unit1.addTask(task9)
        #Unit 2
        unit2 = self.units[1]
        task2 = self.tasks[1]
        task5 = self.tasks[4]
        task7 = self.tasks[6]
        unit2.addTask(task2)
        unit2.addTask(task5)
        unit2.addTask(task7)
        #Unit 3
        unit3 = self.units[2]
        task4 = self.tasks[3]
        task8 = self.tasks[7]
        unit3.addTask(task4)
        unit3.addTask(task8)

        print("\t Tasks added to units")
  
    def loadBuffer(self, buffer, batch):
        if(not buffer.isFull()):
            buffer.addBatch(batch)



if __name__ == "__main__":
    PRODUCTIONGOAL = 51
    PL = Productionline()



