## Project 1
## Mathias Myrmell Moen
## Group 7

from container import Container
from setOfContainers import setOfContainers
from ships import Ship
from dock import Dock
import random
import copy

identificationNumbers = []

#Get unique identification number
def getNewIdentificationNumber():
    identificationNumber = random.randint(1, 10000000)
    if(identificationNumber in identificationNumbers):
        getNewIdentificationNumber()
    else:
        identificationNumbers.append(identificationNumber)
        return identificationNumber

#Create container with fixed length and cargo weight
def createContainer(idNr, length, cargoWeight):
    container = Container(length, idNr)
    container.setCargoWeight(cargoWeight)
    return container

#Task 3
#Create random container with random length and cargo weight
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

#Create set of random containers
def createSetOfContainers(numberOfContainers):
    containerList = []
    for i in range(numberOfContainers):
        containerList.append(createRandomContainer())
    return setOfContainers(containerList)

#Task 4

#Save a set of containers to a file
def saveContainersToFile(containers):
    try:
        file = open("project1/datafiles/data.csv", "r")
        file.close()
    except:
        print("could not read file")
    try:
        file = open("project1/datafiles/data.csv", "a")
        for container in containers:
            data = container.getFileFormat()
            file.write(data)
        file.flush()
        file.close()
    except:
        print("could not append to file")
    return 0

#Load a set of containers from a file
def loadContainersFromFile():
    listOfContainers = []
    try:
        file = open("project1/datafiles/data.csv", "r")
        
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


# Task 6
#Save current load to file
def saveLoadToFile(ship):
    if(ship.getDecks() == None):
        print("No load to save")
        return None
    containers = ship.getContainers()
    try:
        file = open("project1/datafiles/load.csv", "r")
        file.close()
    except:
        print("could not read file")
    try:
        file = open("project1/datafiles/load.csv", "a")
        for container in containers:
            data = container.getFileFormat()
            file.write(data)
        file.flush()
        file.close()
    except:
        print("could not append to file")

#Read load from file
def getLoadFromFile(ship):
    listOfContainers = []
    try:
        file = open("project1/datafiles/load.csv", "r")
        
        for line in file:
            data = line.split(",")
            idNr = int(data[0])
            length = int(data[1])
            # startWeigth = int(data[2])
            # maxWeigth = int(data[3])
            cargoWeight = int(data[4])
            # totalWeight = int(data[5])
            container = Container(length, idNr)
            container.setCargoWeight(cargoWeight)
            if((container in ship.getContainers()) == False):
                listOfContainers.append(container)
        file.close()
    except:
        print("could not read file")
    
    return listOfContainers   


if __name__ == "__main__":
    # 2.1 Containers
    # Task 1
    print("------Task 1-------")
    c1 = Container(40, getNewIdentificationNumber()) #Create container with length 40 and random idNr
    c2 = Container(20, getNewIdentificationNumber()) #Create container with length 20 and random idNr
    print("Container id: ", c1.getidNr())

    #Task 2
    print("\n"+"------Task 2-------")
    setContainer = createSetOfContainers(5) #Create set with 5 containers
    print(setContainer)
    setContainer.removeContainer(setContainer.getContainerByIndex(0)) #Remove first container in set
    print("Removed first container in set")
    print(setContainer)
    #Task 3
    print("\n"+"------Task 3-------")
    print("Create random container")
    print(createRandomContainer())
    print("Create set of random containers")
    print(createSetOfContainers(5))

    #Task 4
    print("\n"+"------Task 4-------")
    saveContainersToFile(setContainer.getContainerList())
    print("Saved set of containers to file: data.csv")
    print("Loaded set of containers from file: data.csv")
    setContainers2 = createSetOfContainers(0)
    setContainers2.setContainerList(loadContainersFromFile())
    print(setContainers2)


    # 2.2 Ships
    #Task 5
    print("\n"+"------Task 5-------")
    length = 1 #USER INPUT
    width = 1 #USER INPUT
    height = 1 #USER INPUT

    ship = Ship(length, width, height) #Create ship 
    print("The empty ship will look like this:")
    print(ship.getDecks())
    print("finding suitablke bay for container...")
    print(ship._findPlacement(c1))
    print("Loading a container to the ship...")
    ship.addContainer(c1)
    ship.addContainer(c2)
    print("The ship will then look like this:")
    print(ship.getDecks())
    print("Removing container...")
    ship.removeContainer(c1)
    print("The ship will then look like this:")
    print(ship.getDecks())

    #Task 6
    print("\n"+"------Task 6-------")
    print("Saving load to file: load.csv")
    saveLoadToFile(ship)
    print("Loading load from file: load.csv")
    load = getLoadFromFile(ship)
    print("Load:", load)


    #Task 7
    print("\n"+"------Task 7-------")
    setContainers3 = createSetOfContainers(length*width*height) 
    print("Loading set of containers to ship...")
    loadedShip = ship.loadShip(setContainers3) 
    print("Loaded containers:", len(loadedShip[0]))
    print("Unloaded containers:", len(loadedShip[1]))
    print("Ship will look like this:")
    print(ship.getDecks())
    print("Unloading ship...")
    ship.unloadShip()
    print("Ship will look like this:")
    print(ship.getDecks())

    #Task 8
    print("\n"+"------Task 8-------")
    print("Loading ship by weight...")
    setContainers4 = createSetOfContainers(length*width*height)# if big number, this will take some time. Un-comment line 223 in ships.py if you want to keep progress
    loadedShipByWeight = ship.loadShipByWeight(setContainers4)
    print("Loaded containers:", len(loadedShipByWeight[0]))
    print("Unloaded containers:", len(loadedShipByWeight[1]))
    print("Ship will look like this:")
    print(ship.getDecks())

    #Task 9
    print("\n"+"------Task 9-------")
    print("Stability of ship")
    stability = ship.stability()
    print("Vertical stability: ", stability[0])
    print("Horizontal stability: ", stability[1])
    print("Alongside stability: ", stability[2])

    #Task 10
    print("\n"+"------Task 10-------")
    print("Was not able to fully complete this task, so it was not included in the final report")

    #2.3 Docks
    #Task 11
    print("\n"+"------Task 11-------")
    dock = Dock()
    ship2 = Ship(4,4,4)
    ship2.getDecks()
    setContainers6 = createSetOfContainers(20)
    ship2.loadShipByWeight(copy.copy(setContainers6))
    print("Docking ship...")
    dock.dockShip(ship2)
    print("Ship is docked")

    print("Unloading ship with one crane...")
    unload = dock.unloadShip(1)
    print("It took ",unload[0]," minutes to unload the ship with ",unload[1]," cranes")
    print("Ship is unloaded")

    setContainers7 = createSetOfContainers(20)
    ship2.loadShipByWeight(setContainers7)

    print("Unloading ship with 4 cranes...")
    unload4 = dock.unloadShip(4)
    print("It took ",unload4[0]," minutes to unload the ship with ",unload4[1]," cranes")
    print("Ship is unloaded")

    print("Undocking ship...")
    dock.undockShip()
    print("Ship is undocked")
    print(ship2.getDecks())    