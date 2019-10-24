import csv
import networkx as nx
import math

mac_data_directory= "/zWorkStation/JournalWork/Topic-Model/Data/"
linux_data_directory="/home/C00408440/ZWorkStation/JournalVersion/Data/"

G= nx.DiGraph()


def building_graph_from_text_data():
  for itaration in range(2):
    with open(linux_data_directory + 'GraphData/GraphInputData_Test.txt') as csv_file:
      csv_reader = csv.reader(csv_file, delimiter='|')
      #limitLineForExperiment=0
      for line in csv_reader:
       # if limitLineForExperiment>10000:
        #  break
        #limitLineForExperiment+=1
        if itaration==0:
          G.add_node(line[0])
          continue
        else:
          for i in range(1,len(line),2): # 1:Starting from 2nd term {first term is source}, stop, increment by 2
            G.add_edge(line[0],line[i],weight=line[i+1])
            #print("Processing Node for:" + line[0])

def print_Graph_Statistics():
  print("Number of Nodes In Graph: " + str(G.number_of_nodes()))
  print("Number of Edges In Graph: "+ str(G.number_of_edges()))
def export_Graph_to_Gephi_format():
  nx.write_gexf(G,mac_data_directory+"GraphData/gephi_format_graph.gexf")


def export_Lower_CommunityGraph_to_Gephi_format():
  nx.write_gexf(G,mac_data_directory+"GraphData/gephi_format_LowerCommunityGraph.gexf")

def disconnectTopTermInGraph():
  with open(mac_data_directory + 'GraphData/zScoreSorted.txt') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter='|')
    topTermNumber=0
    for line in csv_reader:
      G.remove_node(line[0])
      if topTermNumber <100:
        break
      topTermNumber += 1


def lowerLevelConnectivityChecking():
  logFile= open(mac_data_directory + 'GraphData/LowerConnectivityLogFile.txt',"w")
  with open(mac_data_directory + 'GraphData/zScoreSorted.txt') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter='|')
    avoidTopZScoreTerm=0
    for line in csv_reader:
      if avoidTopZScoreTerm<100:
        avoidTopZScoreTerm += 1
        continue

      neighborsNode= G[line[0]]
      logFile.write("Soruce: "+ line[0] + "\n")
      logFile.write("NeighborNode:" +"\n")


      totalConnectedTerm=len(neighborsNode)
      totalFrequency=0
      counterForLogFileWrite=0
      for term in neighborsNode:
        weightDict= neighborsNode[term]
        if counterForLogFileWrite==10:
          logFile.write("\n")
          counterForLogFileWrite=0
        else:
          counterForLogFileWrite+=1
        logFile.write(term + " | ")
        for weightVal in weightDict:
         logFile.write(weightDict[weightVal]+ " | ")
         totalFrequency+=int(weightDict[weightVal])
      #Mean Devaition Calculation for the term
      mean=float(totalFrequency/totalConnectedTerm)
      logFile.write("\n" + "Mean: " + str(mean) +"\n")



      SD_Value=deviationCalculation(mean,line[0],neighborsNode)
      logFile.write("SD Value: "+str(SD_Value)+"\n")
      removedEdgeList=[]
      for term in neighborsNode:
        weightDict= neighborsNode[term]
        for weightVal in weightDict:
         if int(weightDict[weightVal])<mean:
           oneSDVal=mean-SD_Value
           if int(weightDict[weightVal])<oneSDVal:
             removedEdgeList.append(term)
      for removeTerm in removedEdgeList:
        G.remove_edge(line[0],removeTerm)
        logFile.write("Edges Remove From "+ line[0]+ " to "+ removeTerm+"\n")


