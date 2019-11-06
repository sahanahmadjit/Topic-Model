import csv
import networkx as nx
import math


mac_data_directory= "/zWorkStation/JournalWork/Topic-Model/Data/"
linux_data_directory="/home/C00408440/ZWorkStation/JournalVersion/Data/"


TOP_ZSCORE_TERM_NUMBER =2
G= nx.DiGraph()
zScore_G= nx.DiGraph()

finalDictonaryCommunity = dict()
zScoreFinalDictonaryCommunity = dict()
nonOverlappingFinalDictonaryCommunity= dict()
communityNumber=0

#topZScoreTerm  if else condition should be same

def building_graph_from_text_data():
  for itaration in range(2):
    with open(mac_data_directory + 'GraphData/GraphInputData_Test.txt') as csv_file:
      csv_reader = csv.reader(csv_file, delimiter='|')
      for line in csv_reader:
        if itaration==0:
          G.add_node(line[0])
          continue
        else:
          for i in range(1,len(line),2): # 1:Starting from 2nd term {first term is source}, stop, increment by 2
            G.add_edge(line[0],line[i],weight=line[i+1])
            #print("Processing Node for:" + line[0])

def building_topZScoreBased_graph_from_text_data():
  #Take Top Zcore term into a list
  topZScoreTermDict=[]
  topZScoreTerm=TOP_ZSCORE_TERM_NUMBER
  with open(mac_data_directory + 'GraphData/zScoreSorted_Test.txt') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter='|')
    for line in csv_reader:
      if topZScoreTerm==0:
        break
      else:
        topZScoreTermDict.append(line[0])
        topZScoreTerm -= 1
    print("Top ZScore Term List", topZScoreTermDict)

  for itaration in range(2):
    with open(mac_data_directory + 'GraphData/GraphInputData_Test.txt') as csv_file:
      csv_reader = csv.reader(csv_file, delimiter='|')
      for line in csv_reader:
        if itaration==0:
          zScore_G.add_node(line[0])
          continue
        else:
          for i in range(1,len(line),2): # 1:Starting from 2nd term {first term is source}, stop, increment by 2
            if line[0] in topZScoreTermDict or line[i] in topZScoreTermDict:
              zScore_G.add_edge(line[0],line[i],weight=line[i+1])
              #print("Processing Node for:" + line[0] + line[i])




def print_Graph_Statistics():
  print("Number of Nodes In Graph: " + str(G.number_of_nodes()))
  print("Number of Edges In Graph: "+ str(G.number_of_edges()))
def export_Graph_to_Gephi_format():
  nx.write_gexf(G,mac_data_directory+"GraphData/gephi_format_graph.gexf")


def export_Lower_CommunityGraph_to_Gephi_format():
  nx.write_gexf(G,mac_data_directory+"GraphData/gephi_format_LowerCommunityGraph.gexf")

def disconnectTopTermInGraph():
  with open(mac_data_directory + 'GraphData/zScoreSorted_Test.txt') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter='|')
    topZScoreTerm=TOP_ZSCORE_TERM_NUMBER
    for line in csv_reader:
      if topZScoreTerm ==0:
        break
      else:
        G.remove_node(line[0])
        topZScoreTerm -= 1


def lowerLevelConnectivityChecking():
  logFile= open(mac_data_directory + 'GraphData/LowerConnectivityLogFile.txt',"w")
  with open(mac_data_directory + 'GraphData/zScoreSorted.txt') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter='|')
    topZScoreTerm=TOP_ZSCORE_TERM_NUMBER
    for line in csv_reader:
      if topZScoreTerm ==0:
        continue
      else:topZScoreTerm -= 1

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
  topZScoreTerm = TOP_ZSCORE_TERM_NUMBER
  with open(mac_data_directory + 'GraphData/zScoreSorted_Test.txt') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter='|')
    queueDictonaryCommnunity = dict()

    global communityNumber #Global variable to track total number of community
    for line in csv_reader:
      if topZScoreTerm >0:
        topZScoreTerm -= 1
        continue

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
  logFile = open(mac_data_directory + 'GraphData/LowerConnectivityLogFile_Test.txt', "w")
  for k,v in finalDictonaryCommunity.items():
    print(k,v)
  for k,v in finalDictonaryCommunity.items():
    logFile.write(k + "|" + str(v) + "|")


