import networkx as nx
import csv
import math
import operator
from enum import Enum
import matplotlib.pyplot as plt


class percentageOfTopValue(Enum):
    A = .10
    B = .20
    C = .30

    D = .40
    E = .50

    F = .50
    G = .50


coVaraitionValueRange = {
    'identicalRangeOne': .10,
    'identicalRangeTwo': .20,
    'identicalRangeThree': .30,

    'mediumDiffRangeOne': .50,
    'mediumDiffRangeTwo': .70,

    'spredingRangeOne': .80,
    'spreadingRangeTwo': .90}

CO_EFFICIENT_FOR_COMMUNITY_JOIN = .25
LOWER_LEVEL_CO_EFFICIENT_FOR_COMMUNITY_JOIN = .05
C0_EFFICIENT_FOR_MULTIPLE_COMMUNITY = .05
global COMMUNITY_NUMBER
TOP_ZSCORE_TERM_NUMBER = 15
CO_EFFICIENT = 1
SAMPLING_TERM_COLLECTION_NUMBER = 5

MAC_DATA_DIRECTORY = "/ZResearchCode/HTopicModel/Topic-Model/Data/"
linux_data_directory = "/home/C00408440/ZWorkStation/JournalVersion/Data/"
GRAPH_DATA_DIRECTORY = "GraphData/"
COMMUNITY_DATA_DIRECTORY = "CommunityData/"
RANGE_DATA_DIRECTORY = "ClusterRange/"
SAMPLING_STATISTICS_DIRECTORY = "SampleStatistics/"
GRAPH_INPUT_DATA_FILENAME = "GraphInputData_NewsGroup.txt"
ZSCORE_SORTED_FILENAME = "zScoreSorted_NEWSGROUP.txt"
GEPHI_FORMAT_GRAPH_FILENAME = "gephi_format_graph_NEWSGROUP.gexf"
GEPHI_FORMAT_LOWER_LEVEL_COMMUNITY_GRAPH_FILENAME = "gephi_format_LowerCommunityGraph_NEWSGROUP.gexf"
LOWER_LEVEL_CONNECTIVITY_LOGFILE = "LowerConnectivityLogFile_NEWSGROUP.txt"
SAMPLING_FILENAME = "SamplingFile_Test"
EDGE_REMOVE_LIST_LOGFILE = "LowerLevelEdgeRemovalLogFile_NEWSGROUP.txt"
ZSCORE_REVERSE_SORTED_FILENAME = "ZREVERSE_SORTED_NEWSGROUP.txt"
CO_VARIATION_VALUE_FILENAME = "CO_VARIATION_VALUE_NEWSGROUP.txt"
TOP_CLUSTER_TERM_DATA_FILENAME= "NEWSGROUP_TOP_CLUSTER_TERM.txt"
ZSORE_SORTED_BY_ASSO_FILENAME = "zScoreSortedByAsso_NEWSGROUP.txt"


G = nx.DiGraph()
rebuildG = nx.DiGraph()
zScore_G = nx.DiGraph()

finalDictonaryCommunity = dict()
zScoreFinalDictonaryCommunity = dict()
nonOverlappingFinalDictonaryCommunity = dict()
communityTrackingDict = dict()
hLevelCommunityNumberDict = dict()
communityGraphHashMap = dict()
zScoreAssocationDict = dict()
markMultipleCommunity = []
unabletoConnectCommunity = []




def export_Graph_to_Gephi_format():
    nx.write_gexf(G, MAC_DATA_DIRECTORY + GRAPH_DATA_DIRECTORY + GEPHI_FORMAT_GRAPH_FILENAME)


# topZScoreTerm  if else condition should be same

def building_graph_from_text_data():
    for itaration in range(2):
        with open(MAC_DATA_DIRECTORY + GRAPH_DATA_DIRECTORY + GRAPH_INPUT_DATA_FILENAME) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter='|')
            for line in csv_reader:
                if itaration == 0:
                    G.add_node(line[0])
                    continue
                else:
                    for i in range(1, len(line),
                                   2):  # 1:Starting from 2nd term {first term is source}, stop, increment by 2
                        G.add_edge(line[0], line[i], weight=line[i + 1])


