
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

    def getLength(self):
        return self.length

    def setLength(self, length):
        self.length = length

    def getStartWeight(self):
        return self.startWeight

    def getMaxCargoWeight(self):
        return self.maxCargoWeight

    def getTotalWeight(self):
        return self.totalWeight

    def setCargoWeight(self, newCargoWeight):
        self.newCargoWeight = newCargoWeight
    
    def getidNr(self):
        return self.idNr

    def setidNr(self, idNr):
        self.idNr = idNr

    def __str__(self):
        return "ContainerID:" + str(self.idNr)+"\n"+"-----------------"+"\n"+"Length: "+str(self.length)+"\n"+"Start Weight: "+str(self.startWeight)+"\n"+"Max Cargo Weight: "+str(self.maxCargoWeight)+"\n"+"Cargo Weight: "+str(self.cargoWeight)+"\n"+"Total weight: "+str(self.getTotalWeight())+"\n"+"-----------------"+"\n"
    
    def fileFormat(self):
        return str(self.idNr)+","+str(self.length)+","+str(self.startWeight)+","+str(self.maxCargoWeight)+","+str(self.cargoWeight)+","+str(self.getTotalWeight())+"\n"

class setContainers:

    def __init__(self, containerList):
        self.containerList = containerList

    def getContainerList(self):
        return self.containerList

    def setContainerList(self, containerList):
        self.containerList = containerList
    
    def addContainer(self, container):
        self.containerList.append(container)

    def removeContainer(self, container):
        self.containerList.remove(container)
    
    def getContainer(self, index):
        return self.containerList[index]

    def __str__(self):
        returnValue = "Containers:" + "\n" + "----------------------" + "\n"+ "\n"
        for container in self.containerList:
            returnValue += str(container)+"\n"
        return returnValue
    