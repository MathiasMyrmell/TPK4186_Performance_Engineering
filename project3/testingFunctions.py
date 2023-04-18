# #Testing interval to input buffer
    # path = "project3/testing/inputTime/"
    # batchSizes = [20,35,50]
    # batchProdductionTime = [273, 462, 654]
    # plotData = []
    # totFiles = 1
    # for k in range(len(batchSizes)):
    #     resultat = []
    #     for j in range(1,batchProdductionTime[k], 3):
    #         productionGoal = 1000
    #         tasksInUnits = [[1,3,6,9],[2,5,7],[4,8]]
    #         # heuristics = [[1,3,6,9],[2,5,7],[4,8]]
    #         heuristics = [[9,6,3,1],[7,5,2],[8,4]]
    #         loadToInputBufferInterval = j
    #         groupingOfBatches = batchSizes[k]
    #         SIM = Simulator(path+str(batchSizes[k])+"/",productionGoal,tasksInUnits, heuristics, loadToInputBufferInterval, groupingOfBatches)
    #         P = SIM.printer
    #         SC = SIM.scheduler
    #         PL = SIM.productionline

    #         runningtime = SIM.run()
    #         res = [j,runningtime]
    #         resultat.append(res)
    #         # print(i, SIM.run())
    #         # P.getStatus()
    #         print(str(batchSizes[k])+" file number: "+str(totFiles))
    #         totFiles += 1
    #     # print(resultat)
    #     print("Batch size: "+str(batchSizes[k])+ " done")
    #     totFiles = 1

    # def getInfoFromFile(file):
    #     groupingOfBatches = ""
    #     lastLine = ""
    #     # try:
    #     f = open(file, "r")
    #     i = 1
        
    #     for line in f:
    #         # Grouping of batches
    #         # if i == 20:
    #         #     groupingOfBatches = line

    #         # Time between batches to input buffer
    #         if i == 19:
    #             groupingOfBatches = line
    #         lastLine = line
    #         i += 1
    #     f.close()
    #     # except:
    #         # print("could not read file")
    #     return [groupingOfBatches, lastLine]

    # def getData(info):
    #     # print(info)
    #     #Get grouping
    #     grouping = info[0].split(" ")[-1].split("\n")[0]
    #     # print(grouping)

    #     #Get running time
    #     runningTime = info[1].split("\t")[0]
        
    #     # print("grouping", grouping)
    #     # print("runningTime", runningTime)
    #     return [float(grouping),float(runningTime)]
    
    # print("Started reading files")
    # path = "project3/testing/inputTime/"
    # os.chdir(path)
    # for m in range(len(batchSizes)):
    #     print("Batch size: "+str(batchSizes[m])+" started")
    #     os.chdir(str(batchSizes[m])+"/")
    #     result = []
    #     for file in os.listdir():
    #         if file.endswith(".txt"):
    #             info = getInfoFromFile(file)
    #             result.append(getData(info))

    #     print("Files read")
    #     # print(result)
        
    #     # Sort result
    #     print("Sorting data")
    #     print("Result: ", result)
    #     data = []
    #     while len(result)>0:
    #         lowestLoadingtime = float("inf")
    #         for res in result:
    #             if res[0] < lowestLoadingtime:
    #                 lowestLoadingtime = res[0]
    #         for res in result:
    #             if res[0] == lowestLoadingtime:
    #                 data.append(res)
    #                 result.remove(res)
    #                 break
    #         lowestLoadingtime = float("inf")
        
    #     print("Data sorted")
    #     print("Sorted "+str(batchSizes[m])+":", data)
    #     xAxis = []
    #     yAxis = []
    #     print("Creating plot data")
    #     for i in range(len(data)):
    #         xAxis.append(data[i][0])
    #         yAxis.append(data[i][1])
    #     # Print plot
    #     # print("xAxis: ", xAxis)
    #     # print("yAxis: ", yAxis)
    #     plotData.append([batchSizes[m],xAxis,yAxis])
    #     print("Plot data created")
    #     os.chdir("..")
    # os.chdir("../../..")
    # print("Plotting")
    # fig = plt.figure()
    # legend = []
    # colors = ['g', 'r', 'b']
    # i = 0
    # print("plotData", plotData)
    # for plot in plotData:
    #     legend.append(str(plot[0]))
    #     plt.plot(plot[1], plot[2], label="Batch size: " + str(plot[0]), color=colors[i])
    #     # plt.plot(xAxis, yAxis)
    #     i+=1
    # plt.xlabel("Loadingtime to inputbuffer interval",fontsize='13')	
    # plt.ylabel("Time",fontsize='13')
    # plt.legend(legend, loc='upper left')
    # fig.savefig("project3/figures/MotsattHierarkisk.png")
    # plt.show()




  # # Testing heuristics
    # a = [1,3,6,9]
    # b = [2,5,7]
    # c = [4,8]
    # heuristics = [[1,3,6,9],[2,5,7],[4,8]]
    # def createHeuristics(heu):
    #     unit1 = heu[0]
    #     hU1 = []
    #     for i in unit1:
    #         for j in unit1:
    #             for k in unit1:
    #                 for l in unit1:
    #                     if i != j and i != k and i != l and j != k and j != l and k != l:
    #                         hU1.append([i,j,k,l])

    #     unit2 = heu[1]
    #     hU2 = []
    #     for i in unit2:
    #         for j in unit2:
    #             for k in unit2:
    #                 if i != j and i != k and j != k:
    #                     hU2.append([i,j,k])


    #     unit3 = heu[2]
    #     hU3 = []
    #     for i in unit3:
    #         for j in unit3:
    #             if i != j:
    #                 hU3.append([i,j])
    #     return hU1,hU2,hU3

    # hU1,hU2,hU3 = createHeuristics(heuristics)
    
    # Run simulation for each heuristic and batch size
    # batchSizes = [20,27,35,43,50]
    # i = 1

    # for u1 in hU1:
    #     for u2 in hU2:
    #         for u3 in hU3:
    #             for batchSize in batchSizes:
    #                 path = "project3/testing/heuristics/"
    #                 productionGoal = 1000
    #                 tasksInUnits = [[1,3,6,9],[2,5,7],[4,8]]
    #                 heuristics = [u1,u2,u3]
    #                 loadToInputBufferInterval = 1
    #                 groupingOfBatches = batchSize
    #                 SIM = Simulator(path, productionGoal,tasksInUnits, heuristics, loadToInputBufferInterval, groupingOfBatches)
    #                 P = SIM.printer
    #                 SC = SIM.scheduler
    #                 PL = SIM.productionline

    #                 SIM.run()
    #                 print(i)
    #             i += 1
    
    # def creatHeuristicNumber():
    #     heu = {}
    #     i = 1
    #     for u1 in hU1:
    #         for u2 in hU2:
    #             for u3 in hU3:
    #                 heu[str([u1,u2,u3])] = i
    #                 i += 1
    #     return heu
    
    # heu = creatHeuristicNumber()
    # print(heu)
    # def getHeuristicNumber(heur):
    #     # print(heu.replace(" ",""))
    #     for keys in heu:
    #         if keys.replace(" ","") == heur.replace(" ",""):
    #             return heu[keys]

    # # Read Files
    # path = os.chdir("project3/testing/heuristics/")
    # result = {}
    # for file in os.listdir(path):
    #     if file.endswith(".txt"):
    #         f = open(file, "r")
    #         i = 1
    #         h1 = None
    #         h2 = None
    #         h3 = None
    #         groupingOfBatches = None
    #         lastLine = None
    #         for line in f:
    #             # Heuristics
    #             if i == 9:
    #                 h1 = line
    #             elif i == 14:
    #                 h2 = line
    #             elif i == 18:
    #                 h3 = line
    #             # Batch size
    #             elif i == 20:
    #                 groupingOfBatches = line
    #             lastLine = line
    #             i += 1
    #         f.close()
    #         # except:
    #             # print("could not read file")
    #     # String to int 
    #     h1 = h1.split(":")[1].replace("\n","")#.replace("[","").replace("]","").split(', ')
    #     # h1 = [int(i) for i in h1]
    #     h2 = h2.split(":")[1].replace("\n","")#.replace("[","").replace("]","").split(', ')
    #     # h2 = [int(i) for i in h2]
    #     h3 = h3.split(":")[1].replace("\n","")#.replace("[","").replace("]","").split(', ')
    #     # h3 = [int(i) for i in h3]
    #     heursitic = "["+str(h1)+","+str(h2)+","+str(h3)+"]"
    #     heuristicNumber = getHeuristicNumber(heursitic)
    #     groupingOfBatches = int(groupingOfBatches.split(" ")[-1].replace("\n",""))
    #     lastLine = lastLine.split("\t")[0]
    #     if groupingOfBatches not in result:
    #         result[groupingOfBatches] = [[heuristicNumber, lastLine]]
    #     else:
    #         result[groupingOfBatches].append([heuristicNumber,lastLine])
    # os.chdir("../../..")
    # # print(result)


    # def getplotData(dataList):
    #     xValue = []
    #     yValue = []
    #     while len(dataList) > 0:
    #         minXvalue = float("inf")
    #         minYvalue = None
    #         data = None
    #         for d in dataList:
    #             if float(d[0]) < minXvalue:
    #                 minXvalue = int(d[0])
    #                 minYvalue = float(d[1])
    #                 data = d

    #     #             min = float(i[0])
    #     #             minIndex = i
    #         xValue.append(minXvalue)
    #         yValue.append(minYvalue)
    #         dataList.remove(data)
    #     return xValue, yValue
    # #data [[56, '5731.5'], [178, '6191.5'], [61, '6358.0'], [236, '5731.5'], [160, '6168.5'], [159, '6216.5'], [215, '5671.0'], [274, '6191.5']
    
    # def getSortedPlotData(xValue, yValue):
    #     xV = []
    #     yV = []
    #     for i in range(len(yValue)):
    #         if yValue[i] < 5672:
    #             xV.append(xValue[i])
    #             yV.append(yValue[i])
    #     return xV, yV

    # #Create plot
    # fig = plt.figure()
    # for key in result:
    #     xValue, yValue = getplotData(result[key])
    #     xV , yV = getSortedPlotData(xValue, yValue)
    #     print(len(xV))
    #     # print("res", xValue)
    #     # plt.plot(xValue, yValue, label=key)
    #     plt.plot(xV, yV, label=key)


    # plt.xlabel("Heuristic",fontsize='13')
    # plt.ylabel("Time",fontsize='13')
    # plt.legend()
    # fig.savefig("project3/figures/OptimalHeuristic2.png")
    # plt.show()



    # #Testing each buffer size
    # for i in range(20,51):
    #     worstCase = worstCaseRunningTime(i)
    #     minInputTime = int(worstCase*0.355)
    #     maxInoputTime = int(worstCase*0.47)
    #     for j in range(minInputTime, maxInoputTime+1):
    #         path = "project3/testing/batchSizes/"
    #         productionGoal = 1000
    #         tasksInUnits = [[1,3,6,9],[2,5,7],[4,8]]
    #         heuristics = [[1,3,6,9],[2,5,7],[4,8]]
    #         loadToInputBufferInterval = j
    #         groupingOfBatches = i
    #         SIM = Simulator(path, productionGoal,tasksInUnits, heuristics, loadToInputBufferInterval, groupingOfBatches)
    #         P = SIM.printer
    #         SC = SIM.scheduler
    #         PL = SIM.productionline

    #         print(SIM.run())

    # Read files
    # path = os.chdir("project3/testing/batchSizes/")
    # result = {}
    # for file in os.listdir(path):
    #     if file.endswith(".txt"):
    #         f = open(file, "r")
    #         i = 1
    #         groupingOfBatches = None
    #         loadToInputBufferInterval = None
    #         h1 = None
    #         h2 = None
    #         h3 = None
    #         for line in f:
    #             # Heuristics
    #             if i == 9:
    #                 h1 = line.split(":")[1]
    #             elif i == 14:
    #                 h2 = line.split(":")[1]
    #             elif i == 18:
    #                 h3 = line.split(":")[1]
    #             # Load to input buffer interval
    #             if i == 19:
    #                 loadToInputBufferInterval = line
    #             # Batch size
    #             elif i == 20:
    #                 groupingOfBatches = line
    #             lastLine = line
    #             i += 1
    #         f.close()
    #         # except:
    #             # print("could not read file")
    #     # String to int 
    #     groupingOfBatches = groupingOfBatches.split(" ")[-1].replace("\n","")
    #     loadToInputBufferInterval=loadToInputBufferInterval.split(" ")[-1].replace("\n","")
    #     lastLine = lastLine.split("\t")[0]
    #     if groupingOfBatches not in result:
    #         result[groupingOfBatches] = [[loadToInputBufferInterval, lastLine, [h1, h2, h3]]]
    #     else:
    #         result[groupingOfBatches].append([loadToInputBufferInterval,lastLine, [h1, h2, h3]])
    # # print(result)
    # os.chdir("../../..")
    # # Find lowest time for each batch size
    # reduced = {}

    # for key in sorted(result):
    #     minTime = float("inf")
    #     interval = None
    #     heuristic = None
    #     for value in result[key]:
    #         if float(value[1]) < minTime:
    #             minTime = float(value[1])
    #             interval = float(value[0])
    #             heuristic = [value[2]]
    #     reduced[key] = [[interval, minTime, heuristic]]
    
    # print(reduced)

    # # create plot data
    # xValue = []
    # yValue = []
    # for key in sorted(reduced):
    #     xValue.append(int(key))
    #     yValue.append(reduced[key][0][1])
    # print("X",xValue)
    # print("Y",yValue)
    # # Plot result
    # # xValue = 25
    # # yValue = reduced["25"][0][1]
    # fig = plt.figure()
    # plt.plot(xValue, yValue)
    # plt.xlabel("Batch size",fontsize='13')
    # plt.ylabel("Time",fontsize='13')
    # fig.savefig("project3/figures/OptimalBatchSize2.png")
    # plt.show()