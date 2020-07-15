from nltk.corpus import stopwords
import os
import re
from collections import Counter
import spacy
import pytextrank
import en_core_web_sm

MAC_DATA_DIRECTORY = "/ZResearchCode/HTopicModel/Topic-Model/Data/"
BROWN_INDEX_DIRECTORY = "IndexData/"
BROWN_INDEX_FILENAME = "Index_NewsGroup.txt"
BROWN_DATA_FOLDER= "brown/"
NUMBER_OF_TERMS_EXTRACTED_FROM_DOCUMENT = 10

# Load English tokenizer, tagger, parser, NER and word vectors
nlp = spacy.load("en_core_web_sm")
# add PyTextRank to the spaCy pipeline
tr = pytextrank.TextRank()
nlp.add_pipe(tr.PipelineComponent, name="textrank", last=True)

stopWordsListManual = ['subject']



def dataPreprocess(path):
    print("Process Start:")
    folders = []
    for r, d, f in os.walk(path):
        for folder in d:
            folders.append(os.path.join(r, folder))
    for folderName in folders:
        print("Processing Folder: "+folderName)
        # print("Folder Location", folderName)
        for files in os.listdir(folderName):
            print("FileName",files)
            filepath = os.path.join(folderName, files)
            print("Full File Path", filepath)
            file_read = open(filepath, "r", encoding="iso-8859-1")
            text = file_read.read().lower()
            replace_ForwardSlash_Doc = re.sub(r'/[a-z]*','',text)
            replace_Dash_doc = re.sub(r'-[a-z]*','', replace_ForwardSlash_Doc)
            file_read.close()
            file_write = open(filepath,"w",encoding="iso-8859-1")
            file_write.write(replace_Dash_doc)
            file_write.close()


def renameFileinFolder(path):
    print("Process Start:")
    folders = []
    fileNumber = 1
    for r, d, f in os.walk(path):
        for folder in d:
            folders.append(os.path.join(r, folder))
    for folderName in folders:
        print("Processing Folder: " + folderName)
        # print("Folder Location", folderName)
        for files in os.listdir(folderName):
            print("FileName", files)
            newFileName = str(fileNumber) + '.txt'
            filepath = os.path.join(folderName, files)
            newFilePath = os.path.join(folderName,newFileName)
            print("Full File Path", filepath)
            print("newFilePath", newFilePath)
            os.rename(filepath, newFilePath)
            fileNumber = fileNumber + 1

def readAllFilesFromSourceFolder(path):
    print("============Extracting Document for Keywords========")
    folders = []
    rankedSinglePharesDict = dict()
    rankedMultiplePharesDict = dict()
    # r=root, d=directories, f = files

    stopWordsList = set(stopwords.words('english'))
    for r, d, f in os.walk(path):
        for folder in d:
            folders.append(os.path.join(r, folder))
    for folderName in folders:
        print("Processing Folder: "+folderName)
        # print("Folder Location", folderName)
        for files in os.listdir(folderName):
            # print("FileName",files)
            filepath = os.path.join(folderName, files)
            #print("Full File Path", filepath)
            sample_file = open(filepath, "r", encoding="iso-8859-1")
            text = sample_file.read().lower()
            doc = nlp(text)

            # examine the top-ranked phrases in the document
            numberOfTermsExtractedFromDocuments = 0
            RANKED_POINT = 2*NUMBER_OF_TERMS_EXTRACTED_FROM_DOCUMENT
            for phares in doc._.phrases:
                if numberOfTermsExtractedFromDocuments == NUMBER_OF_TERMS_EXTRACTED_FROM_DOCUMENT:
                    break
                splitbySpace = re.split('\s+', str(phares))  # split the sentence by space
                filterWord = []
                for word in splitbySpace:
                    removeSpace= word.strip()
                    if removeSpace.isalpha():  # check the word contains only letter
                        if removeSpace.lower() not in stopWordsList:  # Remove Stop Word from List
                                if removeSpace.lower() not in stopWordsListManual:
                                    filterWord.append(removeSpace)

                if len(filterWord)== 0: #if no meaningful word look for the next one
                    continue
                if len(filterWord) == 1:
                    if filterWord[0] in rankedSinglePharesDict:
                        oldValue = rankedSinglePharesDict[filterWord[0]]
                        rankedSinglePharesDict[filterWord[0]] = oldValue + "|" + files+ ".txt" + "|" + str(RANKED_POINT)
                    else:
                        rankedSinglePharesDict[filterWord[0]] = files +".txt" + "|" + str(RANKED_POINT)
                else:
                    itr = 0
                    pharesAddWithSpace = ""
                    for words in filterWord:
                        if itr == 0:
                            pharesAddWithSpace = words
                            itr = 1
                        else:
                            pharesAddWithSpace = pharesAddWithSpace + " " + words

                    if pharesAddWithSpace in rankedMultiplePharesDict:
                        oldValue = rankedMultiplePharesDict[pharesAddWithSpace]
                        rankedMultiplePharesDict[pharesAddWithSpace] = oldValue + "|" + files + ".txt" + "|" + str(RANKED_POINT)
                    else:
                        rankedMultiplePharesDict[pharesAddWithSpace] = files +".txt" + "|" + str(RANKED_POINT)

                RANKED_POINT = RANKED_POINT - 2
                numberOfTermsExtractedFromDocuments = numberOfTermsExtractedFromDocuments + 1
               # print("{:.4f} {:5d}  {}".format(phares.rank, phares.count, phares.text))

    buildIndexFile(rankedSinglePharesDict, rankedMultiplePharesDict)
    # print(phares.chunks)


def buildIndexFile(rankedSinglePharesDict, rankedMultiplePharesDict):
    print("=======Building Index File========")
    index_data_write = open(MAC_DATA_DIRECTORY+ BROWN_DATA_FOLDER+ BROWN_INDEX_DIRECTORY, "w")
    for key, value in rankedMultiplePharesDict.items():
        index_data_write.write(key + "|" + str(value))
        index_data_write.write("\n")
    print("==========MultiPhase Write Finished in Index======")
    for key, value in rankedSinglePharesDict.items():
        index_data_write.write(key + "|" + str(value))
        index_data_write.write("\n")


def BRWONFunctionMain():
    dataPreprocess(MAC_DATA_DIRECTORY + BROWN_DATA_FOLDER)
    renameFileinFolder(MAC_DATA_DIRECTORY + BROWN_DATA_FOLDER)
    #readAllFilesFromSourceFolder(MAC_DATA_DIRECTORY+BROWN_DATA_FOLDER)



BRWONFunctionMain()
