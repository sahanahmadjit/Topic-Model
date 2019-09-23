import csv
import networkx as nx

mac_data_directory= "/zWorkStation/JournalWork/Topic-Model/Data/"
linux_data_directory="/home/C00408440/ZWorkStation/JournalVersion/Data/"

zDictPreprocess = dict()
def createZScoreFormatData():
  for itaration in range(2):
    with open(linux_data_directory + 'GraphData/GraphInputData_Test.txt') as csv_file:
      csv_reader = csv.reader(csv_file, delimiter='|')
      for line in csv_reader:
        tempDictForFrqAssociation = dict()
        tempDictForFrqAssociation ={'frequency':0,'association':0}
        term=line[0]
        for i in range(1,len(line),2): # 1:Starting from 2nd term {first term is source}, stop, increment by 2
            tempDictForFrqAssociation['frequency']= int(tempDictForFrqAssociation['frequency']+int(line[i+1]))
            tempDictForFrqAssociation['association']=int(tempDictForFrqAssociation['association']+1)
        zDictPreprocess[term]=tempDictForFrqAssociation

def print_Dictonary():
  for key in zDictPreprocess:
    tempDict = zDictPreprocess[key]
    print(key)
    for k, v in tempDict.items():
      print(k, tempDict[k])

def writeFrequencyAssociationToFile():
  frequencyAssociationDatainputFile = open(linux_data_directory + "GraphData/FrequencyAssociationInfo_test.txt", "w")
  for key in zDictPreprocess:
    print("Writing Data For: " + key)
    frequencyAssociationDatainputFile.write(key)
    tempDict = zDictPreprocess[key]
    for k, v in tempDict.items():
      frequencyAssociationDatainputFile.write("|" + k + "|" + str(v))
    frequencyAssociationDatainputFile.write("\n")


def main_ZScore():
  createZScoreFormatData()
  print_Dictonary()
  writeFrequencyAssociationToFile()


main_ZScore()