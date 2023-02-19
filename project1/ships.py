import copy
from container import Container
from setOfContainers import setOfContainers

#Task 5
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

    def setDecks(self, decks):
        d = [[[None]*self.width]*self.length]
        d+=decks
        self.decks = d

    #Get decks of ship
    def getDecks(self):
        if(self.decks == None):
            self.createDecks()
            
        return self.decks
    
    #Get lenght of ship
    def getLength(self):
        return self.length
    
    #get width of ship
    def getWidth(self):
        return self.width

    #Get height of ship
    def getHeight(self):
        return self.height

    #Add a container to the ship
    def addContainer(self, container):
        if(self.decks == None):
            self.createDecks()
        position = self._findPlacement(container)
        #If no suitable placement is found, return False
        if position == False:
            return False
        #Else, add container to ship
        self.containers.append(container)
        for pos in position:
            self.decks[pos[0]][pos[1]][pos[2]] = container#.idNr
        return True
    
    #Find the position of a given container in the ship
    def findContainer(self, container):
        if(self.decks == None):
            return None
        placement = ()
        for i in range(0,self.height):
            #Current deck
            deck = self.decks[i]
            for j in range(self.length):
                #Current row
                row = deck[j]
                for k in range(self.width):
                    #Current position
                    position = row[k]
                    if position!=0 and position != None:
                        if(position == container):
                            placement += (i, j, k),
        if placement == ():
            return None
        else:
            return placement

    #Return a list of all containers in the ship    
    def getContainers(self):
        if(self.decks == None):
            return None
        return self.containers

    #Return Container based on idNr
    def getContainer(self, idNr):
        if(self.decks == None):
            return None
        for container in self.containers:
            if container.idNr == idNr:
                return container
        return None

    #Remove a container from the ship
    def removeContainer(self, container):
        if(self.decks == None):
            return None
        #If container not in ship
        if (container in self.containers) == False:
            return
        #Else if container in ship
        else:
            self.containers.remove(container)
            position = self.findContainer(container)
            for pos in position:
                self.decks[pos[0]][pos[1]][pos[2]] = 0

    #Return the load of the ship
    def getCargo(self):
        if(self.decks == None):
            return None
        return self.decks
    
    #Return the load of ship, with idNr
    #Only used for testing code
    def getCargoIdNr(self):
        load = copy.copy(self.getCargo())
        for i in range(len(load)):
            for j in range(len(load[i])):
                for k in range(len(load[i][j])):
                    if load[i][j][k] != 0 and load[i][j][k] != None:
                        id = load[i][j][k].idNr
                        load[i][j][k] = id
        return load

    #Find a suitable placement for a given container
    def _findPlacement(self, container, deck = None):
        decks = self.getDecks()
        for i in range(self.height+1):
            if(i == 0):
                continue # Skip first deck
            #Current deck
            deck = decks[i]
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
        #If position is at bottom deck, return True
        if positionUnder == None:
            return True
        #Elif position under is empty, return False
        elif positionUnder == 0:
            return False
        #Elif position under is occupied, return True
        elif positionUnder != 0:
            return True

 
    #Task 7
    #Load ship
    def loadShip(self, c):
        if(self.decks == None):
            return None
        containers = None
        if type(c) == setOfContainers:
            containers = c.getContainerList() 
        else:
            containers = copy.copy(c)
        #List of container that are loaded
        loadedContainers = []
        #List of containers that are not loaded
        unloadedContainers = containers
        i=0
        #Limit to prevent infinite loop
        limit = len(containers)*2

        while len(unloadedContainers)>0 and i<limit:
            #Check if container is already in ship
            for c in self.getContainers():
                if c.idNr == unloadedContainers[0].idNr:
                    unloadedContainers.remove(unloadedContainers[0])
            #If container can be added, add container
            if self.addContainer(unloadedContainers[0]):
                loadedContainers.append(unloadedContainers[0])
                unloadedContainers.remove(unloadedContainers[0])
            #If container can not be added, move container to end of list
            elif self.addContainer(unloadedContainers[0])==False:
                container = unloadedContainers[0]
                unloadedContainers.remove(container)
                unloadedContainers.append(container)
            i+=1
            # print("iteration", i, "of", limit) #uncomment if you want to see how many iterations left
        return loadedContainers, unloadedContainers
    
    #Unload ship
    def unloadShip(self):
        if(self.decks == None):
            return None
        unloadedContainers = []
        load = self.getCargo()
        baseDeck = load[0]
        load.remove(baseDeck) # removing bottom deck
        iteration = 0
        for i in range(self.height-1, -1, -1):
            #Current deck
            currentDeck = load[i]
            emptyDeck = False
            #Find containers in deck
            containers = []
            while not emptyDeck:
                for j in range(self.length):
                    currentRow = currentDeck[j]
                    for k in range(self.width):
                        currentPos = currentRow[k]
                        if currentPos != 0 and currentPos not in containers:
                            containers.append(currentPos)
                emptyDeck = True
            #Remove containers from ship
            for c in containers:
                position = self.findContainer(c)
                for pos in position:
                    self.decks[pos[0]][pos[1]][pos[2]] = 0
                unloadedContainers.append(c)
                
        #Add base deck to load
        load.insert(0, baseDeck)
        return unloadedContainers
    

    #Task 8
    #Load ship based on containers weight
    def loadShipByWeight(self, containers):
        if(self.decks == None):
            return None
        #Sort containers by weight
        sortedContainers = self._sortContainersByWeight(containers)
        #Load ship with sorted containers
        return self.loadShip(sortedContainers)
       
    #Sort containers by weight
    def _sortContainersByWeight(self, c):
        sortedContainers = []
        containers = c.getContainerList()
        stop = False
        while len(containers)>0 or stop:
            heaviest = 0
            for c in containers:
                weight = c.getTotalWeight()
                if weight > heaviest:
                    heaviest = weight
                    heaviestContainer = c
            sortedContainers.append(heaviestContainer)
            containers.remove(heaviestContainer)
            if len(sortedContainers)>self.getLength()*self.getWidth()*self.getHeight():
                stop = True
        return sortedContainers


    #Task 9
    #Calulate total load of ship
    def getTotalLoad(self):
        if(self.decks == None):
            return None
        containers = self.getContainers()
        load = 0
        for container in containers:
            load += container.getTotalWeight()
        return load
    
    #Calculate the weight distribution of the ship
    def weightDistributionSideways(self):
        if(self.decks == None):
            return None
        #Assumption: Containerloads weight are distributed evenly in the container.
        # Therefore if width of ship is odd number, half of weight in container is on starboard and half of weight in container is on portside, for containers in the middle

        #Check if width is even or odd
        evenWidth = None
        if self.width%2 == 0:
            evenWidth = True
        else:
            evenWidth = False
        #Sort containers by port/starboard
        decks = copy.copy(self.getCargo())
        #remove bottom deck
        decks.remove(decks[0])
        portSideDecks = []
        middleSideDeck = []
        starboardDecks = []
        #Sort containers by port/starboard
        for i in range(len(decks)):
            #Decks
            for j in range(len(decks[i])):
                #Rows
                for k in range(len(decks[i][j])):
                    #Positions
                    middleDeckPosition = 0
                    #Set middle deck position based on even or odd width
                    if evenWidth == False:  
                        middleDeckPosition = int(self.width/2)
                    elif evenWidth == True:
                        middleDeckPosition = (self.width/2)-0.5
                    if(k<middleDeckPosition):
                        portSideDecks.append(decks[i][j][k])
                    elif(k>middleDeckPosition):
                        starboardDecks.append(decks[i][j][k])
                    elif(k==middleDeckPosition):
                        middleSideDeck.append(decks[i][j][k])

        #Calculate weight of starboard and portside
        allDecks = [portSideDecks, middleSideDeck, starboardDecks]
        weights = [0, 0, 0]
        for d in allDecks:
            for c in d:
                if c != 0:
                    if c.getLength() == 40:
                        weights[allDecks.index(d)] +=  c.getTotalWeight()/2
                    elif c.getLength() == 20:
                        weights[allDecks.index(d)] += c.getTotalWeight()
        if evenWidth == False:
            weights[0]+=weights[1]/2
            weights[2]+=weights[1]/2

        return weights[0], weights[2]

    #Calculate weight distibution of sections of ship
    def weightDistributionAlongside(self):
        if(self.decks == None):
            return None
        #Assumption: Containerloads weight are distributed evenly in the container.
        # Therefore if length of ship is L%3 = 0, the weight is distributed evenly in the sections
        # If L%3 = 1 or L%3 = 2, the weight row between sections, are distributed evenly between sections
        
        decks = copy.copy(self.getCargo())
        #remove bottom deck
        decks.remove(decks[0])
        #Calculate length of sections
        length = self.length

        #Sort containers by sections
        #[firstSection, firstBorderSection, middleSection, secoundBorderSection, lastSection]
        sections = [[], [], [], [], []]
        
        for i in range(len(decks)):
            for j in range(len(decks[i])):
                if j < int(length/3):
                    sections[0].append(decks[i][j])
                elif j == int(length/3):
                    sections[1].append(decks[i][j])
                elif j<int(2*length/3):
                    sections[2].append(decks[i][j])
                elif j == int(2*length/3):
                    sections[3].append(decks[i][j])
                else:
                    sections[4].append(decks[i][j])
        #Calculate weight of sections
        # [loadFirstSection, loadFirstBorderSection, loadMiddleSection, loadSecoundBorderSection, loadLastSection]
        loads = [0, 0, 0, 0, 0]
        for s in range(len(sections)):
            section = sections[s]
            load = loads[s]
            for i in range(len(section)):
                for j in range(len(section[i])):
                    if(section[i][j] != 0):
                        load += self._getWeightOfBay(section[i][j]) 
            loads[s] = load
        #Calculate weight of sections
        loadSection = [0,0,0]
        if length%3 == 0:
            loadSection[0] = loads[0]
            loadSection[1] = loads[1] + loads[2]
            loadSection[2] = loads[3] + loads[4]
        elif length%3 == 1:
            loadSection[0] = loads[0] + (1/3)*loads[1]
            loadSection[1] = (2/3)*loads[1] + loads[2] + (2/3)*loads[3]
            loadSection[2] = (1/3)*loads[3]+ loads[4]
        else:
            loadSection[0] = loads[0] + (2/3)*loads[1]
            loadSection[1] = (1/3)*loads[1] + loads[2] + (1/3)*loads[3]
            loadSection[2] = (2/3)*loads[3]+ loads[4]
        # return load in stern, middle, bow
        return loadSection[0], loadSection[1], loadSection[2]

    #Calcualte weight distributin in height of ship
    def weightDistributionHeight(self):
        if(self.decks == None):
            return None
        decks = copy.copy(self.getCargo())
        #remove bottom deck
        decks.remove(decks[0])
        decksWeigth = []
        #For each deck
        for i in range(len(decks)):
            deckWeigth = 0
            for length in decks[i]:
                for container in length:
                    if container != 0:
                        deckWeigth += self._getWeightOfBay(container)
            decksWeigth.append(deckWeigth)
        return decksWeigth

    #Calculate weight of bay
    def _getWeightOfBay(self, container):
        weight = 0
        if container.getLength() == 40:
            weight = container.getTotalWeight()/2
        elif container.getLength() == 20:
            weight = container.getTotalWeight()
        return weight

    #Calculate stability of ship
    def stability(self):
        if(self.decks == None):
            return None
        #Vertical stability
        verticalStability = self._verticalStability()

        #Sideways stability
        sidewaysStability = self._sidewaysStability(0.05)
        
        #Alonsgside stability
        alongsideStability = self._alongsideStability(0.05)

        if verticalStability and sidewaysStability and alongsideStability:
            print("The ship is stable")
        else:
            print("The ship is not stable")

        return verticalStability, sidewaysStability, alongsideStability

    #Calculate vertical stability
    def _verticalStability(self):
        #Vertical stability
        deckLoad = self.weightDistributionHeight()
        verticalStability = True
        bottomDeck = deckLoad[0]
        for d in range(len(deckLoad)-1):
            if(deckLoad[d+1]<=bottomDeck):
                verticalStability = True
                bottomDeck = deckLoad[d+1]
            else:
                verticalStability = False
                break
        return verticalStability
    
    #Calculate sideways stability
    def _sidewaysStability(self, factor):
        sidewaysLoad = self.weightDistributionSideways()
        sidewaysStability = False
        weightDifference = abs(sidewaysLoad[0]-sidewaysLoad[1])
        if sidewaysLoad[0]*factor >= weightDifference or sidewaysLoad[1]*factor >= weightDifference:
            sidewaysStability = True
        return sidewaysStability
    
    #Calculate alongside stability
    def _alongsideStability(self, factor):
        alongsideLoad = self.weightDistributionAlongside()
        alongsideStability = False
        heaviestSection = max(alongsideLoad)
        lightestSection = min(alongsideLoad)
        if round(lightestSection*(1+factor),0) >= heaviestSection:
            alongsideStability = True
        
        return alongsideStability