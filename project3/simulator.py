#Import classes
from productionline import Productionline
from batch import Batch
from action import Action
from scheduler import Scheduler
from printer import Printer
from logger import Logger

# Import other modules
import sys
from decimal import *
import copy


class Simulator:

    def __init__(self, path, productionGoal, tasksInUnits, heuristics, loadToInputBufferInterval, groupingOfBatches):
        try:
            if productionGoal <20:
                raise ValueError("Production goal must be more than 20")
            else:
                self.time = round(Decimal(0),1)
                self.productionGoal = productionGoal
                self.tasksInUnits = tasksInUnits
                self.heuristics = heuristics
                self.loadToInputBufferInterval = loadToInputBufferInterval
                self.groupingOfBatches = groupingOfBatches
                self.loadToInputBufferInterval = loadToInputBufferInterval
                self.scheduler = Scheduler()
                self.productionline = Productionline(self.tasksInUnits, self.heuristics)
                self.logger = Logger(path)
                self.printer = Printer(self, self.logger)
                
                self.batches = self.createBatches(self.productionGoal, self.groupingOfBatches)
        except ValueError as e:
            sys.stdout.write("{}{}".format("\t",str(e))+"\n")
            sys.stdout.write("Program terminated\n")
            
            # Exits the program
            sys.exit(1)
    
    # # Getters
    # Returns current simulation time
    def getTime(self):
        return self.time

    # Returns info about the simulation
    def getInfo(self):
        info = [self.productionGoal, self.tasksInUnits, self.heuristics, self.loadToInputBufferInterval, self.groupingOfBatches]
        return info

    # Returns the productionline
    def getProductionline(self):
        return self.productionline
    
    # Returns the scheduler
    def getScheduler(self):
        return self.scheduler
    

    # # Setters
    def updateTime(self):
        self.time = self.time+round(Decimal(0.1),1)


    # # Functions
    # Creates batchs in chosen sizes, and returns a list of batches
    def createBatches(self, numWafers, groupingOfBatches):
        batches = []
        i = 1
        while numWafers>0:
            if numWafers >= groupingOfBatches+20 and numWafers >= groupingOfBatches:
                batches.append(Batch(i,groupingOfBatches))
                numWafers -= groupingOfBatches
            elif 20<=numWafers<=50:
                batches.append(Batch(i,numWafers))
                numWafers = 0
            else:
                batchSize = int(round(numWafers/2,0))
                batches.append(Batch(i,batchSize))
                numWafers -= batchSize
            i+=1
        return batches
    
    # Creates action for loading batches to inputbuffer
    def createLoadToInputBufferAction(self):
        if len(self.batches) == 0:
            return
        batches = copy.copy(self.batches)
        for i in range(len(batches)):
            if (self._atInterval() and self._spaceInInputBuffer(batches[i])):
                batch = self.batches.pop(i)
                self._executeLoadToInputBufferAction(batch)
                break
    
    # Checks if current time is at interval set by user
    def _atInterval(self):
        if (self.time % self.loadToInputBufferInterval)==0:
            return True
        return False

    # Checks if inputbuffer has space for batch
    def _spaceInInputBuffer(self, batch):
        if self.productionline.getBuffer("Input buffer").canAcceptBatch(batch):
            return True
    
    # # Executes load to inputbuffer action
    def _executeLoadToInputBufferAction(self, batch):
        inputbuffer = self.productionline.getBuffer("Input buffer")
        startTime = self.time
        finishTime = self.time + round(Decimal(1),1)
        action = Action("Load batch to 'Input buffer'",batch, startTime, finishTime, inputbuffer)
        self.scheduler.addAction(action)
        action.setStatus(True)
        outputString = "Started loading Batch " + str(action.getBatch().getId()) + " to inputbuffer"
        self.logger.logEvent(self.time,outputString)

    # Checks if simulation is finished
    def isFinished(self):
        if self.productionGoal == self.productionline.getBuffer("Output buffer").getCurrentLoad() and len(self.scheduler.getActions())==0:
            return True
        return False

    # Updates state of the simulation
    def updateState(self):
        #Check ongoing actions
        self._checkOngoingActions()
        
        #Create new actions
        self._createNewActions()

    def _checkOngoingActions(self):
        for action in self.scheduler.getActions():
            if action.getStatus() == True:
                if action.getFinishTime() <= self.time:
                    #Finish action
                    self._finishAction(action)

    def _createNewActions(self):
        for unit in self.productionline.getUnits():
            if unit.getInProduction() == True:
                continue
            newAction = unit.createProductionStartAction(self.time)
            if newAction != None:
                self.scheduler.addAction(newAction)
    
    # Executes pending actions in scheduler 
    def executeNewActions(self):
        actions = self.scheduler.getActions()
        # Skip if there are no actions
        if len(actions) == 0:
            return
        units = self.productionline.getUnits()
        # Check every unit
        for unit in units:
            # Skip if unit is in production
            if unit.getInProduction():
                continue
            # Check if unit can start production of a new batch
            for task in unit.heuristics:
                for action in actions:
                    # Skip "Load to input buffer" actions
                    if action.getTask() == None:
                        continue
                    if action.getTask().getId() == task:
                        self._executeAction(unit,action)

    # Finishes an action that is finished, and removes it from the scheduler
    def _finishAction(self, action):
        if action.getName() == "Load batch to 'Input buffer'":
            #Add batch to inputbuffer
            inputbuffer = action.getInputbuffer()
            inputbuffer.addBatch(action.getBatch())
            # Remove action
            self.scheduler.removeAction(action)
            outputString = "Batch " + str(action.getBatch().getId()) + " added to inputbuffer"
            self.logger.logEvent(self.time,outputString)
        elif action.getName() == "Load to task":
            #Remove batch from buffer
            action.getInputbuffer().removeBatch(action.getBatch())
            newAction = action.getNextAction()
            self.scheduler.removeAction(action)
            self.scheduler.addAction(newAction)
            self._executeAction(None,newAction)
            outputString = "Batch " + str(action.getBatch().getId()) + " loaded to " + str(action.getTask().getName())
            self.logger.logEvent(self.time, outputString)

        elif action.getName() == "Process batch":
            newAction = action.getNextAction()
            self.scheduler.removeAction(action)
            self.scheduler.addAction(newAction)
            self._executeAction(None,newAction)
            outputString ="Batch " + str(action.getBatch().getId()) + " finish processed in " + str(action.getTask().getName())
            self.logger.logEvent(self.time, outputString)
        
        elif action.getName() == "Unload to buffer":
            self.scheduler.removeAction(action)
            action.getTask().getUnit().endProduction()
            action.getOutputbuffer().addBatch(action.getBatch())
            outputString = "Batch " + str(action.getBatch().getId()) + " unloaded to " + str(action.outputbuffer.name)
            self.logger.logEvent(self.time,outputString)

    # Executes an action
    def _executeAction(self, unit,newAction):
        if newAction.getName() == "Load to task":
            unit.setInProduction(True)
            newAction.setStatus(True)
            newAction.getTask().setInProduction(True)
            outputString = "Started loading Batch " + str(newAction.getBatch().getId()) + " to task " + newAction.getTask().getName()
            self.logger.logEvent(self.time,outputString)
        elif newAction.getName() == "Process batch":
            outputString = "Started processing Batch " + str(newAction.getBatch().getId()) + " in task " + newAction.getTask().getName()
            self.logger.logEvent(self.time,outputString)
            newAction.setStatus(True)
        elif newAction.getName() == "Unload to buffer":
            outputString = "Started unloading Batch " + str(newAction.getBatch().getId()) + " from task " + newAction.getTask().getName()
            self.logger.logEvent(self.time,outputString)
            newAction.setStatus(True)
        return 0
    
    # Runs the simulation
    def run(self):
        i = 0
        while not self.isFinished() :
            try:    
                # #Check if ongoing actions is finished, and/or create new actions
                self.updateState()

                # #Check for new action to be executed
                self.executeNewActions()

                # Load new batch into inputbuffer if possible
                self.createLoadToInputBufferAction()

                # Print events to console
                self.printer.printEvents(self.getTime()) 
                if not self.isFinished():
                    # Update time
                    self.updateTime()
                    i += 1
            except ValueError as e:
                sys.stdout.write(str(e) + "\n")
                sys.stdout.write("Simulation terminated\n")
                break
            
        sys.stdout.write("Simulation finished\n")
        self.logger.saveToFile(self.getInfo())


    



if __name__ == "__main__":
    sys.stdout.write("Starting program...\n")
    path = "project3/standardSimulation/"
    productionGoal = 50
    tasksInUnits = [[1,3,6,9],[2,5,7],[4,8]]
    heuristics = [[1,3,6,9],[2,5,7],[4,8]]
    loadToInputBufferInterval = 1
    groupingOfBatches = 50
    SIM = Simulator(path, productionGoal,tasksInUnits, heuristics, loadToInputBufferInterval, groupingOfBatches)
    P = SIM.printer
    SC = SIM.scheduler
    PL = SIM.productionline
    
    SIM.run()
    P.getStatus()
    