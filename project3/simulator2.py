
from scheduler import Scheduler
from productionline import Productionline
from batch import Batch
from action import Action

import sys
from decimal import *


class Simulator:
    def __init__(self, productionGoal):
        self.productionGoal = productionGoal
        self.scheduler = Scheduler()
        self.productionline = Productionline()
        self.time = round(Decimal(0),1)

        self.batches = []
        
    def setTime(self, time):
        self.time = time

    def getTime(self):
        return self.time
    
    def getProductionGoal(self):
        return self.productionGoal

    def isFinished(self):
        return self.productionline.isFinished(self.productionGoal)
    
    def updateTime(self):
        self.time += round(Decimal(0.1),1)


    def startProductionLine(self):
        #Check if productionGoal is too low
        if productionGoal <20:
            raise ValueError("Production goal must be more than 20")
        batches = self._createBatches(productionGoal)
        #Create actions for loading batches into inputbuffer
        inputbuffer = self.productionline.getBuffer("Input buffer")
        for batch in batches:
            processingtime = 1 #1 minute
            action = Action("Load batch to 'Input buffer'", processingtime, batch, inputbuffer, self.productionline.getTask("Task 1"))
            self.scheduler.addAction(action)

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
    


    def run(self):
        #Start the production line
        self.startProductionLine()
        #Run simulation
        i = 0
        while not self.isFinished() and i<273:
            sys.stdout.write("{0:s}\t{1:s}\n".format(str(self.getTime()), "Actions performed"))
            #Check if ongoing actions is finished
            self.scheduler.updateActions(self.getTime())
            
            #Check for new action to be executed
            self.scheduler.executeNewActions(self.getTime())


            # print(self.scheduler.actions)
            # print(self.time)
            self.updateTime()
            
            i+=1


class Printer:
    def __init__(self, simulator):
        self.simulator = simulator


    def getStatus(self):
        buffers = self.simulator.productionline.getBuffers()
        tasks = self.simulator.productionline.getTasks()
        returnValue = ""
        for buffer in buffers:
            returnValue += buffer.getName() + ": " + str(buffer.currentLoad) + " wafers\n"
        for task in tasks:
            returnValue += task.getName() + ": " +"Production? " +str(task.getInProduction())+"\n"
        sys.stdout.write(returnValue)


if __name__ == "__main__":
    productionGoal = 20
    SIM = Simulator(productionGoal)
    pL = SIM.productionline
    sC = SIM.scheduler
    p = Printer(SIM)
    # simulator.run()

    print("Simulator")
    
    #Starting production line
    print("Time: ", SIM.getTime())
    SIM.startProductionLine()
    sC.executeNewActions(SIM.getTime())
    
   
    # Jump to one minute
    SIM.setTime(1)
    print("Time: ", SIM.getTime())
    #Check if ongoing actions is finished
    sC.updateActions(SIM.getTime())
    sC.executeNewActions(SIM.getTime())
    
    #Jump to 12 minutes
    SIM.setTime(round(Decimal(12.0) ,1))
    print("Time: ", SIM.getTime())
    sC.updateActions(SIM.getTime())
    sC.executeNewActions(SIM.getTime())

    p.getStatus()