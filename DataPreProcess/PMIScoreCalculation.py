import csv
import re
import operator
import os
from random import randint
import networkx as nx
import math



MAC_DATA_DIRECTORY= "/ZResearchCode/HTopicModel/Topic-Model/Data/"
linux_data_directory="/home/C00408440/ZWorkStation/JournalVersion/Data/"
INDEX_FILE_DIRECTORY = "IndexData/"
RANGE_DATA_DIRECTORY = "ClusterRange/"
COMMUNITY_DATA_DIRECTORY = "CommunityData/"
GRAPH_DATA_DIRECTORY = "GraphData/"
CLUSTER_RANGE_DATA_FILENAME= "NEWSGROUP_MANUAL_ADD_RANGE.txt"
GRAPH_INPUT_DATA_FILENAME = "GraphInputData_NewsGroup.txt"
INDEX_FILE_NAME = "Index_NewsGroup.txt"
TOP_CLUSTER_TERM_DATA_FILENAME= "NEWSGROUP_TOP_CLUSTER_TERM.txt"
DATA_SAMPLE_FILENAME= "NEWSGROUP_SAMPLE_DATA_FILENAME"
TOTAL_RANDOM_SAMPLE = 100
SINGLE_CLUSTER_RANDOM_SAMPLE = 10

sampleList = []
G = nx.DiGraph()
indexDict = dict()
def loadTheGraphFromTextFile():
    for itaration in range(2):
        with open(MAC_DATA_DIRECTORY + GRAPH_DATA_DIRECTORY + GRAPH_INPUT_DATA_FILENAME) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter='|')
            for line in csv_reader:
                if itaration == 0:
                    G.add_node(line[0])
                    continue
                else:
                    for i in range(1, len(line),2):  # 1:Starting from 2nd term {first term is source}, stop, increment by 2
                        G.add_edge(line[0], line[i], weight=line[i + 1])


def loadIndexFileFromTextFile():
    with open(MAC_DATA_DIRECTORY + INDEX_FILE_DIRECTORY + INDEX_FILE_NAME) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter = '|')
        for line in csv_reader:
            docList = []
            for item in range(1,len(line)):
                if item%2!=0:
                    fileNumber = re.sub('.txt',"",line[item])
                    docList.append(fileNumber)
                else:
                    docList.append(line[item])
            indexDict[line[0]] = docList #key is the term





def PMICoreScoreCalculationBase(x,y):
    xFileRank = indexDict[x]
    yFileRank = indexDict[y]
    xSet = set()
    ySet = set()
    xWeight = 0
    yWeight = 0
    for i in range(0,len(xFileRank)):
        if i%2==0:
            xSet.add(xFileRank[i])
        else:
            xWeight = xWeight + int(xFileRank[i])

    for i in range(0,len(yFileRank)):
        if i%2== 0:
            ySet.add(yFileRank[i])
        else:
            yWeight = yWeight + int(yFileRank[i])
    intersection = xSet.intersection(ySet)
    unionWeight = xWeight + yWeight

    intersectionWeight = 0
    for item in intersection:
        fileIndex = xFileRank.index(item)
        intersectionWeight = intersectionWeight + int(xFileRank[fileIndex+1])

    pOfX = xWeight/unionWeight
    pofY = yWeight/unionWeight
    pOfIntersection = intersectionWeight/unionWeight

    score = pOfIntersection/(pOfX*pofY)
    PMIScore = math.log2(score)

    return  PMIScore










def PMIScoreOfSampleList():
    PMIScor = 0
    for i in range(0,len(sampleList),2):
        x=sampleList[i]
        y=sampleList[i+1]
        scoreOne= PMICoreScoreCalculationBase(x,y)
        scoreTwo = PMICoreScoreCalculationBase(y,x)

        if scoreOne > scoreTwo:
            PMIScor = PMIScor + scoreOne
        else:
            PMIScor = PMIScor + scoreTwo

    print("===========PMI Score==========")
    totalCase = len(sampleList)/2
    print(PMIScor/totalCase)







def createSampleList():
    # Load All the CommunityTerm
    for fileName in os.listdir(MAC_DATA_DIRECTORY + COMMUNITY_DATA_DIRECTORY):
        #print("FileName",fileName)
        filePath = os.path.join(MAC_DATA_DIRECTORY + COMMUNITY_DATA_DIRECTORY + fileName)
        #print("Full File Path", filePath)

        lineNumber = 0
        clusterTerm = []

        with open(filePath) as csv_file:

            csv_reader = csv.reader(csv_file, delimiter='\n')
            for line in csv_reader:
                clusterTerm.append(line[0])
                lineNumber +=1

        readIndexFile = open(MAC_DATA_DIRECTORY + COMMUNITY_DATA_DIRECTORY + fileName, "r")
        loadIndexFile = readIndexFile.readlines()
        readIndexFile.close()

        lineNumber = lineNumber - 1
        for i in range(1, SINGLE_CLUSTER_RANDOM_SAMPLE):
            randomLineNumber = randint(1, lineNumber)
            x = loadIndexFile[randomLineNumber]
            x = x.rstrip() #Removing tailing newline
            neigboutofX = G[x]
            for key, value in neigboutofX.items():
                if key in clusterTerm:
                    sampleList.append(x) #X found
                    sampleList.append(key)# Y found
                    break

def PMI_main():
    loadIndexFileFromTextFile()
    loadTheGraphFromTextFile()
    createSampleList()
    PMIScoreOfSampleList()



PMI_main()
