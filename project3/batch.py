


class Batch:

    def __init__(self, id, numWafers):
        if 20 <= numWafers and numWafers <= 50 :
            self.id = id
            self.numWafers = numWafers
        else:
            raise ValueError("Number of wafers must be between 20 and 50")
    
    # #Getters
    # Get batch id
    def getId(self):
        return self.id
    
    # Get number of wafers in batch
    def getNumWafers(self):
        return self.numWafers









    # def isReadyForProduction(self):
    #     return True




    
        
    
    