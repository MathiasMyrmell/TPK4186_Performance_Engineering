
from buffer import Buffer
from batch import Batch
from unit import Unit
from task import Task
import sys
class Productionline:

    def __init__(self,tasksInUnit,heuristics):#TODO: fiks printlines
        self.units = []
        self.tasks = []
        self.buffers = []
        self.finished = False
        self.createLine(tasksInUnit,heuristics)
    
    # # Getters
    #Returns units
    def getUnits(self):
        return self.units

    #Returns tasks
    def getTasks(self):
        return self.tasks
    
    #Returns buffers
    def getBuffers(self):
        return self.buffers
    
    #Returns buffer by name
    def getBuffer(self, name):
        for buffer in self.buffers:
            if(buffer.getName() == name):
                return buffer
        return None

    # # Functions
    #Initialize the production line
    def createLine(self,tasksInUnits,heuristics):
        # print("Creating production line...")
        #Create batches

        #Create units
        self._createUnits(heuristics)

        #Create Tasks
        self._createTasks()

        #Create Buffers
        self._createBuffers()

        #Link tasks to buffers
        self._linkTasksToBuffers()

        #Add Tasks to units
        self._addTasksToUnits(tasksInUnits)

        # print("Production line created")

    def _createUnits(self,heuristics):
        for i in range(len(heuristics)):
            self.units.append(Unit("Unit "+str(i+1),heuristics[i]))
        # print("\t Units created")

    def _createTasks(self):
        processingTimes = [0.5,3.5,1.2,3,0.8,0.5,1,1.9,0.3]
        for i in range(1,10):
            self.tasks.append(Task(i,"Task "+str(i),processingTimes[i-1]))

        # print("\t Tasks created")

    def _createBuffers(self):
        self.buffers.append(Buffer("Input buffer",120))
        for i in range(1,9):
            self.buffers.append(Buffer("Buffer "+str(i),120))
        self.buffers.append(Buffer("Output buffer",float('inf')))
        # print("\t Buffers created")
    
    def _linkTasksToBuffers(self):
        for i in range(0,9):
            self.tasks[i].setInputbuffer(self.buffers[i])
            self.tasks[i].setOutputBuffer(self.buffers[i+1])

        # print("\t Tasks linked to buffers")

    def _addTasksToUnits(self, tasksInUnits):
        for i in range(len(self.units)):
            unit = self.units[i]
            for task in tasksInUnits[i]:
                unit.addTask(self.tasks[task-1])
        # print("\t Tasks added to units")
  


   #Get task by name
    # def getTask(self, name):
    #     for task in self.tasks:
    #         if(task.getName() == name):
    #             return task
    #     return None

    #Get finished status
    # def isFinished(self, productionGoal):
    #     numWafersProduced = self.buffers[-1].currentLoad
    #     lastTaskInProduction = self.tasks[-1].getInProduction()
    #     if (numWafersProduced == productionGoal) and not lastTaskInProduction:
    #         return True
    #     return False
    
    #Set finished status
    # def setFinished(self, finished):
    #     self.finished = finished

    # def loadBuffer(self, buffer, batch):
    #     if(not buffer.isFull()):
    #         buffer.addBatch(batch)

    # def loadBatchFromBufferToTask(self, batch, buffer):
    #     task = buffer.getNextTask()
    #     task.startProduction(batch,0)#ADD START TIME
    #     buffer.removeBatch(batch)

    # def loadBatchFromTaskToBuffer(self, batch, task):
    #     buffer = task.getNextBuffer()
    #     buffer.addBatch(batch)
    #     task.endProduction()

    # def status(self):
    #     returnValue = ""
    #     for buffer in self.buffers:
    #         returnValue += buffer.getName() + ": " + str(buffer.currentLoad) + " wafers\n"
    #     for task in self.tasks:
    #         returnValue += task.getName() + ": " +"Production? " +str(task.getInProduction())+"\n"
    #     sys.stdout.write(returnValue)

    # def findBatch(self, batch):
    #     for buffer in self.buffers:
    #         for ba in buffer.batches:
    #             if ba == batch:
    #                 return buffer
    #     for task in self.tasks:
    #         if task.batch == batch:
    #             return task
            
    #     return None


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
    

