# Container Ship

# 1. Import Modules
# -----------------

import sys
import random

# 2. Containers
# -------------

class Container:
    def __init__(self, serialNumber, length, weight, cargo):
        self.serialNumber = serialNumber
        self.length = length
        self.weight = weight
        self.cargo = cargo

    def getSerialNumber(self):
        return self.serialNumber
    
    def getLength(self):
        return self.length
    
    def getWeight(self):
        return self.weight
    
    def getCargo(self):
        return self.cargo

    def getTotalWeight(self):
        return self.weight + self.cargo

# 3. Container Piles
# ------------------

class ContainerPileLayer:
    def __init__(self, container):
        self.container1 = container
        self.container2 = None

    def getContainer1(self):
        return self.container1
    
    def setContainer1(self, container):
        self.container1 = container

    def getContainer2(self):
        return self.container2
    
    def setContainer2(self, container):
        self.container2 = container

    def isFull(self):
        return self.container1.getLength()==40 or self.container2!=None

    def getTotalWeight(self):
        if self.container2==None:
            return self.container1.getTotalWeight()
        return self.container1.getTotalWeight() + self.container2.getTotalWeight()

    def canGoOnTop(self, other):
        if self.isFull():
            if other.isFull():
                return self.getTotalWeight() <= other.getTotalWeight()
            return False
        return True

class ContainerPile:
    def __init__(self):
        self.layers = []

    def getLayers(self):
        return self.layers

    def isEmpty(self):
        return len(self.layers)==0
    
    def getHeight(self):
        return len(self.layers)

    def getLayer(self, index):
        if index<0 or index>=self.getHeight():
            return None
        return self.layers[index]

    def pushLayer(self, layer):
        self.layers.append(layer)

    def getTopLayer(self):
        if self.isEmpty():
            return None
        return self.layers[-1]

    def popTopLayer(self):
        if self.isEmpty():
            return
        self.layers.pop()

    def pileContainer(self, container):
        if self.isEmpty():
            layer = ContainerPileLayer(container)
            self.pushLayer(layer)
            return
        topLayer = self.getTopLayer()
        if topLayer.isFull():
            layer = ContainerPileLayer(container)
            self.insertLayer(layer)
            return
        if container.getLength()==40:
            self.popTopLayer()
            layer = ContainerPileLayer(container)
            self.insertLayer(layer)
            self.pushLayer(topLayer)
            return
        self.popTopLayer()
        topLayer.setContainer2(container)
        self.insertLayer(topLayer)

    def insertLayer(self, layer):
        lighterLayers = self.popLighterLayers(layer)
        self.pushLayer(layer)
        self.pushLayers(lighterLayers)

    def popLighterLayers(self, layer):
        lighterLayers = []
        while True:
            if self.isEmpty():
                break
            topLayer = self.getTopLayer()
            if layer.canGoOnTop(topLayer):
                break
            self.popTopLayer()
            lighterLayers.append(topLayer)
        return lighterLayers

    def pushLayers(self, layers):
        layers.reverse()
        for layer in layers:
            self.pushLayer(layer)

# 4. Ships
# --------

# 5. Printer
# ----------

class Printer:

    def printContainerPile(self, pile,  outputFile):
        for index in range(pile.getHeight()-1, -1, -1):
            layer = pile.getLayer(index)
            self.printContainerPileLayer(layer, outputFile)

    def printContainerPileLayer(self, layer, outputFile):
        container1 = layer.getContainer1()
        self.printContainer(container1, outputFile)
        container2 = layer.getContainer2()
        if container2!=None:
            outputFile.write(" ")
            self.printContainer(container2, outputFile)
        outputFile.write(" total weight {0:d}\n".format(layer.getTotalWeight()))

    def printContainer(self, container, outputFile):
        outputFile.write("[{0:d} {1:d}]".format(container.getSerialNumber(), container.getLength()))

# 6. Tester
# ---------

class Tester:
    def __init__(self):
        self.serialNumber = 0
    
    def createRandomContainerSample(self, size):
        sample = []
        for _ in range(size):
            container = self.createRandomContainer()
            sample.append(container)
        return sample
    
    def createRandomContainer(self):
        length = random.choice([20, 40])
        if length==20:
            weight = 2
            cargo = random.randint(0, 20)
        else:
            weight = 4
            cargo = random.randint(0, 22)
        self.serialNumber += 1
        return Container(self.serialNumber, length, weight, cargo)

# 7. Main
# ---------


printer = Printer()
tester = Tester()
pile = ContainerPile()

containers = tester.createRandomContainerSample(10)
for container in containers:
    pile.pileContainer(container)
 
printer.printContainerPile(pile, sys.stdout)


