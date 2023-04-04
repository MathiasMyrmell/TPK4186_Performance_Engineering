
from productionline import Productionline
from batch import Batch

import sys
from decimal import *
import copy

class Printer:
    def __init__(self, simulator):
        self.simulator = simulator


    def getStatus(self):
        buffers = self.simulator.productionline.getBuffers()
        tasks = self.simulator.productionline.getTasks()
        returnValue = "\n"
        for buffer in buffers:
            returnValue += buffer.getName() + ": " + str(buffer.currentLoad) + " wafers\n"
        for task in tasks:
            returnValue += task.getName() + ": " +"Production? " +str(task.getInProduction())+"\n"
        sys.stdout.write(returnValue)


class Action:
        
        def __init__(self, name, batch):
            self.name = name
            self.precedingActions = []
            #Current status
            self.status =False
            self.batch = batch
            self.startTime = 0
            self.finishTime = float("inf")


        def createPrecedingActions(self):
            preceidingActions = []
            preceidingActions.append(Action("Load batch from buffer to task",self.batch))
            preceidingActions.append(Action("Load batch from task to buffer",self.batch))
            preceidingActions.append(Action("Load batch from buffer to task",self.batch))
            preceidingActions.append(Action("Load batch from task to buffer",self.batch))
            preceidingActions.append(Action("Load batch from buffer to task",self.batch))
            preceidingActions.append(Action("Load batch from task to buffer",self.batch))
            preceidingActions.append(Action("Load batch from buffer to task",self.batch))
            preceidingActions.append(Action("Load batch from task to buffer",self.batch))
            preceidingActions.append(Action("Load batch from buffer to task",self.batch))
            preceidingActions.append(Action("Load batch from task to buffer",self.batch))
            preceidingActions.append(Action("Load batch from buffer to task",self.batch))
            preceidingActions.append(Action("Load batch from task to buffer",self.batch))
            preceidingActions.append(Action("Load batch from buffer to task",self.batch))
            preceidingActions.append(Action("Load batch from task to buffer",self.batch))
            preceidingActions.append(Action("Load batch from buffer to task",self.batch))
            preceidingActions.append(Action("Load batch from task to buffer",self.batch))
            preceidingActions.append(Action("Load batch from buffer to task",self.batch))
            preceidingActions.append(Action("Load batch from task to buffer",self.batch))

            self.precedingActions = preceidingActions


        def getNextAction(self):
            if(len(self.precedingActions) == 0):
                return None
            action = self.precedingActions.pop(0)
            action.precedingActions = self.precedingActions
            return action
        

class Scheduler:
    
    def __init__(self):
        self.actions = []

    def addAction(self, action):
        self.actions.append(action)

    def removeAction(self, action):
        self.actions.remove(action)

    