def deviationCalculation(mean,sourceTerm,neighborsNode):
  meanDeviationSummation=0.0
  standardDeviationSummation=0.0
  for term in neighborsNode:
    weightDict=neighborsNode[term]
    for weightVal in weightDict:
      deviation=abs(int(weightDict[weightVal])-mean)
      meanDeviationSummation+=deviation
      standardDeviationSummation+= math.pow(deviation,2)
  meanDeviation=meanDeviationSummation/len(neighborsNode)
  standardDeviation=math.sqrt(standardDeviationSummation/len(neighborsNode))
  return standardDeviation

def lowerLevelCommunityNumber():
  with open(linux_data_directory + 'GraphData/zScoreSorted_Test.txt') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter='|')

    queueDictonaryCommnunity = dict()
    finalDictonaryCommunity = dict()
    communityNumber = 0
    for line in csv_reader:
      sourceTerm= line[0]
      if sourceTerm in finalDictonaryCommunity:
        continue
   #   print("Source Term ", sourceTerm)
      inEdgesTouple=G.in_edges(sourceTerm)
   #   print(inEdgesTouple)
      inEdges=[]
      for term in inEdgesTouple:#Take inEdges touple to a list
        inEdges.append(term[0])


      outEdges = G[sourceTerm]
      for term in outEdges:
        if term in finalDictonaryCommunity:
          continue #Already Processed. So continue
        elif term in inEdges: #Check the both incoming and outgoing edge
          queueDictonaryCommnunity[term]= communityNumber
        elif len(G[term])==0: #Check the outgoing node has any neighbour [outgoing edges]
          queueDictonaryCommnunity[term]=communityNumber

      #Do the same thing for incomingEdges
      for term in inEdges:
        if term in finalDictonaryCommunity:
          continue #Already Processed. So continue
        elif len(G[term])==0 or len(G[term])==1:  # Check the incoming node has any neighbour [outgoing edges] or only one outgoing edge which connected to this node
          queueDictonaryCommnunity[term] = communityNumber

      #All node visited. Pop the source term from queue to Final queue
      finalDictonaryCommunity[sourceTerm]=communityNumber
      #Now processed all the queue item for this source term
      while (bool(queueDictonaryCommnunity)):
        tempInsertQueueDict= dict()
        for key,value in queueDictonaryCommnunity.items():
          if key in finalDictonaryCommunity:
            continue #already processed
          inEdgesTouple = G.in_edges(key)
          inEdges=[]
          for term in inEdgesTouple:
            inEdges.append(term[0])
          outEdges = G[key]
          for term in inEdges:
            if term in finalDictonaryCommunity:
              continue
            elif term in outEdges:  # Check the both incoming and outgoing edge
              tempInsertQueueDict[term] = value
            elif len(G[term])==0 or len(G[term])==1:  # Check the unidirected node has any neighbour [outgoing edges] or only one outgoing edge which connected to this node.
              tempInsertQueueDict[term] = value
          #Same process but now consider outedges
          for term in outEdges:
            if term in finalDictonaryCommunity:
              continue
            elif len(G[term]) == 0:  # Check the unidirected node has any neighbour [outgoing edges]
              tempInsertQueueDict[term] = value
          #All nodes processed for queue item. Now pop it from queue and add it to the FINAL queue
          finalDictonaryCommunity[key]=value
        #New InsertDictonary become the queue dictonary now
        queueDictonaryCommnunity=tempInsertQueueDict

      #Maximun Distance travelled for the current Community No node left. Increase Community Number
      communityNumber += 1
  print("Total Community Number ", communityNumber)

  for k,v in finalDictonaryCommunity.items():
    print("Node: ", k, " Community: ",v)








building_graph_from_text_data()

def main_Graph_Building_function():
  building_graph_from_text_data()
  '''
 
  export_Graph_to_Gephi_format()
  print_Graph_Statistics()
  disconnectTopTermInGraph()
  lowerLevelConnectivityChecking()
  print_Graph_Statistics()
  export_Lower_CommunityGraph_to_Gephi_format()
   '''
  lowerLevelCommunityNumber()
  #print_Graph()


main_Graph_Building_function()
