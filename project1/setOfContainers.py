#Task 2

class setOfContainers:
    #Initializes the set of containers
    def __init__(self, containerList):
        self.containerList = containerList

    #Get list of containers
    def getContainerList(self):
        return self.containerList

    #Set list of containers
    def setContainerList(self, containerList):
        self.containerList = containerList
    
    #Add container to list of containers
    def addContainer(self, container):
        self.containerList.append(container)
    
    #Add list of containers to list of containers
    def addListOfContainers(self, containerList):
        for container in containerList:
            self.containerList.append(container)

    #Remove container from list of containers
    def removeContainer(self, container):
        self.containerList.remove(container)

    #Get container by id
    def getContainerById(self, idNr):
        for container in self.containerList:
            if container.getidNr() == idNr:
                return container
        return None
    
    #Get container by index
    def getContainerByIndex(self, index):
        print(index)
        return self.containerList[index]
    
    #Get string representation of set of containers
    def __str__(self):
        returnValue = "Containers in set:" + "\n" + "----------------------" + "\n"
        for container in self.containerList:
            returnValue += "Container id: " + str(container.getidNr())+"\n"
        return returnValue