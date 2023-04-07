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
class Simulator:

    def __init__(self, productionGoal, tasksInUnits, heuristics, loadToInputBufferInterval, groupingOfBatches):
        try:
            if productionGoal <20:
                raise ValueError("Production goal must be more than 20")
            else:
                self.time = round(Decimal(0),1)
                self.productionGoal = productionGoal
                self.loadToInputBufferInterval = loadToInputBufferInterval
                self.scheduler = Scheduler()
                self.productionline = Productionline(tasksInUnits, heuristics)
                self.logger = Logger(self)
                self.printer = Printer(self)
                
                self.batches = self.createBatches(self.productionGoal, groupingOfBatches)
        except ValueError as e:
            sys.stdout.write("{}{}".format("\t",str(e))+"\n")
            sys.stdout.write("Program terminated\n")
            
            # Exits the program
            sys.exit(1)
    
    # # Getters
    def getTime(self):
        return self.time



    # # Setters
    def updateTime(self):
        self.time = self.time+round(Decimal(0.1),1)


    # # Functions
    def createBatches(self, numWafers, groupingOfBatches):
        batches = []
        i = 1
        while(numWafers > 0):
            if(numWafers//50==0):
                batches.append(Batch(i,numWafers))
                numWafers = 0
            elif(numWafers//50 > 1):
                batches.append(Batch(i,50))
                numWafers -= 50
            elif(numWafers%50 == 0):
                batches.append(Batch(i,50))
                numWafers -= 50
            else:
                if(numWafers%50 < 20):
                    num = int(numWafers/2)
                    batches.append(Batch(i,num))
                    numWafers -= num
                else:
                    batches.append(Batch(i,50))
                    numWafers -= 50
            i+=1
        return batches
    


    def createLoadToInputBufferAction(self):
        # Assumption: Loadingtime to first inputbuffer = 0
        if len(self.batches) == 0:
            return
        elif self.time == round(Decimal(0),1) or (self.time % self.loadToInputBufferInterval)==0:
            print("Creating new action")
            inputbuffer = self.productionline.getBuffer("Input buffer")
            batch = self.batches.pop(0)
            startTime = self.time
            finishTime = self.time + round(Decimal(1),1)
            action = Action("Load batch to 'Input buffer'",batch, startTime, finishTime, inputbuffer)
            self.scheduler.addAction(action)
            self._executeLoadToInputBufferAction(action)

    def _executeLoadToInputBufferAction(self, action):
        if self._canActionBeExecuted(action):
            action.setStatus(True)
            outputString = "Started loading Batch " + str(action.getBatch().getId()) + " to inputbuffer"
            sys.stdout.write(outputString+"\n")
            self.logger.logEvent(outputString)
    
    ##### TODO: MÅ FIKSES
    def _canActionBeExecuted(self,action):
        if action.getName() == "Load batch to 'Input buffer'":
            #Check if inputbuffer has space
            inputbuffer = self.productionline.getBuffer("Input buffer")
            if inputbuffer.maxCapacity-inputbuffer.currentLoad >= action.batch.numWafers:
                return True
        elif action.getName()== "Load batch from buffer to task":
            batch = action.getBatch()
            buffer = self.productionline.findBatch(batch)
            if buffer == None:
                return False
            elif buffer.getNextTask().canAcceptBatch(batch):
                return True

        elif action.getName() == "Load batch from task to buffer":
            batch = action.getBatch()
            task = self.productionline.findBatch(batch)
            if task != None:
                return True

        
        return False
   

    def isFinished(self):
        # if len(self.scheduler.actions) == 0:
        #     return True
        # return False
        # print("Productiongoal == produced", self.productionGoal == self.productionline.getBuffer("Output buffer").currentLoad)
        # print("Number of actions:", len(self.scheduler.actions))
        if self.productionGoal == self.productionline.getBuffer("Output buffer").getCurrentLoad() and len(self.scheduler.getActions())==0:
            return True
        return False

    def checkIfProductionIsValid(self):
        #Check if only on task per unit is in production at a time
        for unit in self.productionline.getUnits():
            tasksInProduction = 0
            for task in unit.getTasks():
                if task.getInProduction():
                    tasksInProduction += 1
            if tasksInProduction > 1:
                self.printer.getStatus()
                raise ValueError("More than one task in production at a time")


    #TODO: SJEKK DENNE
    def executeNewActions(self):
        if len(self.scheduler.getActions()) == 0:
            return
        units = self.productionline.getUnits()
        # Check every unit
        for unit in units:
            # Check if unit is in production
            if unit.getInProduction():
                print("Unit is in production")
                continue
            # Check if unit can start production of a new batch
            for heuristic in unit.heuristics:
                # print(heuristic)
                pass
                

                    

            #     unit.startProduction(self.time)



    def updateState(self):
        #Check ongoing actions
        for action in self.scheduler.getActions():
            if action.getStatus() == True:
                if action.getFinishTime() <= self.time:
                    #Finish action
                    self._finishAction(action)
                    break
        #Create new actions
        for unit in self.productionline.getUnits():
            if unit.getInProduction() == True:
                # print(unit.name," is in production")
                continue
            # print(unit.name, "is not in production")
            newAction = unit.createProductionStartAction(self.time)
            if newAction != None:
                # unit.inProduction = True
                self.scheduler.addAction(newAction)
                self.executeAction(unit,newAction)
                break

        # print("\n")
        # for unit in self.productionline.units:
        #     if unit.inProduction == False:
        #         newAction = unit.createProductionStartAction(self.time)
        #         if newAction != None:
        #             # unit.inProduction = True
        #             self.scheduler.addAction(newAction)
        #             break
    
    def _finishAction(self, action):
        if action.getName() == "Load batch to 'Input buffer'":
            #Add batch to inputbuffer
            inputbuffer = action.getInputbuffer()
            inputbuffer.addBatch(action.getBatch())
            # Remove action
            self.scheduler.removeAction(action)
            print("Batch loaded to inputbuffer")
            outputString = "Batch " + str(action.getBatch().getId()) + " added to inputbuffer"
            self.logger.logEvent(outputString)
        elif action.getName() == "Load to task":
            #Remove batch from buffer
            action.getInputbuffer().removeBatch(action.getBatch())
            print("Batch loaded to ", action.getTask().getName())
            newAction = action.getNextAction()
            self.scheduler.removeAction(action)
            self.scheduler.addAction(newAction)
            self.executeAction(None,newAction)
            outputString = "Batch " + str(action.getBatch().getId()) + " loaded to " + str(action.getTask().getName())
            self.logger.logEvent(outputString)

        elif action.getName() == "Process batch":
            print("Batch processed")
            newAction = action.getNextAction()
            self.scheduler.removeAction(action)
            self.scheduler.addAction(newAction)
            self.executeAction(None,newAction)
            outputString ="Batch " + str(action.getBatch().getId()) + " finish processed in " + str(action.getTask().getName())
            self.logger.logEvent(outputString)
        
        elif action.getName() == "Unload to buffer":
            print("Batch unloaded to buffer")
            self.scheduler.removeAction(action)
            action.getTask().getUnit().endProduction()
            action.getOutputbuffer().addBatch(action.getBatch())
            outputString = "Batch " + str(action.getBatch().getId()) + " unloaded to " + str(action.outputbuffer.name)
            self.logger.logEvent(outputString)



    def executeAction(self, unit,newAction):
        if newAction.getName() == "Load to task":
            unit.setInProduction(True)
            newAction.setStatus(True)
            newAction.getTask().setInProduction(True)
            print("Started loading batch to task")
            outputString = "Started loading Batch " + str(newAction.getBatch().getId()) + " to task " + newAction.getTask().getName()
            self.logger.logEvent(outputString)
        elif newAction.getName() == "Process batch":
            print("Started processing batch")
            outputString = "Started processing Batch " + str(newAction.getBatch().getId()) + " in task " + newAction.getTask().getName()
            self.logger.logEvent(outputString)
            newAction.setStatus(True)
        elif newAction.getName() == "Unload to buffer":
            print("Started unloading batch to buffer")
            outputString = "Started unloading Batch " + str(newAction.getBatch().getId()) + " from task " + newAction.getTask().getName()
            self.logger.logEvent(outputString)
            newAction.setStatus(True)
        return 0
    
    def run(self):
        # self.startProductionLine()
        # self.batches = self.createBatches(self.productionGoal)
        # self.createLoadToInputBufferAction()

        while not self.isFinished():
            try:
                sys.stdout.write("--Time: " + str(self.time) + "--\n")
                
                # #Check if ongoing actions is finished, and/or create new actions
                self.updateState()
                
                # #Check for new action to be executed
                self.executeNewActions()


                #Check if production is valid
                self.checkIfProductionIsValid()

                # Load new batch into inputbuffer
                self.createLoadToInputBufferAction()

                # Update time
                self.updateTime()
            except ValueError as e:
                # print(e)
                break
            

        self.logger.saveToFile()

    # def executeAction(self, action):
    #     if action.name == "Load batch to 'Input buffer'":
    #         inputbuffer = self.productionline.getBuffer("Input buffer")
    #         # inputbuffer.addBatch(action.batch)
    #         action.status = True
    #         action.startTime = self.time
    #         action.finishTime = self.time + round(Decimal(1),1)
    #         outputString = "Batch " + str(action.batch.id) + " added to inputbuffer"
    #         # sys.stdout.write(outputString+"\n")
    #         self.logger.logEvent(outputString)
    #     elif action.name == "Load batch from buffer to task":
    #         action.status = True
    #         batch = action.batch
    #         buffer = self.productionline.findBatch(batch)
    #         task = buffer.getNextTask()
    #         finishTime = task.startProduction(batch, self.time)
    #         action.startTime = self.time
    #         action.finishTime = finishTime+round(Decimal(1),1)
    #         buffer.removeBatch(batch)
    #         # sys.stdout.write("Batch " + str(action.batch.id) + " added to " + str(task.name) + "\n")
    #         self.logger.logEvent("Batch " + str(action.batch.id) + " added to " + str(task.name))
    #     elif action.name == "Load batch from task to buffer":
    #         action.status = True
    #         batch = action.batch
    #         task = self.productionline.findBatch(batch)
    #         buffer = task.getOutputBuffer()
    #         buffer.addBatch(batch)
    #         task.endProduction()
    #         action.startTime = self.time
    #         action.finishTime = self.time + round(Decimal(1),1)
    #         # sys.stdout.write("Batch " + str(action.batch.id) + " added to " + str(buffer.name) + "\n")
    #         self.logger.logEvent("Batch " + str(action.batch.id) + " added to " + str(buffer.name))
    
    # def loadNewBatchIntoInputBuffer(self):
    #     for action in self.scheduler.actions:
    #         if action.name == "Load batch to 'Input buffer'":
    #             if action.status == False:
    #                 if self._canActionBeExecuted(action):
    #                     self.executeAction(action)
    #                     break

    # def startProductionLine(self):
    #     #Check if productionGoal is too low
    #     if self.productionGoal <20:
    #         raise ValueError("Production goal must be more than 20")
    #     batches = self.createBatches(self.productionGoal)
    #     #Create actions for loading batches into inputbuffer
    #     inputbuffer = self.productionline.getBuffer("Input buffer")
    #     for batch in batches:
    #         processingtime = 1 #1 minute
    #         inputBuffer = self.productionline.getBuffer("Input buffer")
    #         action = Action("Load batch to 'Input buffer'", batch, inputBuffer)
    #         # action.createPrecedingActions()
    #         # action.createPrecedingActions5()
    #         self.scheduler.addAction(action)

    # def updateActions(self):
    #     oldActions = copy.copy(self.scheduler.actions)
    #     newActions = []
        
    #     for action in self.scheduler.actions:
    #         #Initial state
    #         if action.status == False:
    #             pass
    #         if action.status == True:
    #             if action.finishTime == self.time:
    #                 self.finishAction(action)
    #                 nextAction = action.getNextAction()
    #                 oldActions.remove(action)
    #                 if nextAction != None:
    #                     newActions.append(nextAction)
    #     self.scheduler.actions = oldActions + newActions


    # def executeNewActions(self):
    #     if len(self.scheduler.actions) == 0:
    #         return
    #     for action in self.scheduler.actions:
    #         if action.status == False:
    #             #Check if action can be executed
    #             if self._canActionBeExecuted(action):
    #                 self.executeAction(action)


if __name__ == "__main__":
    sys.stdout.write("Starting simulation...\n")
    productionGoal = 20
    tasksInUnits = [[1,3,6,9],[2,5,7],[4,8]]
    heuristics = [[1,3,6,9],[2,5,7],[4,8]]
    loadToInputBufferInterval = 654
    groupingOfBatches = None #TODO: Implement grouping of batches
    SIM = Simulator(productionGoal,tasksInUnits, heuristics, loadToInputBufferInterval, groupingOfBatches)
    P = SIM.printer
    SC = SIM.scheduler
    PL = SIM.productionline

    SIM.run()
    P.getStatus()