def hierarchicalCommunityConnection():

  with open(mac_data_directory + 'GraphData/zScoreSorted_Test.txt') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter='|')
    topZScoreTerm=TOP_ZSCORE_TERM_NUMBER
    for line in csv_reader:
      communityNumberCollection = dict()
      listofCommunity=[]
      if topZScoreTerm==0:
        break
      else:
        topZScoreTerm-=1
      sourceTerm=line[0]
      print(sourceTerm,zScore_G.edges)
      inEdgesTouple=zScore_G.in_edges(sourceTerm)
      print("In Edges:", len(inEdgesTouple))
      inEdges=[]
      for term in inEdgesTouple:#Take inEdges touple to a list
        inEdges.append(term[0])


      outEdges = zScore_G[sourceTerm]

      for term in outEdges:
        if term in inEdges:
          communityNumber= finalDictonaryCommunity[term]#Find out the community Number
          if communityNumber in communityNumberCollection:
            oldCommunityNumber= communityNumberCollection[communityNumber]#Retrive the Number of community as an example 1|3   3 terms of 1 community
            oldCommunityNumber +=1
            communityNumberCollection[communityNumber]=oldCommunityNumber
          else:
            communityNumberCollection[communityNumber]=1
          max_Commnuity_Number=0
          max_community= 0
          for k,v in communityNumberCollection.items():
            if v>max_Commnuity_Number:
              max_community = k
          listofCommunity.append(max_community)
      zScoreFinalDictonaryCommunity[sourceTerm]=listofCommunity

  for k,v in zScoreFinalDictonaryCommunity.items():
    print("Term:", k, "Value:", v)



def non_overlapping_hierarchicalCommunityConnection():
  for k,v in zScoreFinalDictonaryCommunity.items():
    allCommunityList= v
    allCommunitySummationDict=dict()
    for community in allCommunityList:
      if community not in allCommunitySummationDict:
        allCommunitySummationDict[community]=1
      else:
        prevCommunityVal=allCommunitySummationDict.get(community)
        prevCommunityVal+=1
        allCommunitySummationDict[community]=prevCommunityVal

    nonOverlappingFinalDictonaryCommunity[k]=allCommunitySummationDict
  print(communityNumber)
  for k,v in nonOverlappingFinalDictonaryCommunity.items():
    print("Term:", k, "Value:", v)
  for communityNumberByOrder in range(0,communityNumber-1):
    maxCommunityTerm=0
    maxCommunityNumber=0
    for k,v in nonOverlappingFinalDictonaryCommunity.items():#first loop  to find out maxCommunityTerm
     if communityNumberByOrder in v:
        if maxCommunityNumber<v[communityNumberByOrder]:
          maxCommunityNumber= v[communityNumberByOrder]
          maxCommunityTerm=k

    for k,v in nonOverlappingFinalDictonaryCommunity.items():#second loop to delete overlapping community and keep the max one
       if k==maxCommunityTerm:
         continue
       elif communityNumberByOrder in v:
         del v[communityNumberByOrder]

  for k,v in nonOverlappingFinalDictonaryCommunity.items():
    print("Term:", k, "Value:", v)


def samplingTermFromCommunity():
  CopyG=G

  #finalDictonaryCommunity

  for communityNumberByOrder in range(0,communityNumber-1):
    cardinalityDict = dict()
    for k,v in finalDictonaryCommunity.items():
      if v== communityNumberByOrder:
        outgoingEdge = G[k] #outgoing Edge/neightbor node
        cardinalityDict[k]= len(outgoingEdge)

    print(sorted(cardinalityDict.items(), key= lambda kv: (kv[1], kv[0])))










def main_Graph_Building_function():
  building_graph_from_text_data()
  disconnectTopTermInGraph()
  '''
 
  export_Graph_to_Gephi_format()
  print_Graph_Statistics()
  
  lowerLevelConnectivityChecking()
  print_Graph_Statistics()
  export_Lower_CommunityGraph_to_Gephi_format()
   '''
  lowerLevelCommunityNumber()
  building_topZScoreBased_graph_from_text_data()
  hierarchicalCommunityConnection()
  non_overlapping_hierarchicalCommunityConnection()
  samplingTermFromCommunity()
  #print_Graph()


main_Graph_Building_function()
