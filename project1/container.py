#Task 1

class Container:
    length20 = 20
    length40 = 40

    def __init__(self, length, idNr):
        if(length == 20):
            self.idNr = idNr
            self.length = 20
            self.startWeight = 2000
            self.maxCargoWeight = 20000
            self.cargoWeight = 0
            self.totalWeight = self.startWeight + self.cargoWeight
        elif(length == 40):
            self.idNr = idNr
            self.length = 40
            self.startWeight = 4000
            self.maxCargoWeight = 22000
            self.cargoWeight = 0
            self.totalWeight = self.startWeight + self.cargoWeight
        else:
            print("Invalid container length")

    #Get idNr of container
    def getidNr(self):
        return self.idNr

    #Get length of container
    def getLength(self):
        return self.length

    #Get start weight of container
    def getStartWeight(self):
        return self.startWeight

    #Get cargo weight of container
    def getMaxCargoWeight(self):
        return self.maxCargoWeight

    #Get cargo weight of container
    def getCargoWeight(self):
        return self.cargoWeight
    
    #Set cargo weight of container
    def setCargoWeight(self, newCargoWeight):
        self.cargoWeight = newCargoWeight
        self.setTotalWeight()
    
    #Get total weight of container
    def getTotalWeight(self):
        return self.totalWeight

    #Set total weight of container
    def setTotalWeight(self):
        self.totalWeight = self.startWeight + self.cargoWeight
    
    #Get file format of container
    def getFileFormat(self):
        return str(self.idNr)+","+str(self.length)+","+str(self.startWeight)+","+str(self.maxCargoWeight)+","+str(self.cargoWeight)+","+str(self.getTotalWeight())+"\n"
  

    