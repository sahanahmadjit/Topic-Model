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


coVaraitionValueRange={
    'identicalRangeOne':.10,
    'identicalRangeTwo':.20,
    'identicalRangeThree':.30,

    'mediumDiffRangeOne':.50,
    'mediumDiffRangeTwo':.70,

    'spredingRangeOne':.80,
    'spreadingRangeTwo':.90}

CO_EFFICIENT_FOR_COMMUNITY_JOIN = .25
global COMMUNITY_NUMBER
TOP_ZSCORE_TERM_NUMBER = 10
CO_EFFICIENT = 1



MAC_DATA_DIRECTORY = "/ZResearchCode/HTopicModel/Topic-Model/Data/"
linux_data_directory = "/home/C00408440/ZWorkStation/JournalVersion/Data/"
GRAPH_DATA_DIRECTORY = "GraphData/"
GRAPH_INPUT_DATA_FILENAME = "GraphInputData_NewsGroup.txt"
ZSCORE_SORTED_FILENAME = "zScoreSorted_NEWSGROUP.txt"
GEPHI_FORMAT_GRAPH_FILENAME = "gephi_format_graph_NEWSGROUP.gexf"
GEPHI_FORMAT_LOWER_LEVEL_COMMUNITY_GRAPH_FILENAME = "gephi_format_LowerCommunityGraph_NEWSGROUP.gexf"
LOWER_LEVEL_CONNECTIVITY_LOGFILE = "LowerConnectivityLogFile_NEWSGROUP.txt"
SAMPLING_FILENAME = "SamplingFile_Test"
EDGE_REMOVE_LIST_LOGFILE = "LowerLevelEdgeRemovalLogFile_NEWSGROUP.txt"
ZSCORE_REVERSE_SORTED_FILENAME = "ZREVERSE_SORTED_NEWSGROUP.txt"
CO_VARIATION_VALUE_FILENAME = "CO_VARIATION_VALUE_NEWSGROUP.txt"

G = nx.DiGraph()
zScore_G = nx.DiGraph()

finalDictonaryCommunity = dict()
zScoreFinalDictonaryCommunity = dict()
nonOverlappingFinalDictonaryCommunity = dict()
communityTrackingDict = dict()
higherLevelCommunityDict = dict()



def export_Graph_to_Gephi_format():
  nx.write_gexf(G,MAC_DATA_DIRECTORY+GRAPH_DATA_DIRECTORY + GEPHI_FORMAT_GRAPH_FILENAME)
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
    if len(neighborsNode) == 0: #avoid devision by zero problem
        meanDeviation = 0
        standardDeviation = 0
    else:
        meanDeviation = meanDeviationSummation / len(neighborsNode)
        standardDeviation = math.sqrt(standardDeviationSummation / len(neighborsNode))
    return standardDeviation


def co_Variation():
    print("Mean Value= mean *" , CO_EFFICIENT)
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
            if totalConnectedTerm == 0: #avoid division by zero problem
                mean = 0
            else:
                mean = float(totalFrequency / totalConnectedTerm)

            SD_Value = deviationCalculation(mean, line[0], neighborsNode)
            coVarience = float(SD_Value/mean)
            total_Covarience = total_Covarience + coVarience
            logFile.write(line[0] + "|" + str(mean) + "|" + str(SD_Value) +"|" + str(coVarience) +"\n")


def co_Variation():
    print("Mean Value= mean *" , CO_EFFICIENT)
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
            if totalConnectedTerm == 0: #avoid division by zero problem
                mean = 0
            else:
                mean = float(totalFrequency / totalConnectedTerm)

            SD_Value = deviationCalculation(mean, line[0], neighborsNode)
            coVarience = float(SD_Value/mean)
            total_Covarience = total_Covarience + coVarience
            logFile.write(line[0] + "|" + str(mean) + "|" + str(SD_Value) +"|" + str(coVarience) +"\n")


def filteringGraph1stPhase():
    print("Total Number of Edges Befor Filtering: ", G.number_of_edges())
    with open(MAC_DATA_DIRECTORY + GRAPH_DATA_DIRECTORY +  CO_VARIATION_VALUE_FILENAME) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='|')
        for line in csv_reader:
            sourceTerm = line[0]
            co_variation= float(line[3])
            neighbourNode = G[sourceTerm] #Neighbor node formate {'letters': {'weight': '8.0'}
            unSortedWeightDict = dict()
            for term in neighbourNode:
                 breakingWeight = neighbourNode[term]
                 for weight in breakingWeight:
                     unSortedWeightDict[term] = breakingWeight[weight]

            sortedWeight = sorted(unSortedWeightDict.items(), key=operator.itemgetter(1),reverse= True)  # sortedWeight now is a touple not a dictonary
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
                    G.remove_edge(sourceTerm,term)
                #print("Edge Remove From", sourceTerm , " --- ", term)
    print("Total Number of Edges Befor Filtering: ", G.number_of_edges())

# Python program to illustrate the intersection
# of two lists using set() method
def intersection(lst1, lst2):
    return list(set(lst1) & set(lst2))

def highLevelBaseCommunityStructure():
    higeherLevelCommunityList = []
    COMMUNITY_NUMBER = 0
    with open(MAC_DATA_DIRECTORY + GRAPH_DATA_DIRECTORY + ZSCORE_SORTED_FILENAME) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='|')
        termNumber = 0
        for line in csv_reader:
            if termNumber == TOP_ZSCORE_TERM_NUMBER:
                break
            else:
                higeherLevelCommunityList.append(line[0])
                termNumber = termNumber + 1

    hightLevelNeighbourList = []
    for sourceterm in higeherLevelCommunityList:
        sourceTermNeighbours = G[sourceterm]
        for targetTerm in higeherLevelCommunityList:
            if sourceterm == targetTerm:
                continue
            else:
                targetTermNeighbours = G[targetTerm]
                commonTermSet = set(sourceTermNeighbours) & set(targetTermNeighbours)
                unionTermSet = set(sourceTermNeighbours) or set(targetTermNeighbours)
                percentageOfCommonTermSet = len(commonTermSet)/len(unionTermSet)
                if percentageOfCommonTermSet>= CO_EFFICIENT_FOR_COMMUNITY_JOIN:
                    if sourceterm in higherLevelCommunityDict:
                        tempCommunityNumber = higherLevelCommunityDict[sourceterm]
                        higherLevelCommunityDict[targetTerm] = tempCommunityNumber

                    else:
                        higherLevelCommunityDict[sourceterm] = COMMUNITY_NUMBER
                        higherLevelCommunityDict[targetTerm] = COMMUNITY_NUMBER
                        COMMUNITY_NUMBER = COMMUNITY_NUMBER + 1
                        print(sourceterm, " match number with ", targetTerm, " is ", len(commonTermSet),
                              " PercentageOFSharedTerm: ", percentageOfCommonTermSet, "%")



    for k,v in higherLevelCommunityDict.items():
        print(k,v)

def



def recognizeCommunity():
    nx.draw(G, with_labels=True)
    plt.show()



def main_Graph_Building_function():
    print("=====Building Graph From Text Data=====")
    building_graph_from_text_data()
    print("=======Writing Co_Varience Value To File======")
    co_Variation()
    print("=======1st Phase Fitering=====")
    filteringGraph1stPhase()
    print("======Visualization=========")
    #export_Graph_to_Gephi_format()
    recognizeCommunity()
    highLevelBaseCommunityStructure()


main_Graph_Building_function()