def deviationCalculation(mean, sourceTerm, neighborsNode):
    meanDeviationSummation = 0.0
    standardDeviationSummation = 0.0
    for term in neighborsNode:
        weightDict = neighborsNode[term]
        for weightVal in weightDict:
            deviation = abs(float(weightDict[weightVal]) - mean)
            meanDeviationSummation += deviation
            standardDeviationSummation += math.pow(deviation, 2)
    if len(neighborsNode) == 0:  # avoid devision by zero problem
        meanDeviation = 0
        standardDeviation = 0
    else:
        meanDeviation = meanDeviationSummation / len(neighborsNode)
        standardDeviation = math.sqrt(standardDeviationSummation / len(neighborsNode))
    return standardDeviation


def co_Variation():
    print("Mean Value= mean *", CO_EFFICIENT)
    total_Covarience = 0.0
    logFile = open(MAC_DATA_DIRECTORY + GRAPH_DATA_DIRECTORY + CO_VARIATION_VALUE_FILENAME, "w")
    with open(MAC_DATA_DIRECTORY + GRAPH_DATA_DIRECTORY + ZSCORE_SORTED_FILENAME) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='|')
        topZScoreTerm = TOP_ZSCORE_TERM_NUMBER
        termNumber = 0
        for line in csv_reader:
            if topZScoreTerm != 0:
                topZScoreTerm -= 1
                continue
            neighborsNode = G[line[0]]
            totalConnectedTerm = len(neighborsNode)
            totalFrequency = 0
            counterForLogFileWrite = 0
            for term in neighborsNode:
                weightDict = neighborsNode[term]
                for weightVal in weightDict:
                    totalFrequency += float(weightDict[weightVal])
            # Mean Devaition Calculation for the term
            if totalConnectedTerm == 0:  # avoid division by zero problem
                mean = 0
            else:
                mean = float(totalFrequency / totalConnectedTerm)

            SD_Value = deviationCalculation(mean, line[0], neighborsNode)
            coVarience = float(SD_Value / mean)
            total_Covarience = total_Covarience + coVarience
            logFile.write(line[0] + "|" + str(mean) + "|" + str(SD_Value) + "|" + str(coVarience) + "\n")


def co_Variation():
    print("Mean Value= mean *", CO_EFFICIENT)
    total_Covarience = 0.0
    logFile = open(MAC_DATA_DIRECTORY + GRAPH_DATA_DIRECTORY + CO_VARIATION_VALUE_FILENAME, "w")
    with open(MAC_DATA_DIRECTORY + GRAPH_DATA_DIRECTORY + ZSCORE_SORTED_FILENAME) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='|')
        topZScoreTerm = TOP_ZSCORE_TERM_NUMBER
        termNumber = 0
        for line in csv_reader:
            if topZScoreTerm != 0:
                topZScoreTerm -= 1
                continue
            neighborsNode = G[line[0]]
            totalConnectedTerm = len(neighborsNode)
            totalFrequency = 0
            counterForLogFileWrite = 0
            for term in neighborsNode:
                weightDict = neighborsNode[term]
                for weightVal in weightDict:
                    totalFrequency += float(weightDict[weightVal])
            # Mean Devaition Calculation for the term
            if totalConnectedTerm == 0:  # avoid division by zero problem
                mean = 0
            else:
                mean = float(totalFrequency / totalConnectedTerm)

            SD_Value = deviationCalculation(mean, line[0], neighborsNode)
            coVarience = float(SD_Value / mean)
            total_Covarience = total_Covarience + coVarience
            logFile.write(line[0] + "|" + str(mean) + "|" + str(SD_Value) + "|" + str(coVarience) + "\n")


