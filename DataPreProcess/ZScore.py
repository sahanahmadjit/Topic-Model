import csv
import math
import operator
import matplotlib.pyplot as plt

mac_data_directory= "/zWorkStation/JournalWork/Topic-Model/Data/"
linux_data_directory="/home/C00408440/ZWorkStation/JournalVersion/Data/"

zDictPreprocess = dict()
zScoreDict = dict()
frequencyMean= 0.0
associationMean=0.0
totalNumberOfTerm=0

def createZScoreFormatData():
  for itaration in range(2):
    with open(mac_data_directory + 'GraphData/GraphInputData_Test.txt') as csv_file:
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
  frequencyAssociationDatainputFile = open(mac_data_directory + "GraphData/FrequencyAssociationInfo_Test.txt", "w")
  for key in zDictPreprocess:
    #print("Writing Data For: " + key)
    frequencyAssociationDatainputFile.write(key)
    tempDict = zDictPreprocess[key]
    for k, v in tempDict.items():
      frequencyAssociationDatainputFile.write("|" + k + "|" + str(v))
    frequencyAssociationDatainputFile.write("\n")


def meanCallculation(frequencyMean,associationMean,totalNumberOfTerm):
      with open(mac_data_directory + 'GraphData/FrequencyAssociationInfo_Test.txt') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='|')

        for line in csv_reader:
          frequencyMean = frequencyMean + int(line[2])
          associationMean = associationMean + int(line[4])
          totalNumberOfTerm=totalNumberOfTerm+1

        print("Total Frequency:" + str(frequencyMean))
        print("Total Association:" + str(associationMean))
        frequencyMean=frequencyMean/totalNumberOfTerm
        associationMean=associationMean/totalNumberOfTerm
        totalNumberOfTerm=totalNumberOfTerm
      return frequencyMean,associationMean,totalNumberOfTerm


def statisticalInfoWriteToFile(freq,assiocation,total):
  statisticalWrite=open(mac_data_directory + "GraphData/StatisticalInfo_Test.txt", "w")
  statisticalWrite.write("MeanFrequency"+"|" + str(freq)+ "|" + "MeanAssociation"+ "|" + str(assiocation) +"|"+"Total Number of Term"+"|"+str(total))

def deviationInfoWriteToFile(freqDeviation,associationDevaition):
  statisticalWrite=open(mac_data_directory + "GraphData/StatisticalInfo_Test.txt", "a")
  statisticalWrite.write("\n")
  statisticalWrite.write("SD_Frequency"+"|" + str(freqDeviation)+ "|" + "SD_Association"+ "|" + str(associationDevaition))

def calculateStandardDeviation(meanFrequency,meanAssociation,totalNumberOfTerm):
  with open(mac_data_directory + 'GraphData/FrequencyAssociationInfo_Test.txt') as csv_file:
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

def calculateZScore(meanFreq,SDFreq,meanAsso,SDAsso):
  with open(mac_data_directory + 'GraphData/FrequencyAssociationInfo_Test.txt') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter='|')
    for line in csv_reader:
      zScoreFrequency= (float(line[2])-meanFreq)/SDFreq
      zScoreAssociation= (float(line[4])-meanAsso)/SDAsso
      tempDict = {'zScoreFeq':zScoreFrequency,'zScoreAsso':zScoreAssociation}
      zScoreDict[line[0]]=tempDict

def writeZScore():
  statisticalWrite=open(mac_data_directory + "GraphData/zScoreInfo_Test.txt", "w")
  for key in zScoreDict:
    #print("Writing Data For: " + key)
    statisticalWrite.write(key)
    tempDict = zScoreDict[key]
    for k, v in tempDict.items():
      statisticalWrite.write("|" + k + "|" + str(v))
    statisticalWrite.write("\n")

