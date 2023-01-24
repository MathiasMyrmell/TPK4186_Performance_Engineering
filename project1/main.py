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
    s = Ship(4, 3, 3)
    s.createDecks()

    c1 = Container(40, 1)
    c2 = Container(40, 2)
    c3 = Container(40, 3)
    c4 = Container(40, 4)
    c5 = Container(40, 5)
    c6 = Container(40, 6)
    liste1 = [c1, c2, c3, c4, c5, c6]
    setOfContainers = setContainers(liste1)
    s.loadShip(setOfContainers.getContainerList())
    print(s.getLoad())
    print("------------------------------")
    c7 = Container(40, 7)
    c8 = Container(40, 8)
    c9 = Container(40, 9)
    c10 = Container(40, 10)
    c11 = Container(40, 11)
    c12 = Container(20, 12)
    c13 = Container(40, 13)
    c14 = Container(40, 14)
    c15 = Container(40, 15)
    c16 = Container(40, 16)
    c17 = Container(40, 17)
    c18 = Container(40, 18)
    c19 = Container(40, 19)
    c20 = Container(40, 20)
    c21 = Container(40, 21)
    c22 = Container(40, 22)
    c23 = Container(20, 23)

    liste2 = [c7, c8, c9, c10, c11, c12, c13, c14, c15, c16, c17, c18]
    setOfContainers = setContainers(liste2)
    s.loadShip(setOfContainers.getContainerList())
    print(s.getLoad())
    # print(setOfContainers.getContainerList())
    # #load ship
    # s.loadShip(setOfContainers.getContainerList())
    # print(s.getLoad())