def filteringGraph1stPhase():
    print("Total Number of Edges Befor Filtering: ", G.number_of_edges())
    with open(MAC_DATA_DIRECTORY + GRAPH_DATA_DIRECTORY + CO_VARIATION_VALUE_FILENAME) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='|')
        for line in csv_reader:
            sourceTerm = line[0]
            co_variation = float(line[3])
            neighbourNode = G[sourceTerm]  # Neighbor node formate {'letters': {'weight': '8.0'}
            unSortedWeightDict = dict()
            for term in neighbourNode:
                breakingWeight = neighbourNode[term]
                for weight in breakingWeight:
                    unSortedWeightDict[term] = breakingWeight[weight]

            sortedWeight = sorted(unSortedWeightDict.items(), key=operator.itemgetter(1),
                                  reverse=True)  # sortedWeight now is a touple not a dictonary
            sortedWeightDict = dict(sortedWeight)
            # Using next() + iter()
            # Getting first key in dictionary
            firstKey = next(iter(sortedWeightDict))
            topValue = float(sortedWeightDict[firstKey])
            percentageOfWeight = 0
            if co_variation < .10:
                percentageOfWeight = .10
            elif co_variation < .20:
                percentageOfWeight = .20
            elif co_variation < .30:
                percentageOfWeight = .30
            elif co_variation < .40:
                percentageOfWeight = .40
            elif co_variation < .50:
                percentageOfWeight = .50
            elif co_variation < .60:
                percentageOfWeight = .60
            else:
                percentageOfWeight = .70

            cutOffPoint = topValue * percentageOfWeight
            for term in sortedWeightDict:
                if float(sortedWeightDict[term]) < cutOffPoint:
                    G.remove_edge(sourceTerm, term)
                # print("Edge Remove From", sourceTerm , " --- ", term)
    print("Total Number of Edges Befor Filtering: ", G.number_of_edges())


# Python program to illustrate the intersection
# of two lists using set() method
def intersection(lst1, lst2):
    return list(set(lst1) & set(lst2))


def dictonaryForHigherLevelCommunity():
    hLevelCommunityCandidateList = []
    COMMUNITY_NUMBER = 1
    with open(MAC_DATA_DIRECTORY + GRAPH_DATA_DIRECTORY + ZSCORE_SORTED_FILENAME) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='|')
        termNumber = 0
        for line in csv_reader:
            if termNumber == TOP_ZSCORE_TERM_NUMBER:
                break
            else:
                hLevelCommunityCandidateList.append(line[0])
                termNumber = termNumber + 1

    for sourceterm in hLevelCommunityCandidateList:
        sourceTermNeighbours = list(G.neighbors(sourceterm))
        sourceSet = set(sourceTermNeighbours)
        for targetTerm in hLevelCommunityCandidateList:
            if sourceterm == targetTerm:
                continue
            else:
                targetTermNeighbours = list(G.neighbors(targetTerm))
                targetSet = set(targetTermNeighbours)
                commonTermSet = sourceSet.intersection(targetSet)
                unionTermSet = sourceSet.union(targetSet)
                commonWeight = 0
                for item in commonTermSet:
                    commonWeight= commonWeight + int(G[sourceterm][item]['weight']) #From Source or target doesn'tmatter. Intersection

                unionWeight = 0
                for item in unionTermSet:
                    try:
                        tempWeight = int(G[sourceterm][item]['weight'])
                    except KeyError:
                        tempWeight = int(G[targetTerm][item]['weight']) #Taget terms neighbor which is not common with source term

                    unionWeight = unionWeight + tempWeight


                #Now Get the ration of connection
                percentageOfCommonTermSet = commonWeight/unionWeight
                #percentageOfCommonTermSet = len(commonTermSet) / len(unionTermSet)

                if percentageOfCommonTermSet >= CO_EFFICIENT_FOR_COMMUNITY_JOIN:
                    if sourceterm in hLevelCommunityNumberDict:
                            tempCommunityNumber = hLevelCommunityNumberDict[sourceterm]
                            hLevelCommunityNumberDict[targetTerm] = tempCommunityNumber
                    elif targetTerm in hLevelCommunityNumberDict:
                            tempCommunityNumber = hLevelCommunityNumberDict[targetTerm]
                            hLevelCommunityNumberDict[sourceterm] = tempCommunityNumber

                    else:
                        hLevelCommunityNumberDict[sourceterm] = COMMUNITY_NUMBER
                        hLevelCommunityNumberDict[targetTerm] = COMMUNITY_NUMBER
                        COMMUNITY_NUMBER = COMMUNITY_NUMBER + 1

                    print(sourceterm, " INTERSECTION WEIGHT ", targetTerm, " is ", commonWeight, " UNION WEIGHT", unionWeight,
                              " PercentageOFSharedTerm: ", percentageOfCommonTermSet, "%")


    #Give separete community number for those who didn't get any community number
    for item in hLevelCommunityCandidateList:
        if item in hLevelCommunityNumberDict:
            continue
        else:
            hLevelCommunityNumberDict[item] = COMMUNITY_NUMBER
            COMMUNITY_NUMBER = COMMUNITY_NUMBER + 1

    writeHLevelClusterTermToFile(hLevelCommunityNumberDict)
    higherLevelCommunityBaseStructure(hLevelCommunityNumberDict)

