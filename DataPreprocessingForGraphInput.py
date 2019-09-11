import csv
import re


index_dictonary = dict()
#This function reads the text file line by line. For each line it selects term from first input (input 0)
def source_term_separtor():
    with open('/home/C00408440/ZWorkStation/JournalVersion/Data/IndexData/Index.txt') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='|')
        lineNumber=0
        for line in csv_reader:
            lineNumber = lineNumber +1
            if lineNumber == 1000:
                break
            for i in range(len(line)):
                if i == 0:
                    sourceTerm = line[i]
                else:
                    sourceFile=re.search("txt$",line[i])
                    if sourceFile is not None:
                        i+=1
                        add_targetFile_to_sourceFile(sourceTerm,sourceFile.string,line[i])




#This function takes Term, and sourceFile that needs to match with whole index.
#Then it has the target File with source term file frequency which is the basic of building graph unit
def add_targetFile_to_sourceFile(sourceTerm,sourceFile,frequency):
    print("Data Processing for: " + sourceTerm)
    with open('/home/C00408440/ZWorkStation/JournalVersion/Data/IndexData/Index.txt') as csv_file:
        csv_reader_targetFile = csv.reader(csv_file, delimiter='|')
        for line in csv_reader_targetFile:
            for i in range(len(line)):
                    if line[i]==sourceTerm:
                        break
                    targetFile=re.search("txt$",line[i])
                    if targetFile is not None and sourceFile == targetFile.string:
                        targetTerm=line[0]
                        if sourceTerm in index_dictonary:
                            oldKeyValue = index_dictonary[sourceTerm]
                            oldKeyValue[targetTerm] = frequency
                            index_dictonary[sourceTerm] = oldKeyValue
                        else:
                            target_dictonary = {targetTerm: frequency}
                            index_dictonary[sourceTerm]=target_dictonary
                        #print("SourceTerm: " + sourceTerm + " Target Term: " + line[0] + " Match File:" + targetFile.string + " Frequency: " + frequency)


def print_Dictonary():
    for key in index_dictonary:
        tempDict = index_dictonary[key]
        for k,v in tempDict.items():
            print(k,tempDict[k])
        #print(key)
        #print(index_dictonary[key])

def writeGraphDataToFile():
    graphDatainputFile= open("/home/C00408440/ZWorkStation/JournalVersion/Data/GraphData/GraphInputData.txt","w")
    for key in index_dictonary:
        print("Writing Data For: " + key)
        graphDatainputFile.write(key)
        tempDict=index_dictonary[key]
        for k,v in tempDict.items():
            graphDatainputFile.write("|"+k+"|"+v)
        graphDatainputFile.write("\n")



def main_preprocess_function():
    source_term_separtor()
    writeGraphDataToFile()
  #  print_Dictonary()

main_preprocess_function()

