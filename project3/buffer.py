


class Buffer:

    def __init__(self, name, maxCapacity):
        self.name = name
        self.batches = []
        self.maxCapacity = maxCapacity
        self.currentLoad = 0
        self.previousTask = None
        self.nextTask = None

        
    
    def getName(self):
        return self.name

    def getNextTask(self):
        return self.nextTask
    
    def setNextTask(self, task):
        self.nextTask = task

    def setPreviousTask(self, task):
        self.previousTask = task

    # def getMaxCapacity(self):
    #     return self.maxCapacity
    
    # def is_empty(self):
    #     return len(self.batches) == 0
    
    def getBatches(self):
        return self.batches
    
    # def setBatches(self, batches):
    #     self.batches = batches
    
    # def add(self, batch, completionTime):
    #     load = batch.getNumWafers()
    #     self.batches.append([batch, completionTime])
    #     self.currentLoad += load
    
    def removeBatch(self, batch):
        for b in self.batches:
            if b == batch:
                self.currentLoad -= batch.getNumWafers()
                self.batches.remove(b)

    def addBatch(self, batch):
        self.batches.append(batch)
        self.currentLoad += batch.getNumWafers()


    def isFull(self):
        totWafers = 0
        for batch in self.batches:
            totWafers += batch.getNumWafers()
        if totWafers >= self.maxCapacity:
            return True
        else:
            return False

    def canAcceptBatch(self, batch):
        #Get total number of wafers in buffer
        totWafers = 0
        for b in self.batches:
            totWafers += b.getNumWafers()

        #Check if buffer can accept batch
        if totWafers + batch.getNumWafers() <= self.maxCapacity:
            return True
        else:
            return False
        