def writeHLevelClusterTermToFile(hdict):
    fileWrite = open(MAC_DATA_DIRECTORY + RANGE_DATA_DIRECTORY + TOP_CLUSTER_TERM_DATA_FILENAME, "w")

    for key,value in hdict.items():
        fileWrite.write(key + "|" + str(value) + "\n")
    fileWrite.close()

def higherLevelCommunityBaseStructure(higherLevelCommunityDict):
    sortedHighLevelTermByCommunityNumber = sorted(higherLevelCommunityDict.items(), key=operator.itemgetter(1),
                                                  reverse=True)
    sortedHighLevelTermByCommunityNumberDict = dict(sortedHighLevelTermByCommunityNumber)

    print("=======Higher Level Community Structure========")
    print(sortedHighLevelTermByCommunityNumberDict)

    tempItemList = []

    # Using keys() + list()
    # Getting first key in dictionary
    firstKey = list(sortedHighLevelTermByCommunityNumberDict.keys())[0] #Access first entry , aka the total number of community
    totalNumberOfCommunity = sortedHighLevelTermByCommunityNumberDict[firstKey]

    #Create all the community and keep those in hashmap
    for i in range(1,totalNumberOfCommunity+1):
        tempGraph = nx.DiGraph()
        communityGraphHashMap[i] = [tempGraph]

    tempOrderedCommunityValue = totalNumberOfCommunity
    for key, value in sortedHighLevelTermByCommunityNumberDict.items():
        #print(key, value)
        if value == tempOrderedCommunityValue:

            #graph.add_node(key)
            tempItemList.append(key)
            #print(graph)
            #communityGraphHashMap[value] = graph


        else:
            listValue = communityGraphHashMap[tempOrderedCommunityValue] #Value change. So take the temp order value

            graph = listValue[0]
            for item in tempItemList:
                graph.add_node(item)


            for sourceItem in tempItemList:
                for targetItem in tempItemList:
                    if sourceItem == targetItem:
                        continue
                    else:
                        edgeValueDict = G.get_edge_data(sourceItem, targetItem)
                        # If original graph didn't contain any edge for two nodes
                        if edgeValueDict is not None:
                            weightVal = edgeValueDict['weight']
                            graph.add_edge(sourceItem, targetItem, weight=weightVal)
            communityGraphHashMap[tempOrderedCommunityValue] = graph #Insert the graph to the hashMap
            tempOrderedCommunityValue -= 1 #Finally Reduce the value
            # Now empty the list. Then add the current Node.
            tempItemList = []
            tempItemList.append(key)
            #graph.clear()

    listValue = communityGraphHashMap[value] #Not tempOrderedCommunityValue as it is zero. Last valid value is one.
    graph = listValue[0]
    for item in tempItemList:
        graph.add_node(item)
    #For Last Community this extra line of repeated Code
    for sourceItem in tempItemList:
        for targetItem in tempItemList:
            if sourceItem == targetItem:
                continue
            else:
                edgeValueDict = G.get_edge_data(sourceItem, targetItem)
                if edgeValueDict is not None:  # If original graph didn't contain any edge for two nodes
                    weightVal = edgeValueDict['weight']
                    graph.add_edge(sourceItem, targetItem, weight=weightVal)
    communityGraphHashMap[value] = graph
    #graph.clear()




