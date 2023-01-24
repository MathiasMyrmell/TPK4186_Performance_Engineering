from container import Container, setContainers
from ships import Ship
import random

identificationNumbers = []

def getNewIdentificationNumber():
    identificationNumber = random.randint(1, 10000000)
    if(identificationNumber in identificationNumbers):
        getNewIdentificationNumber()
    else:
        identificationNumbers.append(identificationNumber)
        return identificationNumber

def createContainer(idNr, length, cargoWeight):
    container = Container(length, idNr)
    container.setCargoWeight(cargoWeight)
    return container

def createRandomContainer():
    cargoWeight = 0
    containerLength = random.choice([20, 40])
    if(containerLength == 20):
        cargoWeight = random.randint(1, 20000)
        
    elif(containerLength == 40):
        cargoWeight = random.randint(1, 22000)
    container = Container(containerLength, getNewIdentificationNumber())
    container.setCargoWeight(cargoWeight)
    return container

def createSetOfContainers(numberOfContainers):
    containerList = []
    for i in range(numberOfContainers):
        containerList.append(createRandomContainer())
    return setContainers(containerList)

def readFromFile():
    listOfContainers = []
    try:
        file = open("project1/data.csv", "r")
        
        for line in file:
            data = line.split(",")
            length = int(data[1])
            idNr = int(data[0])
            cargoWeight = int(data[4])
            container = createContainer(idNr, length, cargoWeight)
            listOfContainers.append(container)
        file.close()
    except:
        print("could not read file")
    
    return listOfContainers   

def writeToFile(container):
    try:
        file = open("project1/data.csv", "r")
        file.close()
    except:
        print("could not read file")
    try:
        file = open("project1/data.csv", "a")
        data = container.fileFormat()
        file.write(data)
        file.flush()
        file.close()
    except:
        print("could not append to file")
    return 0



if __name__ == "__main__":
    # #Test container.py
    # #random container
    # container = createRandomContainer()
    # #create multiple containers
    # setOfContainers = createSetOfContainers(3)
    # print(container)
    # #write to file
    # writeToFile(container)
    # #read from file
    # containers = readFromFile()
    # for container in containers:
    #     print(container)

    # #Test ship.py
    # #create ship
    s = Ship(23, 22, 18)
    s.createDecks()
    # #create multiple containers
    setOfContainers = createSetOfContainers(9109)
    # for container in setOfContainers.getContainerList():
    #     print(container)
    # print(setOfContainers.getContainerList())
    # #load ship
    s.loadShip(setOfContainers.getContainerList())
    print(s.getLoad())