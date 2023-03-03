#Task 9
import copy

class Node:

    def __init__(self, player, value, pastNode, tree):
        self.player = player
        self.nodes = []
        self.winnerWhite = 0
        self.winnerBlack = 0
        self.draw = 0
        self.nodeValue = value 
        self.level = None
        self.label = player #remove if nodes in svg hasent color
        self.tree = tree
        self.pastNode = pastNode

        self.structure = None

        self.played = 0
        

    def setNodeValue(self, value):
        self.nodeValue = value

    def getNodeValue(self):
        return self.nodeValue

    def setNodes(self, nodes):
        self.nodes = nodes

    def getNodes(self):
        return self.nodes
    
    def setPastNode(self, value):
        self.pastNode = value
    
    def getPastNode(self):
        return self.pastNode

    def setLevel(self, level):
        self.level = level

    def getLevel(self):
        return self.level
    
    def getTree(self):
        return self.tree
    
    def isLeafNode(self):
        return len(self.getNodes()) == 0

    def getNodeByValue(self, value):
        for i in range(len(self.getNodes())):
            if self.getNodes()[i].getNodeValue() == value:
                return self.getNodes()[i]
        return None
    
    #return list with value of all nodes
    def getNodeValues(self):
        values = []
        for i in range(len(self.getNodes())):
            values.append(self.getNodes()[i].getNodeValue())
        return values

    def addGame(self, m):
        # played = self.getTimesPlayed()
        # self.setTimesPlayed(played+1)
        self.played+=1
        #Moves[0] = pastNode, Moves[1] = nodeValue, Moves[2] = nextNode
        moves = copy.copy(m)
        self.setWinner(m)
        nextColor = "White" if self.player == "Black" else "Black"
        # nextNode
        nextNode = moves[0]
        if nextNode in self.getNodeValues():
            if(len(moves) >= 2):
                self.getNodeByValue(nextNode).addGame(moves[1:])
            else:
                return
        else:
            node = Node(nextColor, nextNode, self, self.getTree()) #self.getNodeValue()
            node.setLevel(self.getLevel()+1)
            if len(moves) >= 2:
                node.addGame(moves[1:])
            self.getNodes().append(node)

    def setTimesPlayed(self, timesPlayed):
        self.played = timesPlayed

    def getTimesPlayed(self):
        return self.played
   
                
    def setWinner(self, moves):
        winner = moves[-1]
        if(winner == "1-0"):
            self.winnerWhite+=1
        elif(winner == "0-1"):
            self.winnerBlack+=1
        else:
            self.draw+=1
        
    def removeNodesUnderDepth(self, depth):
        nodes = self.getNodes()
        newNodes = []
        for i in range(len(nodes)):
            if nodes[i].getLevel() > depth:
                continue
            else:
                nodes[i].removeNodesUnderDepth(depth)
                newNodes.append(nodes[i])
        self.setNodes(newNodes)
    

    def getStructure(self):
        structure = []
        if len(self.getNodes()) == 0:
            if(self.getNodeValue() != "None"):
                # print("Bottom node", self.getNodeValue() )
                structure.append(self.getNodeValue())
        else:
            if len(self.getNodes()) == 1:
                structure.append(self.getNodeValue()+"/"+self.getNodes()[0].getNodeValue())
            else:
                for stru in self.getNodes():
                    structure.append(self.getNodeValue()+"/"+stru.getNodeValue())

            for node in self.getNodes():
                for stru in node.getStructure():
                   structure.append(self.getNodeValue()+"/"+stru)
        return structure



    def getStructureTimesPlayed(self,n):
        structure = []
        #Check if this is last node
        lastNode = True
        for node in self.getNodes():
            if node.getTimesPlayed() >= n:
                lastNode = False
                break
        if lastNode:
            structure.append(self.getNodeValue())
            return structure
        else:
            if len(self.getNodes()) == 0:
                # print("bottom node", self.getNodeValue())
                structure.append(self.getNodeValue())
            else:
                # print("node", self.getNodeValue())
                for node in self.getNodes():
                    if node.getTimesPlayed() >= n:
                        # print(node.getNodeValue())
                        for stru in node.getStructureTimesPlayed(n):
                            structure.append(self.getNodeValue()+"/"+stru)
        return structure
    
    def getWinnersFromLeafs(self):
        winners = []
        if self.isLeafNode():
            self.getTree().setWinnerFromLeaf([self.getNodeValue(),self.getPastNode().getNodeValue(),self.getWinners()])
        else:
            for node in self.getNodes():
                winners.append(node.getWinnersFromLeafs())
        return winners
                

    def getWinners(self):
        return [self._getWinnerWhite(), self._getWinnerBlack(), self._getDraw()]

    def _getWinnerWhite(self):
        return self.winnerWhite
    
    def _getWinnerBlack(self):
        return self.winnerBlack
    
    def _getDraw(self):
        return self.draw
    

    def getTimesPlayedLeaf(self):
        timesPlayed = []
        if self.isLeafNode():
            self.getTree().setTimesPlayedLeaf([self.getNodeValue(),self.getPastNode().getNodeValue(),self.getTimesPlayed()])
        else:
            for node in self.getNodes():
                timesPlayed.append(node.getTimesPlayedLeaf())
        return timesPlayed