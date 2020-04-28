import csv
import re



MAC_DATA_DIRECTORY= "/ZResearchCode/HTopicModel/Topic-Model/Data/"
linux_data_directory="/home/C00408440/ZWorkStation/JournalVersion/Data/"
INDEX_FILE_DIRECTORY = "IndexData/"
RANGE_DATA_DIRECTORY = "ClusterRange/"
CLUSTER_RANGE_DATA_FILENAME= "NEWSGROUP_RANGE.txt"
INDEX_FILE_NAME = "Index_NewsGroup.txt"



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
                    wordAssignmentInTopic[key]= 1

    print(wordAssignmentInTopic)









def selectTermForClassification():
    with open(MAC_DATA_DIRECTORY + INDEX_FILE_DIRECTORY + INDEX_FILE_NAME) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='|')



def mainClassificationVerifcationFunction():
    wordTopicNameBasedOnFileRange("experience")


mainClassificationVerifcationFunction()