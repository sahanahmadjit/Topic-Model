from nltk.corpus import stopwords
import os
import re
from collections import Counter
import spacy
import pytextrank
import en_core_web_sm

MAC_DATA_DIRECTORY = "/ZResearchCode/HTopicModel/Topic-Model/Data/"
NEWSGROUP_INDEX_DIRECTORY = "IndexData/"
NEWSGROUP_INDEX_FILENAME = "Index_NewsGroup.txt"
NEWSGROUP_DATA_FOLDER= "20news-18828/"
NUMBER_OF_TERMS_EXTRACTED_FROM_DOCUMENT = 20

# Load English tokenizer, tagger, parser, NER and word vectors
nlp = spacy.load("en_core_web_sm")
# add PyTextRank to the spaCy pipeline
tr = pytextrank.TextRank()
nlp.add_pipe(tr.PipelineComponent, name="textrank", last=True)


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
            # print("Full File Path", filepath)
            sample_file = open(filepath, "r", encoding="iso-8859-1")
            text = sample_file.read().lower()
            doc = nlp(text)

            # examine the top-ranked phrases in the document
            numberOfTermsExtractedFromDocuments = 0
            for phares in doc._.phrases:
                if numberOfTermsExtractedFromDocuments == NUMBER_OF_TERMS_EXTRACTED_FROM_DOCUMENT:
                    break
                splitbySpace = re.split('\s+', str(phares))  # split the sentence by space
                filterWord = []
                for word in splitbySpace:
                    removeSpace= word.strip()
                    if removeSpace.isalpha():  # check the word contains only letter
                        if removeSpace.lower() not in stopWordsList:  # Remove Stop Word from List
                            filterWord.append(removeSpace)

                if len(filterWord)== 0: #if no meaningful word look for the next one
                    continue
                if len(filterWord) == 1:
                    if filterWord[0] in rankedSinglePharesDict:
                        oldValue = rankedSinglePharesDict[filterWord[0]]
                        rankedSinglePharesDict[filterWord[0]] = oldValue + "|" + files+ ".txt" + "|" + str(phares.count)
                    else:
                        rankedSinglePharesDict[filterWord[0]] = files +".txt" + "|" + str(phares.count)
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
                        rankedMultiplePharesDict[pharesAddWithSpace] = oldValue + "|" + files + ".txt" + "|" + str(phares.count)
                    else:
                        rankedMultiplePharesDict[pharesAddWithSpace] = files +".txt" + "|" + str(phares.count)


                numberOfTermsExtractedFromDocuments = numberOfTermsExtractedFromDocuments + 1
               # print("{:.4f} {:5d}  {}".format(phares.rank, phares.count, phares.text))

    buildIndexFile(rankedSinglePharesDict, rankedMultiplePharesDict)
    # print(phares.chunks)


def buildIndexFile(rankedSinglePharesDict, rankedMultiplePharesDict):
    print("=======Building Index File========")
    index_data_write = open(MAC_DATA_DIRECTORY+ NEWSGROUP_INDEX_DIRECTORY + NEWSGROUP_INDEX_FILENAME, "w")
    for key, value in rankedMultiplePharesDict.items():
        index_data_write.write(key + "|" + str(value))
        index_data_write.write("\n")
    print("==========MultiPhase Write Finished in Index======")
    for key, value in rankedSinglePharesDict.items():
        index_data_write.write(key + "|" + str(value))
        index_data_write.write("\n")


def NewsGroupFunctionMain():
    readAllFilesFromSourceFolder(MAC_DATA_DIRECTORY+NEWSGROUP_DATA_FOLDER)



NewsGroupFunctionMain()
