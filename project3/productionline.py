
from buffer import Buffer
from batch import Batch
from unit import Unit
from task import Task
import sys
class Productionline:

    def __init__(self,unit1Heuristic, unit2Heuristic, unit3Heuristic):
        self.units = []
        self.tasks = []
        self.buffers = []
        self.finished = False
        self.createLine(unit1Heuristic, unit2Heuristic, unit3Heuristic)
    
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
    def createLine(self,unit1Heuristic, unit2Heuristic, unit3Heuristic):
        print("Creating production line...")
        #Create batches

        #Create units
        self._createUnits(unit1Heuristic, unit2Heuristic, unit3Heuristic)

        #Create Tasks
        self._createTasks()

        #Create Buffers
        self._createBuffers()

        #Link tasks to buffers
        self._linkTasksToBuffers()

        #Add Tasks to units
        self._addTasksToUnits()

        print("Production line created")


    def _createUnits(self,unit1Heuristic, unit2Heuristic, unit3Heuristic):
        self.units.append(Unit("Unit 1",unit1Heuristic))
        self.units.append(Unit("Unit 2",unit2Heuristic))
        self.units.append(Unit("Unit 3",unit3Heuristic))
        print("\t Units created")

    def _createTasks(self):
        processingTimes = [0.5,3.5,1.2,3,0.8,0.5,1,1.9,0.3]
        for i in range(1,10):
            self.tasks.append(Task(i,"Task "+str(i),processingTimes[i-1]))
        # self.tasks.append(Task(1,"Task 1",0.5))
        # self.tasks.append(Task(2,"Task 2",3.5))
        # self.tasks.append(Task(3,"Task 3",1.2))
        # self.tasks.append(Task(4,"Task 4",3))
        # self.tasks.append(Task(5,"Task 5",0.8))
        # self.tasks.append(Task(6,"Task 6",0.5))
        # self.tasks.append(Task(7,"Task 7",1))
        # self.tasks.append(Task(8,"Task 8",1.9))
        # self.tasks.append(Task(9,"Task 9",0.3))
        print("\t Tasks created")

    def _createBuffers(self):
        self.buffers.append(Buffer("Input buffer",120)) #float('inf')
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
        task1.setInputbuffer(inputBuffer)
        task1.setOutputBuffer(buffer1)
        #Task 2
        task2 = self.tasks[1]
        buffer1 = self.buffers[1]
        buffer2 = self.buffers[2]
        task2.setInputbuffer(buffer1)
        task2.setOutputBuffer(buffer2)
        #Task 3
        task3 = self.tasks[2]
        buffer2 = self.buffers[2]
        buffer3 = self.buffers[3]
        task3.setInputbuffer(buffer2)
        task3.setOutputBuffer(buffer3)
        #Task 4
        task4 = self.tasks[3]
        buffer3 = self.buffers[3]
        buffer4 = self.buffers[4]
        task4.setInputbuffer(buffer3)
        task4.setOutputBuffer(buffer4)
        #Task 5
        task5 = self.tasks[4]
        buffer4 = self.buffers[4]
        buffer5 = self.buffers[5]
        task5.setInputbuffer(buffer4)
        task5.setOutputBuffer(buffer5)
        #Task 6
        task6 = self.tasks[5]
        buffer5 = self.buffers[5]
        buffer6 = self.buffers[6]
        task6.setInputbuffer(buffer5)
        task6.setOutputBuffer(buffer6)
        #Task 7
        task7 = self.tasks[6]
        buffer6 = self.buffers[6]
        buffer7 = self.buffers[7]
        task7.setInputbuffer(buffer6)
        task7.setOutputBuffer(buffer7)
        #Task 8
        task8 = self.tasks[7]
        buffer7 = self.buffers[7]
        buffer8 = self.buffers[8]
        task8.setInputbuffer(buffer7)
        task8.setOutputBuffer(buffer8)
        #Task 9
        task9 = self.tasks[8]
        buffer8 = self.buffers[8]
        outputBuffer = self.buffers[9]
        task9.setInputbuffer(buffer8)
        task9.setOutputBuffer(outputBuffer)

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

    def loadBatchFromBufferToTask(self, batch, buffer):
        task = buffer.getNextTask()
        task.startProduction(batch,0)#ADD START TIME
        buffer.removeBatch(batch)

    def loadBatchFromTaskToBuffer(self, batch, task):
        buffer = task.getNextBuffer()
        buffer.addBatch(batch)
        task.endProduction()

    def status(self):
        returnValue = ""
        for buffer in self.buffers:
            returnValue += buffer.getName() + ": " + str(buffer.currentLoad) + " wafers\n"
        for task in self.tasks:
            returnValue += task.getName() + ": " +"Production? " +str(task.getInProduction())+"\n"
        sys.stdout.write(returnValue)

    def findBatch(self, batch):
        for buffer in self.buffers:
            for ba in buffer.batches:
                if ba == batch:
                    return buffer
        for task in self.tasks:
            if task.batch == batch:
                return task
            
        return None


if __name__ == "__main__":
    PRODUCTIONGOAL = 51
    PL = Productionline()
    #Create batch
    batch = Batch(25)

    #Load batch to input buffer
    PL.loadBuffer(PL.buffers[0], batch)


    # #V1
    #Load batch from input buffer to task1
    PL.loadBatchFromBufferToTask(batch, PL.buffers[0])
    
    #Load batch from task1 to buffer1
    PL.loadBatchFromTaskToBuffer(batch, PL.tasks[0])
    
    #Load batch from buffer1 to task2
    PL.loadBatchFromBufferToTask(batch, PL.buffers[1])

    #Load batch from task2 to buffer2
    PL.loadBatchFromTaskToBuffer(batch, PL.tasks[1])

    #Load batch from buffer2 to task3
    PL.loadBatchFromBufferToTask(batch, PL.buffers[2])

    #Load batch from task3 to buffer3
    PL.loadBatchFromTaskToBuffer(batch, PL.tasks[2])

    #Load batch from buffer3 to task4
    PL.loadBatchFromBufferToTask(batch, PL.buffers[3])

    #Load batch from task4 to buffer4
    PL.loadBatchFromTaskToBuffer(batch, PL.tasks[3])

    #Load batch from buffer4 to task5
    PL.loadBatchFromBufferToTask(batch, PL.buffers[4])

    #Load batch from task5 to buffer5
    PL.loadBatchFromTaskToBuffer(batch, PL.tasks[4])

    #Load batch from buffer5 to task6
    PL.loadBatchFromBufferToTask(batch, PL.buffers[5])

    #Load batch from task6 to buffer6
    PL.loadBatchFromTaskToBuffer(batch, PL.tasks[5])

    #Load batch from buffer6 to task7
    PL.loadBatchFromBufferToTask(batch, PL.buffers[6])

    #Load batch from task7 to buffer7
    PL.loadBatchFromTaskToBuffer(batch, PL.tasks[6])

    #Load batch from buffer7 to task8
    PL.loadBatchFromBufferToTask(batch, PL.buffers[7])
    
    #Load batch from task8 to buffer8
    PL.loadBatchFromTaskToBuffer(batch, PL.tasks[7])

    #Load batch from buffer8 to task9
    PL.loadBatchFromBufferToTask(batch, PL.buffers[8])

    #Load batch from task9 to Output buffer
    PL.loadBatchFromTaskToBuffer(batch, PL.tasks[8])
    PL.status()
    

