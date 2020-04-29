import csv
import re
import operator
import os
from random import randint



MAC_DATA_DIRECTORY= "/ZResearchCode/HTopicModel/Topic-Model/Data/"
linux_data_directory="/home/C00408440/ZWorkStation/JournalVersion/Data/"
INDEX_FILE_DIRECTORY = "IndexData/"
RANGE_DATA_DIRECTORY = "ClusterRange/"
COMMUNITY_DATA_DIRECTORY = "CommunityData/"
CLUSTER_RANGE_DATA_FILENAME= "NEWSGROUP_MANUAL_ADD_RANGE.txt"
INDEX_FILE_NAME = "Index_NewsGroup.txt"
TOP_CLUSTER_TERM_DATA_FILENAME= "NEWSGROUP_TOP_CLUSTER_TERM.txt"
DATA_SAMPLE_FILENAME= "NEWSGROUP_SAMPLE_DATA_FILENAME"
TOTAL_RANDOM_SAMPLE = 200

communityTermListAsHashMap = dict()
topicAssingmentByCommunityNumberDict = dict()
sampleList = []

def wordTopicNameBasedOnFileRange(word):
    clusterRangeDict = dict()
    fileNumberList = []
    wordAssignmentInTopic = dict()
    #LOAD RANGE FROM FILE
    with open(MAC_DATA_DIRECTORY + RANGE_DATA_DIRECTORY + CLUSTER_RANGE_DATA_FILENAME) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='|')
        for line in csv_reader:
            range_Value = []
            range_Value.append(line[1])
            range_Value.append(line[2])
            clusterRangeDict[line[0]] = range_Value

    with open(MAC_DATA_DIRECTORY + INDEX_FILE_DIRECTORY + INDEX_FILE_NAME) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='|')
        index_line = ""
        for line in csv_reader:
            if line[0] == word:
                index_line = line
                break
            else:
                continue
        for i in range(0,len(index_line)):
            if i == 0:
                continue
            elif i%2 != 0: #to avoid ranking value in index file only take the odd position
                fileNumber = re.split(".txt", index_line[i])
                fileNumberList.append(fileNumber[0])

    for i in fileNumberList:
        i = int(i)
        for key, value in clusterRangeDict.items():
            startRange = int(value[0])
            endRange = int(value[1])
            if i >= startRange and i<=endRange:
                if key in wordAssignmentInTopic:
                    oldValue = wordAssignmentInTopic[key]
                    oldValue = oldValue + 1
                    wordAssignmentInTopic[key] = oldValue
                else:
                    wordAssignmentInTopic[key] = 1

    sortedWordAssignmentinTopicAsList = sorted(wordAssignmentInTopic.items(), key=operator.itemgetter(1), reverse=True)
    sortedDict = dict(sortedWordAssignmentinTopicAsList)
    if len(sortedDict)==0:
        bestTopic= None #Unassignm Term of Topic
    else:
        bestTopic = list(sortedDict.keys())[0]
    #UnBlocked The Code To check the Similair Issue
    #print(word, "->", sortedDict)
    return bestTopic





def hLevelTopicAssignment():
    data = ""
    with open(MAC_DATA_DIRECTORY + RANGE_DATA_DIRECTORY + TOP_CLUSTER_TERM_DATA_FILENAME, "r") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='|')
        for line in csv_reader:
            topic = wordTopicNameBasedOnFileRange(line[0])
            singleLine = line[0] + "|" + str(line[1]) + "|" + topic + "\n"  #term,cluster number, topic
            data += singleLine
            topicAssingmentByCommunityNumberDict[line[1]]=topic

    fileObject = open(MAC_DATA_DIRECTORY + RANGE_DATA_DIRECTORY + TOP_CLUSTER_TERM_DATA_FILENAME, "w")
    fileObject.write(data)


def loadAllCommunityTerm():
    #Load All the CommunityTerm
    for fileName in os.listdir(MAC_DATA_DIRECTORY + COMMUNITY_DATA_DIRECTORY):
        #print("FileName",fileName)
        filePath = os.path.join(MAC_DATA_DIRECTORY + COMMUNITY_DATA_DIRECTORY + fileName)
        #print("Full File Path", filePath)

        with open(filePath) as singleFile:
            listOfTerms = []
            for line in singleFile:
                listOfTerms.append(line.rstrip()) #remove trailing newline by striping

            fileNumber = re.split('.txt',fileName)
            communityTermListAsHashMap[fileNumber[0]] = listOfTerms

    #for key in communityGraphHashMap.items():
        #print(key)




def selectTermForClassification():

    with open(MAC_DATA_DIRECTORY + INDEX_FILE_DIRECTORY + INDEX_FILE_NAME) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='\n')
        totalNumberofLine = 0
        for line in csv_reader:
            totalNumberofLine +=1

        readIndexFile = open( MAC_DATA_DIRECTORY + INDEX_FILE_DIRECTORY + INDEX_FILE_NAME,"r")
        loadIndexFile = readIndexFile.readlines()
        readIndexFile.close()

        totalNumberofLine = totalNumberofLine -1
        for i in range (1,TOTAL_RANDOM_SAMPLE):
            randomLineNumber = randint(1,totalNumberofLine)
            randomLine = loadIndexFile[randomLineNumber]
            sampleList.append(randomLine)

    fileWriter = open(MAC_DATA_DIRECTORY + RANGE_DATA_DIRECTORY + DATA_SAMPLE_FILENAME, "w")
    for item in sampleList:
        fileWriter.write(item)
    fileWriter.close()



def topicAssignmentByModel(word):
    topic = None
    for key,value in communityTermListAsHashMap.items():
        listOFCommunityTerms = communityTermListAsHashMap[key]
        if word in listOFCommunityTerms:
            topic = topicAssingmentByCommunityNumberDict[key]
            break
    return topic





def verification():
    MATCH_COUNT = 0
    UNMATCH_COUNT=0
    with open(MAC_DATA_DIRECTORY + RANGE_DATA_DIRECTORY + DATA_SAMPLE_FILENAME) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='|')

        for line in csv_reader:
            term = line[0]
            #verification by fileRange
            topicByFileRange= wordTopicNameBasedOnFileRange(term)
            #verification by model
            topicByModel = topicAssignmentByModel(term)

            if topicByModel is not None and topicByFileRange is not None:
                if topicByModel == topicByFileRange:
                    MATCH_COUNT +=1
                    #print("MATCH")
                    #print(term + " Topic By File Range: " + topicByFileRange + " Topic By Model: " + topicByModel)
                else:
                    UNMATCH_COUNT +=1
                    #print("NOT MATCH")
                    #print(term + " Topic By File Range: " + topicByFileRange +" Topic By Model: " + topicByModel)

    totalSearch = UNMATCH_COUNT + MATCH_COUNT
    print("Percentage of Accuracy:", MATCH_COUNT/totalSearch)





def mainClassificationVerifcationFunction():
    print("=====Assign Topic Name to Top Terms=====")
    hLevelTopicAssignment()
    loadAllCommunityTerm()
    selectTermForClassification()
    verification()


mainClassificationVerifcationFunction()