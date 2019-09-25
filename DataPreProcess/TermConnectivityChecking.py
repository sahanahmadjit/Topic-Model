import csv
import math

mac_data_directory= "/zWorkStation/JournalWork/Topic-Model/Data/"
linux_data_directory="/home/C00408440/ZWorkStation/JournalVersion/Data/"








def findTermDataFromGraphData(sourceTerm,assocaitedTerm):
  with open(linux_data_directory + 'GraphData/GraphInputData.txt') as csv_file:
    csv_reader_targetFile = csv.reader(csv_file, delimiter='|')
    sourceFound=False
    associatedFound=False
    sourceTermFeq=0
    targetTermFeq=0
    for line in csv_reader_targetFile:
      if line[0]==sourceTerm or line[0]==assocaitedTerm:
        if line[0]==sourceTerm:
          for i in range(len(line)):
            if line[i]==assocaitedTerm:
              print(line[0]+"|"+line[i]+"|"+line[i+1])
              sourceTermFeq=int(line[i+1])
              sourceFound=True
        else:
          for i in range(len(line)):
            if line[i] == sourceTerm:
              print(line[0] + "|" + line[i] + "|" + line[i + 1])
              targetTermFeq=int(line[i+1])
              associatedFound=True
        if sourceFound==True and associatedFound==True:
          break;
  return sourceTermFeq,targetTermFeq

def findFrequencyAssociationInformation(sourceTerm,assocaitedTerm):
  with open(linux_data_directory + 'GraphData/FrequencyAssociationInfo.txt') as csv_file:
    csv_reader_targetFile = csv.reader(csv_file, delimiter='|')
    sourceFound=False
    associatedFound=False
    frequencyInfo=findTermDataFromGraphData(sourceTerm,associatedTerm)

    for line in csv_reader_targetFile:
      if line[0]==sourceTerm or line[0]==assocaitedTerm:
        if line[0]==sourceTerm:
              print(line)
              meanValueSource= float(line[2])/float(line[4])
              print("AVG Frequency Mean: " + str(meanValueSource))
              print("SD of Term: "+calculateStandardDeviation(float(frequencyInfo[0]),meanValueSource,float(line[4])))
              sourceFound=True
        else:
          print(line)
          meanValueAssociated = float(line[2]) / float(line[4])
          print("AVG Frequency Mean: "+str(meanValueAssociated))
          print("SD of Term: " + calculateStandardDeviation(float(frequencyInfo[1]), meanValueAssociated, float(line[4])))
          associatedFound=True
        if sourceFound==True and associatedFound==True:

          break;


def findZScoreInformation(sourceTerm,assocaitedTerm):
  with open(linux_data_directory + 'GraphData/zScoreInfo.txt') as csv_file:
    csv_reader_targetFile = csv.reader(csv_file, delimiter='|')
    sourceFound=False
    associatedFound=False
    for line in csv_reader_targetFile:
      if line[0]==sourceTerm or line[0]==assocaitedTerm:
        if line[0]==sourceTerm:
              print(line)
              sourceFound=True
        else:
          print(line)
          associatedFound=True
        if sourceFound==True and associatedFound==True:
          break;

def calculateStandardDeviation(termFrequency,meanFrequency, totalAssociation):

    frequencyDeviation = termFrequency - meanFrequency
    frequencyDeviation = math.pow(frequencyDeviation,2)
    frequencyDeviation /= totalAssociation
    frequencyDeviation=math.sqrt(frequencyDeviation)

    return str(frequencyDeviation)

print("Source Term:")
sourceTerm= input()
print("Associated Term")
associatedTerm =input()
findFrequencyAssociationInformation(sourceTerm,associatedTerm)
findZScoreInformation(sourceTerm,associatedTerm)

