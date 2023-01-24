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
        d = []
        for i in range(self.height):
            d.append([])
            for j in range(self.length):
                d[i].append([])
                for k in range(self.width):
                    d[i][j].append(0)
        self.decks = d


    #Add a container to the ship
    def addContainer(self, container):
        if container in self.containers:
            print("Container already in ship")
            return False
        self.containers.append(container)
        position = self._findPlacement(container)
        if position == False:
            print("No suitable placement found")
            return False
        for pos in position:
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
        if container.length == 20:
            for i in range(self.height):
                #Current deck
                deck = self.decks[i]
                for j in range(self.length):
                    #Current row
                    row = deck[j]
                    for k in range(self.width):
                        #Current position
                        position = row[k]
                        if(position == 0 and self._occupiedUnder((i, j, k))):
                            return (i, j, k),
        elif container.length == 40:
            for i in range(self.height):
                #Current deck
                deck = self.decks[i]
                #check if there is space forwards
                for j in range (self.length-1):
                    #Current row
                    row1 = deck[j]
                    row2 = deck[j+1]
                    for k in range(self.width):
                        #Current position
                        position1 = row1[k]
                        position2 = row2[k]
                        if(position1 == 0 and position2 == 0 and self._occupiedUnder((i,j,k)) and self._occupiedUnder((i,j,k))):
                            return (i, j, k),(i, j+1, k)
                
                #check if there is space sideways
                for j in range(self.length):
                    #Current row
                    row = deck[j]
                    for k in range(self.width-1):
                        #Current position
                        position1 = row[k]
                        position2 = row[k+1]
                        if(position1 == 0 and position2 == 0 and self._occupiedUnder((i,j,k)) and self._occupiedUnder((i,j,k))):
                            return (i, j, k),(i, j, k+1)
        return False


    #checks if position under given position is occupied by a container
    def _occupiedUnder(self, position):
        if position[0] == 0: #position is at bottom deck
            return True
        if self.decks[position[0]-1][position[1]][position[2]] != 0: #position under is occupied 
            return True
        return False #position under is empty
    
    
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
        limit = len(containers)*len(containers)
        while unloadedContainers != [] or i == limit:
            if self.addContainer(unloadedContainers[0]):
                unloadedContainers.remove(unloadedContainers[0])
            else:
                container = unloadedContainers[0]
                unloadedContainers.remove(container)
                unloadedContainers.append(container)
            # for container in unloadedContainers:
            #     if self.addContainer(container):
            #         loadedContainers.append(container)
            #         unloadedContainers.remove(container)
            #     else:
            #         unloadedContainers.remove(container)
            #         unloadedContainers.append(container)
            i+=1
            print(i)
        return "Ship loaded"
        



if __name__ == "__main__":
    s = Ship(5, 3, 4)
    s.createDecks()

    container1 = Container(40, 2000)
    container2 = Container(20, 4356)
    container3 = Container(20, 56453)
    container4 = Container(40, 64536)
    container5 = Container(20, 6435)
    container6 = Container(40, 1645000)
    container7 = Container(20, 643)
    container8 = Container(40, 345)
    container9 = Container(20, 65433)
    container10 = Container(20, 643)

    containers = [container1, container2, container3, container4, container5, container6, container7, container8, container9, container10]
    s.loadShip(containers)
    print(s.getLoad())



    
