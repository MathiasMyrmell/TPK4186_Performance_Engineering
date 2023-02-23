

class Player():

    def __init__(self,name):
        self.name = name
        self.color = None

    
    def getName(self):
        return self.name
    
    def setColor(self, color):
        self.color = color

    def getColor(self):
        return self.color