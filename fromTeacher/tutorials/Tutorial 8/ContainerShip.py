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
        if not other.isFull():
            return False
        return self.getTotalWeight() <= other.getTotalWeight()


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
        self.popTopLayer()
        topLayer.setContainer2(container)
        self.insertLayer(topLayer)

    def insertLayer(self, layer):
        lighterLayers = self.popLighterLayers(layer.getTotalWeight())
        self.pushLayer(layer)
        self.pushLayers(lighterLayers)

    def popLighterLayers(self, weight):
        lighterLayers = []
        while True:
            if self.isEmpty():
                break
            topLayer = self.getTopLayer()
            if topLayer.getTotalWeight()>=weight:
                break
            self.popTopLayer()
            lighterLayers.append(topLayer)
        return lighterLayers

    def pushLayers(self, layers):
        layers.reverse()
        for layer in layers:
            self.pushLayer(layer)

# 4. Printer
# ----------

class Printer:
    def __init__(self):
        pass

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
        outputFile.write("\n")

    def printContainer(self, container, outputFile):
        outputFile.write("{0:d}".format(container.getSerialNumber()))

printer = Printer()

pile = ContainerPile()
container = Container(1, 20, 2, 10)
pile.pileContainer(container)
container = Container(2, 40, 4, 8)
pile.pileContainer(container)
container = Container(3, 20, 2, 2)
pile.pileContainer(container)

printer.printContainerPile(pile, sys.stdout)