def sortedZScoreWrite():
  with open(mac_data_directory + 'GraphData/zScoreInfo_Test.txt') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter='|')
    avgZscore = dict()
    avg=0.0
    for line in csv_reader:
      avgZscore[line[0]]= (float(line[2])+float(line[4]))/2

    sortedZScore= sorted(avgZscore.items(),key=operator.itemgetter(1),reverse=True)#sortedZScore now is a touple not a dictonary
    sortedZScoreDict= dict(sortedZScore)

  zScoreSortedWrite=open(mac_data_directory + "GraphData/zScoreSorted_Test.txt", "w")
  for key in sortedZScoreDict:
    #print("Writing Data For: " + key)
    zScoreSortedWrite.write(key+ "|" + str(sortedZScoreDict[key]))
    zScoreSortedWrite.write("\n")

  #Ploting the Graph Uncomment to plot the graph
  '''
  print("Starting Ploting ZScore")
  plt.bar(list(sortedZScoreDict.keys()),sortedZScoreDict.values(),color='g')
  plt.show()
  print("Finished Ploting ZScores")
'''

def sortedZScoreByFrequencyWrite():
  with open(mac_data_directory + 'GraphData/zScoreInfo_Test.txt') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter='|')
    avgZscoreFeq = dict()
    avg=0.0
    for line in csv_reader:
      avgZscoreFeq[line[0]]= float(line[2])

    sortedZScoreFeq= sorted(avgZscoreFeq.items(),key=operator.itemgetter(1),reverse=True)#sortedZScore now is a touple not a dictonary
    sortedZScoreFeqDict= dict(sortedZScoreFeq)

  zScoreSortedWrite=open(mac_data_directory + "GraphData/zScoreSortedByFeq_Test.txt", "w")
  for key in sortedZScoreFeqDict:
    #print("Writing Data For: " + key)
    zScoreSortedWrite.write(key+ "|" + str(sortedZScoreFeqDict[key]))
    zScoreSortedWrite.write("\n")

def sortedZScoreByAssociationWrite():
  with open(mac_data_directory + 'GraphData/zScoreInfo_Test.txt') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter='|')
    avgZscoreAsso = dict()
    avg=0.0
    for line in csv_reader:
      avgZscoreAsso[line[0]]= float(line[4])

    sortedZScoreAsso= sorted(avgZscoreAsso.items(),key=operator.itemgetter(1),reverse=True)#sortedZScore now is a touple not a dictonary
    sortedZScoreAssoDict= dict(sortedZScoreAsso)

  zScoreSortedWrite=open(mac_data_directory + "GraphData/zScoreSortedByAsso_Test.txt", "w")
  for key in sortedZScoreAssoDict:
    #print("Writing Data For: " + key)
    zScoreSortedWrite.write(key+ "|" + str(sortedZScoreAssoDict[key]))
    zScoreSortedWrite.write("\n")

def main_ZScore():
  print("Creating ZScore Format");
  createZScoreFormatData()
  print("Finished Creating ZScore Formats")
  #print_Dictonary()
  print("Writing Frequency Association Info to File")
  writeFrequencyAssociationToFile()
  print("Finished Writing Frequency Association Info to File")
  print("Calculating Mean")
  meanInfo=meanCallculation(frequencyMean,associationMean,totalNumberOfTerm)
  print("Finished Calculating Mean")
  #meanInfo,SD info 0 for Frequency and 1 for Association. Mean info 2 is the total number of term
  print("Writing Mean Info to Statistical File")
  statisticalInfoWriteToFile(meanInfo[0],meanInfo[1],meanInfo[2])
  print("Calculating SD")
  SDInfo =calculateStandardDeviation(meanInfo[0],meanInfo[1],meanInfo[2])
  print("Finished Calculating SD")
  print("Writing SD info to Statistical File")
  deviationInfoWriteToFile(SDInfo[0],SDInfo[1])
  print("Calculating ZScore")
  calculateZScore(meanInfo[0],SDInfo[0],meanInfo[1],SDInfo[1])
  print("Finished Calculating ZScore")
  print("Writing ZScore to File")
  writeZScore()
  print("Finished ZScore to File")
  print("Sorting ZScore to File")
  sortedZScoreWrite()
  print("Finished Sorted ZScore to File")
  print("Writing Sorted ZScore By Frequency to File")
  sortedZScoreByFrequencyWrite()
  print("Finished Writing Sorted ZScore By Frequency to File")
  print("Writing Sorted ZScore By Association to File")
  sortedZScoreByAssociationWrite()
  print("Finished Writing Sorted ZScore By Association to File")



main_ZScore()