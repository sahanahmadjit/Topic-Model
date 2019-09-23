import csv
import math

mac_data_directory= "/zWorkStation/JournalWork/Topic-Model/Data/"
linux_data_directory="/home/C00408440/ZWorkStation/JournalVersion/Data/"

zDictPreprocess = dict()
frequencyMean= 0.0
associationMean=0.0
totalNumberOfTerm=0

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


def meanCallculation(frequencyMean,associationMean,totalNumberOfTerm):
      with open(linux_data_directory + 'GraphData/FrequencyAssociationInfo_test.txt') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='|')

        for line in csv_reader:
          frequencyMean = frequencyMean + int(line[2])
          associationMean = associationMean + int(line[4])
          totalNumberOfTerm=totalNumberOfTerm+1

        frequencyMean=frequencyMean/totalNumberOfTerm
        associationMean=associationMean/totalNumberOfTerm
        totalNumberOfTerm=totalNumberOfTerm
      return frequencyMean,associationMean,totalNumberOfTerm


def statisticalInfoWriteToFile(freq,assiocation,total):
  statisticalWrite=open(linux_data_directory + "GraphData/StatisticalInfo_test.txt", "w")
  statisticalWrite.write("MeanFrequency"+"|" + str(freq)+ "|" + "MeanAssociation"+ "|" + str(assiocation) +"|"+"Total Number of Term"+"|"+str(total))

def deviationInfoWriteToFile(freqDeviation,associationDevaition):
  statisticalWrite=open(linux_data_directory + "GraphData/StatisticalInfo_test.txt", "a")
  statisticalWrite.write("\n")
  statisticalWrite.write("SD_Frequency"+"|" + str(freqDeviation)+ "|" + "SD_Association"+ "|" + str(associationDevaition))

def calculateStandardDeviation(meanFrequency,meanAssociation,totalNumberOfTerm):
  with open(linux_data_directory + 'GraphData/FrequencyAssociationInfo_test.txt') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter='|')
    summationFrequencyDeviation=0.0
    summationAssociaionDevaition=0.0
    for line in csv_reader:
      frequencyDeviation = float(line[2]) - meanFrequency
      associaionDevaition =float(line[4]) - meanAssociation
      frequencyDeviation = math.pow(frequencyDeviation,2)
      associaionDevaition = math.pow(associaionDevaition,2)
      summationFrequencyDeviation+= frequencyDeviation
      summationAssociaionDevaition+=associaionDevaition

    summationFrequencyDeviation /= totalNumberOfTerm
    summationAssociaionDevaition/=totalNumberOfTerm
    summationFrequencyDeviation=math.sqrt(summationFrequencyDeviation)
    summationAssociaionDevaition=math.sqrt(summationAssociaionDevaition)
  return summationFrequencyDeviation,summationAssociaionDevaition



def main_ZScore():
  createZScoreFormatData()
  print_Dictonary()
  #writeFrequencyAssociationToFile()
  statiscalInfo=meanCallculation(frequencyMean,associationMean,totalNumberOfTerm)
  statisticalInfoWriteToFile(statiscalInfo[0],statiscalInfo[1],statiscalInfo[2])
  statiscalInfo =calculateStandardDeviation(statiscalInfo[0],statiscalInfo[1],statiscalInfo[2])
  deviationInfoWriteToFile(statiscalInfo[0],statiscalInfo[1])

main_ZScore()