import os, sys, re                  ## open files and parse expressions
from math import log                ## used to calculate tf-idf
from bs4 import BeautifulSoup       ## parse url
from collections import defaultdict ## a dictionary to keep track of data

path = "C:\Users\Testing\Desktop\WEBPAGES_CLEAN"    ## Path based on users directory
allDirectories = []                 ## contains all directory
allFiles = []                       ## contains all file in the directory
numOfDocuments = 0                  ## counts the number of document
BKdictionary = dict()               ## contains all information from the bookkeeper file
countDictionary = defaultdict(int)  ## contanis the number of term in a document
tfidfDictionary = defaultdict(int)  ## contains the calculated tf-idf
invertedIndex = defaultdict(lambda : defaultdict(int))                        ## An inner and outer dictionary 
invalidTags = ['body', 'title', 'h1', 'h2', 'h3', 'b', 'strong', 'html', 'p'] ## Invalid tags in url
invalidIndex = ['the', 'a', 'an', 'this', 'that', 'these', 'those']           ## Used to improve searches

class Parser:
    def __init__(self, filePath, dirNum, fileNum):
        self.file = filePath
        self.empty = False
        self.dirNum = dirNum
        self.fileNum = fileNum
        self.doc = str(dirNum) + '/' + str(fileNum)
        self.soup = ''
            
    def countWords(self):
        try:
            if os.stat(self.file).st_size == 0:
                self.empty = True
                return

            with open(self.file, "r") as f:
                ## Strips the tags    
                self.soup = BeautifulSoup(f, 'lxml')
                for tag in invalidTags:
                    for match in self.soup.findAll(tag):
                        match.replaceWithChildren()

                ## splits the words into a list
                self.soup = re.split('[^a-zA-Z0-9]', str(self.soup))
                
                ## loop through the list and add unique words into dictionary
                for word in self.soup:
                    if word != "":
                        countDictionary[self.doc] += 1
                        invertedIndex[word.lower()][self.doc] += 1                                  
        except:
            print("You did not enter a valid file path")
        
        
def getBKdictionary():
    global BKdictionary
    ## Path based on users directory
    with open('C:\Users\Testing\Desktop\WEBPAGES_CLEAN\\bookkeeping.json', "r") as f:

        ## cleans the line so that it is easily placed into the dictionary
        for l in f:
            l = l.strip('\n')
            l = l.strip(',')
            l = l.replace(' ', '')
            l = l.replace('"', '')
            line = l.split(':')
            BKdictionary[line[0]] = line[-1]


def getAllFiles():
    global BKdictionary
    global invertedIndex
    global allDirectories
    global allFiles
    global numOfDocuments
    global countDictionary
    global tfidfDictionary

    ## remove file from list, since it is not a directory
    allDirectories.extend(os.listdir(path))
    allDirectories.remove('bookkeeping.json')
    allDirectories.remove('bookkeeping.tsv')

    getBKdictionary()

    for d in allDirectories: ## 0-74 + json files
        if os.path.isdir(path + "\\" + str(d) + "\\"):
            fileDirectory = os.listdir(path + '\\' + str(d))                        
            numOfDocuments += len(fileDirectory)
                    
        for f in fileDirectory:
            filePath = path + '\\' + str(d) + '\\' + str(f)
            parser = Parser(filePath, d, f)
            parser.countWords()    


def Calculate():
    termList = []
    term = raw_input('Enter a term: ').lower()

    ## Check if user input one or more value
    ## Then take the appropriate actions
    if ' ' in term:
        termList = term.split(' ')
        for t in invalidIndex:
            if t in termList:
                termList.remove(t)
    else:
        termList.append(term)
    
    ## Calculate tf-idf
    for t in termList:
        for k, v in invertedIndex[t].items():    ## k = doc, v = tf
            tf = float(v) / countDictionary[k]   ## countDictionary[k] = total terms in doc
            idf = log( numOfDocuments, len(invertedIndex[t]) )
            tf_idf = tf * idf
            tfidfDictionary[k] += round(tf_idf, 5)
    
    i = 0 ## keeps track of top 10 value
    for k, v in sorted(tfidfDictionary.items(), key = lambda x: -x[1] ):
        i += 0
        if i < 10: print BKdictionary[k], ': ', v
        
        
if __name__ == "__main__":
    getAllFiles()
    Calculate()



            