class Simulator:

    def __init__(self, productionGoal):
        self.productionGoal = productionGoal
        self.scheduler = Scheduler()
        self.productionline = Productionline()
        self.time = round(Decimal(0),1)
        self.batches = []
    
    def _createBatches(self, numWafers):
        batches = []
        while(numWafers > 0):
            if(numWafers//50==0):
                batches.append(Batch(numWafers))
                numWafers = 0
            elif(numWafers//50 > 1):
                batches.append(Batch(50))
                numWafers -= 50
            elif(numWafers%50 == 0):
                batches.append(Batch(50))
                numWafers -= 50
            else:
                if(numWafers%50 < 20):
                    num = int(numWafers/2)
                    batches.append(Batch(num))
                    numWafers -= num
                else:
                    batches.append(Batch(50))
                    numWafers -= 50
        return batches
    


    def startProductionLine(self):
        #Check if productionGoal is too low
        if productionGoal <20:
            raise ValueError("Production goal must be more than 20")
        batches = self._createBatches(productionGoal)
        #Create actions for loading batches into inputbuffer
        inputbuffer = self.productionline.getBuffer("Input buffer")
        for batch in batches:
            processingtime = 1 #1 minute
            action = Action("Load batch to 'Input buffer'", batch)
            action.createPrecedingActions()
            self.scheduler.addAction(action)


    def updateActions(self):
        oldActions = copy.copy(self.scheduler.actions)
        newActions = []
        
        for action in self.scheduler.actions:
            #Initial state
            if action.status == False:
                pass
            if action.status == True:
                if action.finishTime == self.time:
                    nextAction = action.getNextAction()
                    oldActions.remove(action)
                    if nextAction != None:
                        newActions.append(nextAction)
        self.scheduler.actions = oldActions + newActions

    def executeNewActions(self):
        if len(self.scheduler.actions) == 0:
            return
        for action in self.scheduler.actions:
            if action.status == False:
                #Check if action can be executed
                if self._canActionBeExecuted(action):
                    self.executeAction(action)


    def _canActionBeExecuted(self,action):
        if action.name == "Load batch to 'Input buffer'":
            #Check if inputbuffer has space
            inputbuffer = self.productionline.getBuffer("Input buffer")
            if inputbuffer.maxCapacity-inputbuffer.currentLoad >= action.batch.numWafers:
                return True
        elif action.name == "Load batch from buffer to task":
            batch = action.batch
            buffer = self.productionline.findBatch(batch)
            if buffer == None:
                return False
            elif buffer.getNextTask().canAcceptBatch(batch):
                return True

        elif action.name == "Load batch from task to buffer":
            batch = action.batch
            task = self.productionline.findBatch(batch)
            if task != None:
                return True

        
        return False
   
    def executeAction(self, action):
        if action.name == "Load batch to 'Input buffer'":
            inputbuffer = self.productionline.getBuffer("Input buffer")
            inputbuffer.addBatch(action.batch)
            action.status = True
            action.startTime = self.time
            action.finishTime = self.time + round(Decimal(1),1)
            sys.stdout.write("Batch " + str(action.batch.numWafers) + " added to inputbuffer\n")
        elif action.name == "Load batch from buffer to task":
            action.status = True
            batch = action.batch
            buffer = self.productionline.findBatch(batch)
            task = buffer.getNextTask()
            finishTime = task.startProduction(batch, self.time)
            action.startTime = self.time
            action.finishTime = finishTime+round(Decimal(1),1)
            buffer.removeBatch(batch)
            sys.stdout.write("Batch " + str(action.batch.numWafers) + " added to " + str(task.name) + "\n")
        elif action.name == "Load batch from task to buffer":
            action.status = True
            batch = action.batch
            task = self.productionline.findBatch(batch)
            buffer = task.getNextBuffer()
            buffer.addBatch(batch)
            task.endProduction()
            action.startTime = self.time
            action.finishTime = self.time + round(Decimal(1),1)
            sys.stdout.write("Batch " + str(action.batch.numWafers) + " added to " + str(buffer.name) + "\n")
        
    def isFinished(self):
        if len(self.scheduler.actions) == 0:
            return True
        return False

    def run(self):
        self.startProductionLine()
        while not self.isFinished():
            sys.stdout.write("--Time: " + str(self.time) + "--\n")
            #Check if ongoing actions is finished
            self.updateActions()
            
            #Check for new action to be executed
            self.executeNewActions()

            self.time = round(self.time+Decimal(0.1),1)

if __name__ == "__main__":
    productionGoal = 20
    SIM = Simulator(productionGoal)
    P = Printer(SIM)
    SC = SIM.scheduler
    PL = SIM.productionline

    SIM.run()
    P.getStatus()








    # # #Simulate
    # #Creating initial actions
    # SIM.startProductionLine()
    
    # # #Start simloop
    # # Time 0
    # sys.stdout.write("--Time: " + str(SIM.time) + "--\n")
    # #Check if ongoing actions is finished
    # SIM.updateActions()
    
    # #Check for new action to be executed
    # SIM.executeNewActions()

   



    # # Time 1
    # SIM.time = round(Decimal(1.0),1)
    # sys.stdout.write("--Time: " + str(SIM.time) + "--\n")
    # SIM.updateActions()
    # SIM.executeNewActions()

    # # Time 12
    # SIM.time = round(Decimal(12.0),1)
    # sys.stdout.write("--Time: " + str(SIM.time) + "--\n")
    # SIM.updateActions()
    # SIM.executeNewActions()


    # # Time 13
    # SIM.time = round(Decimal(13.0),1)
    # sys.stdout.write("--Time: " + str(SIM.time) + "--\n")
    # SIM.updateActions()
    # SIM.executeNewActions()

    # # Time 83
    
    # SIM.time = round(Decimal(84.0),1)
    # sys.stdout.write("\n--Time: " + str(SIM.time) + "--\n")
    # SIM.updateActions()
    # SIM.executeNewActions()

    # # Time 85
    # SIM.time = round(Decimal(85.0),1)
    # sys.stdout.write("--Time: " + str(SIM.time) + "--\n")
    # SIM.updateActions()
    # SIM.executeNewActions()

    # # Time 110
    # SIM.time = round(Decimal(110.0),1)
    # sys.stdout.write("--Time: " + str(SIM.time) + "--\n")
    # SIM.updateActions()
    # SIM.executeNewActions()

    # # Time 111
    # SIM.time = round(Decimal(111.0),1)
    # sys.stdout.write("--Time: " + str(SIM.time) + "--\n")
    # SIM.updateActions()
    # SIM.executeNewActions()

    # # Time 172
    # SIM.time = round(Decimal(172.0),1)
    # sys.stdout.write("--Time: " + str(SIM.time) + "--\n")
    # SIM.updateActions()
    # SIM.executeNewActions()

    # # Time 173
    # SIM.time = round(Decimal(173.0),1)
    # sys.stdout.write("--Time: " + str(SIM.time) + "--\n")
    # SIM.updateActions()
    # SIM.executeNewActions()

    # # Time 190
    # SIM.time = round(Decimal(190.0),1)
    # sys.stdout.write("--Time: " + str(SIM.time) + "--\n")
    # SIM.updateActions()
    # SIM.executeNewActions()

    # # Time 191
    # SIM.time = round(Decimal(191.0),1)
    # sys.stdout.write("--Time: " + str(SIM.time) + "--\n")
    # SIM.updateActions()
    # SIM.executeNewActions()
    
    # # Time 202
    # SIM.time = round(Decimal(202.0),1)
    # sys.stdout.write("--Time: " + str(SIM.time) + "--\n")
    # SIM.updateActions()
    # SIM.executeNewActions()

    # # Time 203
    # SIM.time = round(Decimal(203.0),1)
    # sys.stdout.write("--Time: " + str(SIM.time) + "--\n")
    # SIM.updateActions()
    # SIM.executeNewActions()

    # # time 224
    # SIM.time = round(Decimal(224.0),1)
    # sys.stdout.write("--Time: " + str(SIM.time) + "--\n")
    # SIM.updateActions()
    # SIM.executeNewActions()

    # # time 225
    # SIM.time = round(Decimal(225.0),1)
    # sys.stdout.write("--Time: " + str(SIM.time) + "--\n")
    # SIM.updateActions()
    # SIM.executeNewActions()

    # # Time 264
    # SIM.time = round(Decimal(264.0),1)
    # sys.stdout.write("--Time: " + str(SIM.time) + "--\n")
    # SIM.updateActions()
    # SIM.executeNewActions()

    # # Time 265
    # SIM.time = round(Decimal(265.0),1)
    # sys.stdout.write("--Time: " + str(SIM.time) + "--\n")
    # SIM.updateActions()
    # SIM.executeNewActions()

    # # Time 272
    # SIM.time = round(Decimal(272.0),1)
    # sys.stdout.write("--Time: " + str(SIM.time) + "--\n")
    # SIM.updateActions()
    # SIM.executeNewActions()
    # print("Finished: ",SIM.isFinished())

    # # Time 273
    # SIM.time = round(Decimal(273.0),1)
    # sys.stdout.write("--Time: " + str(SIM.time) + "--\n")
    # SIM.updateActions()
    # SIM.executeNewActions()
    # print("Finished: ",SIM.isFinished())



    # # print(SC.actions[0].finishTime)

    # P.getStatus()

    # # action = SC.actions[0]
    # # print("Current action:",action.name)
    # # for a in action.precedingActions:
    # #     print(a.name)

