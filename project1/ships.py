from container import Container, setContainers
#Assumptions: containers can't be set vertically
class Ship:

    #Create a ship with a given length, width and height
    def __init__(self, length, width, height):
        self.length = length
        self.width = width
        self.height = height
        self.containers = []
        self.decks = None


    #Create a 3D array of decks, rows and positions
    def createDecks(self):
        d = [[[None]*self.width]*self.length]
        for i in range(self.height):
            deck = []
            for j in range(self.length):
                deck.append([])
                for k in range(self.width):
                    deck[j].append(0)
            d.append(deck)
        self.decks = d


    #Add a container to the ship
    def addContainer(self, container):

        position = self._findPlacement(container)
        if position == False:
            print("No suitable placement found")
            return False #No Suitable Placement Found
        for pos in position:
            self.containers.append(container)
            self.decks[pos[0]][pos[1]][pos[2]] = container.idNr
        return True
    

    #Find the position of a given container in the ship
    def findContainer(self, container):
        placement = ()
        for i in range(self.height):
            #Current deck
            deck = self.decks[i]
            for j in range(self.length):
                #Current row
                row = deck[j]
                for k in range(self.width):
                    #Current position
                    position = row[k]
                    if(position == container.idNr):
                        placement += (i, j, k),
        if placement == ():
            return None
        else:
            return placement


    #Return a list of all containers in the ship    
    def getContainers(self):
        return self.containers


    #Remove a container from the ship
    def removeContainer(self, container):
        if container not in self.containers:
            print("Container not in ship")
            return
        else:
            self.containers.remove(container)
            position = self.findContainer(container)
            for pos in position:
                self.decks[pos[0]][pos[1]][pos[2]] = 0


    #Return the load of the ship
    def getLoad(self):
        return self.decks
    

    #Find a suitable placement for a given container
    def _findPlacement(self, container):
        for i in range(self.height+1):
            if(i == 0):
                continue # Skip first deck
            #Current deck
            deck = self.decks[i]
            if container.length == 20:
                for j in range(self.length):
                    #Current row
                    row = deck[j]
                    for k in range(self.width):
                        #Current position
                        position = row[k]
                        if position == 0 and self._occupiedUnder((i, j, k)):
                            return (i, j, k),
            elif container.length == 40:
                #check if there is space forwards
                for j in range (self.length-1):
                    #Current row
                    row1 = deck[j]
                    row2 = deck[j+1]
                    for k in range(self.width):
                        #Current position
                        position1 = row1[k]
                        position2 = row2[k]
                        if(position1 == 0 and position2 == 0 and self._occupiedUnder((i,j,k)) and self._occupiedUnder((i,j+1,k))):
                            return (i, j, k),(i, j+1, k)            
                #check if there is space sideways
                for j in range(self.length):
                    #Current row
                    row = deck[j]
                    for k in range(self.width-1):
                        #Current position
                        position1 = row[k]
                        position2 = row[k+1]
                        if(position1 == 0 and position2 == 0 and self._occupiedUnder((i,j,k)) and self._occupiedUnder((i,j,k+1))):
                            return (i, j, k),(i, j, k+1)
        return False


    #checks if position under given position is occupied by a container
    def _occupiedUnder(self, position):
        positionUnder = self.decks[position[0]-1][position[1]][position[2]]

        if positionUnder == None: #position is at bottom deck
            # print("bottom deck")
            return True

        elif positionUnder == 0:
            # print(positionUnder)
            # print("position under is empty")
            return False #position under is empty

        elif positionUnder != 0: #position under is occupied 
            # print(positionUnder)
            # print("position under is occupied")
            return True

    
    
    #Save current load to file
    def saveToFile():
       # TODO
       return 0

    #Read load from file
    def readFromFile():
        # TODO
        return 0


    #Task 7
    #Load ship
    def loadShip(self, containers):
        # TODO 
        # fix function
        loadedContainers = []
        unloadedContainers = containers
        i=0
        limit = len(containers)*2
        while len(unloadedContainers)>0 and i<limit:
            for c in self.getContainers():
                if c.idNr == unloadedContainers[0].idNr:
                    print("Container already in ship")
                    unloadedContainers.remove(unloadedContainers[0])
            if self.addContainer(unloadedContainers[0]):
                loadedContainers.append(unloadedContainers[0].idNr)
                unloadedContainers.remove(unloadedContainers[0])
            elif self.addContainer(unloadedContainers[0])==False:
                container = unloadedContainers[0]
                unloadedContainers.remove(container)
                unloadedContainers.append(container)
            i+=1
        return loadedContainers
    
    def unloadShip(self):
        unloadedContainers = []
        load = self.getLoad()
        load.remove(load[0]) # removing bottom deck
        for i in range(self.height-1, -1, -1):
            currentDeck = load[i]
            # print(currentDeck)
            emptyDeck = False
            while not emptyDeck:
                containers = []
                for j in range(self.length):
                    currentRow = currentDeck[j]
                    for k in range(self.width):
                        currentPos = currentRow[k]
                        if currentPos != 0 and currentPos not in containers:
                            containers.append(currentPos)
                
                emptyDeck = True
            print(containers)
            # for j in range(self.length):
            #     currentRow = currentDeck[j]
            #     print(currentRow)
            #     for k in 
        # return unloadedContainers
    #Task 8
    #


if __name__ == "__main__":
    s = Ship(4, 3, 3)
    s.createDecks()
    # print(s.getLoad())

    c1 = Container(40, 1)
    c2 = Container(40, 2)
    c3 = Container(40, 3)
    c4 = Container(40, 4)
    c5 = Container(40, 5)
    c6 = Container(40, 6)
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
    c19 = Container(20, 19)
    liste2 = [c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12, c13, c14, c15, c16, c17, c18, c19]
    setOfContainers = setContainers(liste2)
    s.loadShip(setOfContainers.getContainerList())
    print(s.unloadShip())
    # print(s.getLoad())
    # print("------------------------------")




    
