class Buffer:

    def __init__(self, name, maxCapacity):
        # Initial values
        self.name = name
        self.maxCapacity = maxCapacity
        # Production values
        self.batches = []
        self.currentLoad = 0
        self.previousTask = None
        self.nextTask = None

    # #Getters
    # Returns name of buffer
    def getName(self):
        return self.name
    
    # Returns max capacity of buffer
    def getMaxCapacity(self):
        return self.maxCapacity

    # Return batches in buffer
    def getBatches(self):
        return self.batches
    
    # Returns current load of buffer
    def getCurrentLoad(self):
        return self.currentLoad


    # #Setters
    # Set task that comes after this buffer
    def setNextTask(self, task):
        self.nextTask = task

    # Set task that comes before this buffer
    def setPreviousTask(self, task):
        self.previousTask = task


    # #Functions
    # Add batch to buffer
    def addBatch(self, batch):
        self.batches.append(batch)
        self.currentLoad += batch.getNumWafers()

    # Remove batch from buffer
    # Raise exception if batch not found
    def removeBatch(self, batch):
        for b in self.batches:
            if b == batch:
                self.currentLoad -= batch.getNumWafers()
                self.batches.remove(b)
                return 
        raise Exception("Batch not found in buffer")

    # Check if buffer can accept batch
    # Returns True if buffer can accept batch, False if not
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
    