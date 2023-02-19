import copy

#Task 10 and 11
class Dock:

    def __init__(self):
        self.ship = None
        self.maxCranes = 4

    #Add ship to dock
    def dockShip(self, ship):
        self.ship = ship
    
    #Remove ship from dock
    def undockShip(self):
        self.ship = None

    #Get ship in dock
    def getShip(self):
        return self.ship

    #Unload ship
    def unloadShip(self, nCranes):
        if nCranes > self.maxCranes:
            print("Too many cranes")
            return
        if self.ship == None:
            print("No ship docked")
            return
       
        #Containers in ship
        containers = copy.copy(self.ship.getContainers())
       
        #Divide the decks into nCranes parts
        xValuesPerSection = self._divideDecksIntoSections(nCranes)

        #Start unloading
        iterations = 0
        while len(containers)!=0:
            containersChosenInIteration = []
            #for each crane
            for i in range(nCranes):
                #find container to unload
                container = self._findUnloadableContainer(xValuesPerSection[i], containersChosenInIteration)
                if container != None:
                    containersChosenInIteration.append(container)
            #remove containers from ship
            for c in containersChosenInIteration:
                containers.remove(c)
                self.ship.removeContainer(c)

            #add time to iterations
            iterations += 1

        #Calculate time
        time = self._calculateTime(iterations)

        #Return result
        return time, nCranes

    #Divide ship in sections
    def _divideDecksIntoSections(self, nCranes):
        lShip = self.ship.getLength()
        lPart = lShip / nCranes
        xValuesPerSection = []
        for i in range(1,nCranes+1):
            lowerThreshold = round((i-1)*(lPart))
            upperThreshold = round(i*lPart)-1
            xValuesPerSection.append([lowerThreshold, upperThreshold])
        return xValuesPerSection
    
    #Finds container in section that can be unloaded
    def _findUnloadableContainer(self, xValues, containersChosenInIteration):
        #Decks in ship
        decks = self.ship.getDecks()
        width = self.ship.getWidth()
        for i in range(len(decks)-1, -1, -1):
            for j in range(xValues[0], xValues[1]+1):
                for k in range(width):
                    container = decks[i][j][k]
                    proceed = self._checkIfPossibleToUnloadContainer(container, containersChosenInIteration)
                    containerAbove = self._checkIfThereAreContainerOverContainer(self.ship.findContainer(container))
                    if container == None:
                        return None
                    elif container == 0:
                        continue
                    elif proceed == False:
                        continue
                    elif containerAbove == False:
                        continue
                    else:
                        return container
              
        return None
    
    #Checks if container can be unloaded
    def _checkIfPossibleToUnloadContainer(self, container, containersChosenInIteration):
        #Check if container is already chosen
        for c in containersChosenInIteration:
            if c == container:
                return False

        #Find position of container
        
        positionContainer = self.ship.findContainer(container)
        if positionContainer == None:
            return False
        #Find adjacent bays to container
        positionsOtherContainers = []
        for c in containersChosenInIteration:
            positionsOtherContainers.append(self.ship.findContainer(c))
        
        adjecentBays = []
        
        for p in positionContainer:
            over = (p[0], p[1]+1, p[2])
            under = (p[0], p[1]-1, p[2])
            left = (p[0], p[1], p[2]-1)
            right = (p[0], p[1], p[2]+1)
            
            if over not in positionContainer:
                adjecentBays.append(over)
            if under not in positionContainer:
                adjecentBays.append(under)
            if left not in positionContainer:
                adjecentBays.append(left)
            if right not in positionContainer:
                adjecentBays.append(right)
            
        #Check if container is in adjacent bay to other container
        for p in positionsOtherContainers:
            if p in adjecentBays:
                return False
        
        #Check if container has a container on top of it
        
        return True
     
    #Check if space above container is clear
    def _checkIfThereAreContainerOverContainer(self, positionContainer):
        if positionContainer == None or positionContainer == 0:
            return False
        height = self.ship.getHeight()
        cargo = copy.copy(self.ship.getCargo())
        for pos in positionContainer:
            for i in range(pos[0]+1, height+1):
                if cargo[i][pos[1]][pos[2]] != 0:
                    return False
        return True

    #Calculate unloading time
    def _calculateTime(self, iterations):
        minutesPerIteration = 4
        return iterations * minutesPerIteration

