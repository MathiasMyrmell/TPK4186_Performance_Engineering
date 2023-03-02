#Task 9
import copy

class Node:

    def __init__(self, player, value, pastNode):
        self.player = player
        self.nodes = []
        self.winnerWhite = 0
        self.winnerBlack = 0
        self.draw = 0
        self.nodeValue = value

        self.label = player #remove if nodes in svg hasent color

        self.pastNode = pastNode

        self.structure = None
        

    def setNodeValue(self, value):
        self.nodeValue = value

    def getNodeValue(self):
        return self.nodeValue

    def getNodes(self):
        return self.nodes
    
    def setPastNode(self, value):
        self.pastNode = value
    
    def getPastNode(self):
        return self.pastNode
    
    def getNextNode(self):
        return self.nextNode

    def setNextNode(self, moves):
        if(len(moves) >= 2):
            self.nextNode = moves[2]
        elif(len(moves) == 1):
            self.nextNode = None
    
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
        #Moves[0] = pastNode, Moves[1] = nodeValue, Moves[2] = nextNode
        moves = copy.copy(m)
        nextColor = "White" if self.player == "Black" else "Black"
        # nextNode
        nextNode = moves[0]
        if nextNode in self.getNodeValues():
            if(len(moves) >= 2):
                self.getNodeByValue(nextNode).addGame(moves[1:])
            else:
                return
        else:
            node = Node(nextColor, nextNode, self.getNodeValue())
            if len(moves) >= 2:
                node.addGame(moves[1:])
            self.getNodes().append(node)

        #TODO: set winner



    def addGame1(self, m, firstMove):
        moves = copy.copy(m)
        nextColor = "White" if self.player == "Black" else "Black"
        if firstMove :
            self.setPastNode(None)
            self.setNodeValue(moves[0])
            self.nextNode = moves[1]
            self.setWinner(moves)
        elif len(moves) >= 3:
            self.setPastNode(moves[0])
            self.setNodeValue(moves[1])
            self.setNextNode(moves)
            moves.remove(moves[0])
            self.setWinner(moves)
        elif len(moves) == 2:
            self.setPastNode(moves[0])
            self.setNodeValue(moves[1])
            self.setWinner(moves)
            return

        if self.getNodeValue() in self.getNodes():
            self.getNodeByValue(self.getNodeValue()).addGame(moves, False)
            self.setWinner(moves)
        else:
            node = Node(nextColor)
            node.addGame(moves, False)
            self.getNodes().append(node)
            self.setWinner(moves)
                
    def setWinner(self, moves):
        winner = moves[-1]
        if(winner == "1-0"):
            self.winnerWhite+=1
        elif(winner == "0-1"):
            self.winnerBlack+=1
        else:
            self.draw+=1
        

    def getStructure(self):
        structure = []
        if len(self.getNodes()) == 0:
            if(self.getNodeValue() != "None"):
                # print("Bottom node", self.getNodeValue() )
                structure.append(self.getNodeValue())
        else:
            if(len(self.getNodes()) == 1):
                print("just one node")
                if len(self.getNodes()) == 1:
                    structure.append(self.getNodeValue()+"/"+self.getNodes()[0].getNodeValue())
                else:
                    for stru in self.getNodes():
                        structure.append(self.getNodeValue()+"/"+stru.getNodeValue())
            else:
                print("more than one node",self.getNodes())
            for node in self.getNodes():
                for stru in node.getStructure():
                   structure.append(self.getNodeValue()+"/"+stru)
        print("Structure", structure)
        return structure