def coreAddTermsToCommunityFunction(currentTerm):
    rankHashmap = dict()
    passBoolean = False
    # Load Graph from HashMap
    for key, value in communityGraphHashMap.items():
        graph = communityGraphHashMap[key]
        listOfNodes = list(graph.nodes)
        graphNodeSet = set()
        for item in listOfNodes:
            graphNodeSet.update(G[item])

        sourceTermNeighbours = G[currentTerm]
        lowerLevelTermNeighSet = set(sourceTermNeighbours)

        commonTermSet = lowerLevelTermNeighSet.intersection(graphNodeSet)
        commonWeight = 0
        for item in commonTermSet:
            commonWeight = commonWeight + int(G[currentTerm][item]['weight'])
            # From Source or target doesn'tmatter. Intersection

        unionWeight = 0
        for item in lowerLevelTermNeighSet:
            unionWeight = unionWeight + int(G[currentTerm][item]['weight'])
        percentageOfCommonTermSet = commonWeight / unionWeight

        if percentageOfCommonTermSet >= LOWER_LEVEL_CO_EFFICIENT_FOR_COMMUNITY_JOIN:
            rankHashmap[key] = percentageOfCommonTermSet
            passBoolean = True
        else:
            rankHashmap[key] = 0.0

    if passBoolean:
        sortedRankHashMapAsList = sorted(rankHashmap.items(), key=operator.itemgetter(1), reverse=True)
        sortedRankDict = dict(sortedRankHashMapAsList)
        bestCommunityNumber = list(sortedRankDict.keys())[0]
        graph = communityGraphHashMap[bestCommunityNumber] #LOAD BEST community in graph
        listOfBestCommunityNodes = list(graph.nodes) #Load List of nodes for best community

        #Testing Purpose Code Added
        if graph.has_node(currentTerm):
            print("DEBUG","ERROR")

        graph.add_node(currentTerm)

        for item in listOfBestCommunityNodes:
            if G.has_edge(currentTerm, item):
                weightVal = G[currentTerm][item]['weight']
                graph.add_edge(currentTerm, item, weight=weightVal)
            if G.has_edge(item, currentTerm):
                weightVal = G[item][currentTerm]['weight']
                graph.add_edge(item, currentTerm, weight=weightVal)

        communityGraphHashMap[bestCommunityNumber] = graph

    if passBoolean == False and currentTerm not in unabletoConnectCommunity:
        unabletoConnectCommunity.append(currentTerm)

def iterativeWaytoAddTermsInCommunity():
    #Stop Condition
    if len(unabletoConnectCommunity) == 0 and len(markMultipleCommunity) == 0:
        print("All Terms Added")
    else:
        tempMarkList = markMultipleCommunity
        tempUnableList = unabletoConnectCommunity
        for terms in tempMarkList:
            coreAddTermsToCommunityFunction(terms)
        for terms in tempUnableList:
            coreAddTermsToCommunityFunction(terms)

        print("Unable to Find community List:", len(unabletoConnectCommunity))
        print("MarkMultiple Community List:", len(markMultipleCommunity))

    #iterativeWaytoAddTermsInCommunity()

def addTermsToTheCommunity():
    with open(MAC_DATA_DIRECTORY + GRAPH_DATA_DIRECTORY + ZSCORE_SORTED_FILENAME) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='|')
        lineNumber = 1
        for line in csv_reader:
            if lineNumber <= TOP_ZSCORE_TERM_NUMBER:
                lineNumber = lineNumber + 1
                continue
            else:
                currentTerm = line[0]
                coreAddTermsToCommunityFunction(currentTerm)


    print("Unable to Find community List:", len(unabletoConnectCommunity))
    print("MarkMultiple Community List:", len(markMultipleCommunity))

    #iterativeWaytoAddTermsInCommunity()




