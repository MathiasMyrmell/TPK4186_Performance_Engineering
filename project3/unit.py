from decimal import *
from action import Action

class Unit:

    def __init__(self, name, heuristics):
        # Initial values
        self.name = name
        self.heuristics = heuristics
        # Production values
        self.tasks = []
        self.inProduction = False
        
    
    # # Getters
    # Returns name
    def getName(self):
        return self.name

    # Returns tasks in unit
    def getTasks(self):
        return self.tasks
    
    # Returns if unit is in production or not
    def getInProduction(self):
        return self.inProduction


    # # Setters
    # Sets units production status
    def setInProduction(self, inProduction):
        self.inProduction = inProduction


    # # Functions
    # Adds task to unit
    def addTask(self, task):
        task.setUnit(self)
        self.tasks.append(task)

    def _getTaskById(self, id):
        for task in self.tasks:
            if task.getId() == id:
                return task
        return None
    
    # Ends production
    def endProduction(self):
        self.inProduction = False
        for task in self.tasks:
            task.endProduction()

    # Creates action to start production
    def createProductionStartAction(self, startTime):
        for id in self.heuristics:
            task = self._getTaskById(id)
            if task != None:
                for batch in task.getInputbuffer().getBatches():
                    if task.canAcceptBatch(batch):
                        # #Create action
                        # Load to task action
                        finishTime = startTime + round(Decimal(1),1)
                        loadAction= Action("Load to task", batch, startTime, finishTime, task.getInputbuffer(), task)
                        # Process action
                        startTime = finishTime
                        finishTime = startTime + task.calculateProcessingTime(batch)
                        
                        processAction = Action("Process batch", batch, startTime, finishTime, None, task)
                        # Unload action
                        startTime = finishTime
                        finishTime = startTime + round(Decimal(1),1)
                        unloadAction = Action("Unload to buffer", batch, startTime, finishTime, None , task, task.getOutputBuffer())
                        
                        # Set next action for each action
                        processAction.setNextAction(unloadAction)
                        loadAction.setNextAction(processAction)
                        return loadAction