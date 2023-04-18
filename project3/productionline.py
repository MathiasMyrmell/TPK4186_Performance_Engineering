
from buffer import Buffer
from unit import Unit
from task import Task
class Productionline:

    def __init__(self,tasksInUnit,heuristics):
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
        print("Creating production line...")
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

        print("Production line created")

    def _createUnits(self,heuristics):
        for i in range(len(heuristics)):
            self.units.append(Unit("Unit "+str(i+1),heuristics[i]))
        print("\t Units created")

    def _createTasks(self):
        processingTimes = [0.5,3.5,1.2,3,0.8,0.5,1,1.9,0.3]
        for i in range(1,10):
            self.tasks.append(Task(i,"Task "+str(i),processingTimes[i-1]))

        print("\t Tasks created")

    def _createBuffers(self):
        self.buffers.append(Buffer("Input buffer",120))
        for i in range(1,9):
            self.buffers.append(Buffer("Buffer "+str(i),120))
        self.buffers.append(Buffer("Output buffer",float('inf')))
        print("\t Buffers created")
    
    def _linkTasksToBuffers(self):
        for i in range(0,9):
            self.tasks[i].setInputbuffer(self.buffers[i])
            self.tasks[i].setOutputBuffer(self.buffers[i+1])

        print("\t Tasks linked to buffers")

    def _addTasksToUnits(self, tasksInUnits):
        for i in range(len(self.units)):
            unit = self.units[i]
            for task in tasksInUnits[i]:
                unit.addTask(self.tasks[task-1])
        print("\t Tasks added to units")
  
