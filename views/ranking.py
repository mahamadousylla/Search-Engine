import os, sys, re                  ## open files and parse expressions
from math import log                ## used to calculate tf-idf
from bs4 import BeautifulSoup       ## parse url
from collections import defaultdict ## a dictionary to keep track of data

path = "C:\Users\Testing\Desktop\WEBPAGES_CLEAN"
allDirectories = []                 ## contains all directory
allFiles = []                       ## contains all file in the directory
numOfDocuments = 0                  ## counts the number of document
BKdictionary = dict()               ## Contains all information from the bookkeeper file
countDictionary = defaultdict(int)  ## Contanis the number of term in a document
tfidfDictionary = dict()            ## Contains the calculated tf-idf
invertedIndex = defaultdict(lambda : defaultdict(int))                        ## An inner and outer dictionary 
invalidTags = ['body', 'title', 'h1', 'h2', 'h3', 'b', 'strong', 'html', 'p'] ## Invalid tags in url


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
    with open('C:\Users\Testing\Desktop\WEBPAGES_CLEAN\\bookkeeping.json', "r") as f:

        ## cleans the word so that it is easily placed into the dictionary
        for l in f:
            l = l.strip('\n')
            l = l.strip(',')
            l = l.replace(' ', '')
            l = l.replace('"', '')
            line = l.split(':')
            BKdictionary[line[0]] = line[-1]
            
    f.close()


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

##        for d in allDirectories: ## 0-74 + json files
        for d in range(0,30):
            if os.path.isdir(path + "\\" + str(d) + "\\"):
                fileDirectory = os.listdir(path + '\\' + str(d))                        
                numOfDocuments += len(fileDirectory)

                        
##            for f in fileDirectory:
            for f in range(0, 30):
                    filePath = path + '\\' + str(d) + '\\' + str(f)
                    parser = Parser(filePath, d, f)
                    parser.countWords()

def writeToFile():
        textFile = open("C:\Users\Testing\Desktop\invertedIndex.txt", "w")

        ##loop through invertedIndex and write to text file
        for k, v in invertedIndex.items(): ## loop through outter dictionary (terms)
            textFile.write('{k} - '.format(k=k))
            for k2, v2 in v.items(): ## loop through inner dictionary (doc: tf)
                textFile.write('{k2}: {v2}; '.format(k2 = k2, v2 = v2))
            textFile.write('\n')

        textFile.close()

def getQuery():
    
    textFile = open("C:\Users\Testing\Desktop\Query.txt", "w")
    textFile.write('Tony Hua 16788298\nMahamadou Sylla 61549479\n\n')
##    listOfTerms = ['informatics', 'irvine', 'mondego']
    listOfTerms = []
##    print('Deliverables: ')

## query for terms
    ## loop through list of terms
    for term in listOfTerms:
        numOfTerm = 0
##        ## write to file
##        textFile.write('--------------------------------------------------------------------------\n')    
##        textFile.write('--------------------------------------------------------------------------\n')
##        textFile.write('{term}:\n'.format(term = term))
##        textFile.write('--------------------------------------------------------------------------\n')
##        textFile.write('--------------------------------------------------------------------------\n')

        ## loop through the inner dictionary of the term
        for k, v in invertedIndex[term].items():
            numOfTerm += v


##        textFile.write('{key}: {value}\n'.format(key = BKdictionary[k], value = v))
##        textFile.write('\n')
##        print('Total number of {term}: {n}'.format(term = term, n = numOfTerm))

##    print('Number of Documents: {n}\n'.format(n = numOfDocuments))
##    print('Number of Unique Words: {n}\n'.format(n = len(invertedIndex)))
##    print('Total size(in KB): 88334 KB\n')

        textfile.close()    
    

def Calculate():
    term = raw_input('Enter a term: ').lower()
##    print ('testing...', term.split())
##    termList = term.split('')
##    print 'termsList : ', termList

    print '---------------------------'
    print '---------------------------'
    print 'Here are the results for {term}'.format(term = term)
    print '---------------------------'
    print '---------------------------'

    
    ## Calculate tf-idf
    for k, v in invertedIndex[term].items(): ## k = doc, v = tf
        tf = float(v) / countDictionary[k]            ## countDictionary[k] = total terms in doc
        idf = log( numOfDocuments, len(invertedIndex[term]) )
        tf_idf = tf * idf
        tfidfDictionary[k] = round(tf_idf, 5)

    
    i = 0 ## keeps track of top 10 value
    for k, v in sorted(tfidfDictionary.items(), key = lambda x: -x[1] ):
        i += 0
        if i > 10: break
        print BKdictionary[k], ': ', v
        
if __name__ == "__main__":
        getAllFiles()
        writeToFile()
        getQuery()
        Calculate()
##        print 'Total number of the term Informatics: ', numOfInformatics
##        print 'Total number of the term Irvine: ', numOfIrvine
##        print 'Total number of the term Mondego: ', numOfMondego
##        print 'Number of Documents: ', numOfDocuments
##        print 'Number of Unique Words: ', len(invertedIndex)
##        print 'Total size(in KB): 88334 KB'



            
