from nltk.corpus import stopwords
import os
import re
from collections import Counter
import spacy
import pytextrank
import en_core_web_sm

mac_data_directory = "/ZResearchCode/HTopicModel/Topic-Model/Data/20news-18828"
newsGroup_Index_Directory = "/ZResearchCode/HTopicModel/Topic-Model/Data/IndexData/"
newsGroup_Index_FileName = "Index_NewsGroup.txt"
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
                    if word.isalpha():  # check the word contains only letter
                        if word.lower() not in stopWordsList:  # Remove Stop Word from List
                            filterWord.append(word)

                if len(filterWord) == 1:
                    if filterWord[0] in rankedSinglePharesDict:
                        oldValue = rankedSinglePharesDict[filterWord[0]]
                        rankedSinglePharesDict[filterWord[0]] = oldValue + "|" + files + "|" + str(phares.count)
                    else:
                        rankedSinglePharesDict[filterWord[0]] = files + "|" + str(phares.count)
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
                        rankedMultiplePharesDict[pharesAddWithSpace] = oldValue + "|" + files + "|" + str(phares.count)
                    else:
                        rankedMultiplePharesDict[pharesAddWithSpace] = files + "|" + str(phares.count)

                #print("{:.4f} {:5d}  {}".format(phares.rank, phares.count, phares.text))
                numberOfTermsExtractedFromDocuments = numberOfTermsExtractedFromDocuments + 1

    buildIndexFile(rankedSinglePharesDict, rankedMultiplePharesDict)
    # print(phares.chunks)


def buildIndexFile(rankedSinglePharesDict, rankedMultiplePharesDict):
    print("=======Building Index File========")
    index_data_write = open(newsGroup_Index_Directory + newsGroup_Index_FileName, "w")
    for key, value in rankedMultiplePharesDict.items():
        index_data_write.write(key + "|" + str(value))
        index_data_write.write("\n")
    print("==========MultiPhase Write Finished in Index======")
    for key, value in rankedSinglePharesDict.items():
        index_data_write.write(key + "|" + str(value))
        index_data_write.write("\n")


def NewsGroupFunctionMain():
    readAllFilesFromSourceFolder(mac_data_directory)


NewsGroupFunctionMain()
