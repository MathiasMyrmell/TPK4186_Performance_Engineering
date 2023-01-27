#Task 2

class setOfContainers:
    #Initializes the set of containers
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