def hashMapCommunityVisualization(hashmapGraph):
    for item in hashmapGraph:
       # print(item) : Moral of the story: now it is not in list order {1: <networkx.classes.digraph.DiGraph object at 0x1170c1750>]
       graph = hashmapGraph[item]
       #print(graph.number_of_nodes())
       nx.draw(graph, with_labels=True)
       plt.savefig("Topic-Model/Data/Images/"+str(item))
       plt.clf()




def visualizeCommunity(vGraph):
    nx.draw(vGraph, with_labels=True)
    plt.savefig("Topic-Model/Data/Images/SmallCommunityPicture")



def recognizeCommunity(G):
    nx.draw(G, with_labels=True)
    plt.savefig("Topic-Model/Data/Images/CommunityPicture")

def writingClusterToFile():
    for key,value in communityGraphHashMap.items():
        file = open(MAC_DATA_DIRECTORY + COMMUNITY_DATA_DIRECTORY + str(key) + ".txt", "w+")
        graph = communityGraphHashMap[key]
        listOfNodes = list(graph.nodes)
        print(listOfNodes)
        for item in listOfNodes:
            file.write(item + "\n")


def loadSortedZScoreforAssocaition():
    with open(MAC_DATA_DIRECTORY + GRAPH_DATA_DIRECTORY + ZSORE_SORTED_BY_ASSO_FILENAME) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='|')
        for line in csv_reader:
            zScoreAssocationDict[line[0]] = line[1]

def sapmlingFromCommunity():

    # Load Graph from HashMap
    for key, value in communityGraphHashMap.items():
        graph = communityGraphHashMap[key]
        listOfNodes = list(graph.nodes)
        communityRankedDict = dict()
        for item in listOfNodes:
            communityRankedDict[item] = zScoreAssocationDict[item]
        sortedRankHashMapAsList = sorted(communityRankedDict.items(), key=operator.itemgetter(1), reverse=True)


        length = len(sortedRankHashMapAsList)
        listOfNodesCoverSet = set()
        dataSetCoverStatistics = dict()
        for i in range(0, length, 1):
            if i !=0 and i%SAMPLING_TERM_COLLECTION_NUMBER == 0:
                percentageOfCover = len(listOfNodesCoverSet)/length
                dataSetCoverStatistics[i] = percentageOfCover
            else:
                toupleTerm = sortedRankHashMapAsList[i]
                listOfNodesCoverSet.add(toupleTerm[0]) #Add one item
                neighboursList = graph[toupleTerm[0]]
                listOfNodesCoverSet.update(neighboursList) #Add multiple item


        file = open(MAC_DATA_DIRECTORY + SAMPLING_STATISTICS_DIRECTORY + str(key) + ".txt", "w+")
        for key,value in dataSetCoverStatistics.items():
            file.write(str(key) + "|" + str(value) + "\n")









def main_Graph_Building_function():
    print("=====Building Graph From Text Data=====")
    building_graph_from_text_data()
    print("=======Writing Co_Varience Value To File======")
    co_Variation()
    print("=======1st Phase Fitering=====")
    filteringGraph1stPhase()
    print("======Visualization=========")
    # export_Graph_to_Gephi_format()
    #recognizeCommunity(G)
    dictonaryForHigherLevelCommunity()
    print("======VisulazileLocalCommunity=====")
    hashMapCommunityVisualization(communityGraphHashMap)
    print("======Adding Term to Community======")
    addTermsToTheCommunity()
    print("======After Adding Terms to The Community Visualizatin=======")
    hashMapCommunityVisualization(communityGraphHashMap)
    print("=======Writing Data to Community File=======")
    writingClusterToFile()
    print("========Sampling Method Started======")
    loadSortedZScoreforAssocaition()
    sapmlingFromCommunity()



main_Graph_Building_function()
