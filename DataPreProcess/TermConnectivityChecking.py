import csv


mac_data_directory= "/zWorkStation/JournalWork/Topic-Model/Data/"
linux_data_directory="/home/C00408440/ZWorkStation/JournalVersion/Data/"








def findTermDataFromGraphData(sourceTerm,assocaitedTerm):
  with open(linux_data_directory + 'GraphData/GraphInputData.txt') as csv_file:
    csv_reader_targetFile = csv.reader(csv_file, delimiter='|')
    sourceFound=False
    associatedFound=False
    for line in csv_reader_targetFile:
      if line[0]==sourceTerm or line[0]==assocaitedTerm:
        if line[0]==sourceTerm:
          for i in range(len(line)):
            if line[i]==assocaitedTerm:
              print(line[0]+"|"+line[i]+"|"+line[i+1])
              sourceFound=True
        else:
          for i in range(len(line)):
            if line[i] == sourceTerm:
              print(line[0] + "|" + line[i] + "|" + line[i + 1])
              associatedFound=True
        if sourceFound==True and associatedFound==True:
          break;


def findFrequencyAssociationInformation(sourceTerm,assocaitedTerm):
  with open(linux_data_directory + 'GraphData/FrequencyAssociationInfo.txt') as csv_file:
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



print("Source Term:")
sourceTerm= input()
print("Associated Term")
associatedTerm =input()
findTermDataFromGraphData(sourceTerm ,associatedTerm)
findFrequencyAssociationInformation(sourceTerm,associatedTerm)
findZScoreInformation(sourceTerm,associatedTerm)

