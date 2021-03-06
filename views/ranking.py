import os, sys, re                  ## open files and parse expressions
import json
import ast
from math import log                ## used to calculate tf-idf
from collections import defaultdict ## a dictionary to keep track of data


invalidIndex = []                   ## Used to improve searches
uniqueTerms = set()                 ## set of unique terms to calculate tfidf
numOfDocuments = 37497              ## counts the number of document
BKdictionary = dict()               ## contains all information from the bookkeeper file
countDictionary = defaultdict(int)  ## contanis the number of term in a document
tfidfDictionary = defaultdict(int)  ## contains the calculated tf-idf
invertedIndex = defaultdict(lambda : defaultdict(int))                        ## An inner and outer dictionary 
invalidTags = ['body', 'title', 'h1', 'h2', 'h3', 'b', 'strong', 'html', 'p'] ## Invalid tags in url

        
def getBKdictionary():
    global BKdictionary

    f = open("BKdictionary.json", "r")
    BKdictionary = json.loads(f.read())


def getAllFiles():
    global BKdictionary
    global invertedIndex
    global numOfDocuments
    global countDictionary
    global tfidfDictionary
    global invalidTags

    getBKdictionary()


    f = open("countDictionary.json", "r")
    countDictionary = json.loads(f.read())

    g = open("invertedIndex.json", "r")
    invertedIndex = json.loads(g.read())


def getUserInput(term):
    global uniqueTerms
    termList = []
    uniqueTerms = set()
    term = term.lower()

    try:
        ## parses the term and checks for unique terms
        termList = re.split('[^a-zA-Z0-9]', term)

        for t in termList:
            if t != '':
                uniqueTerms.add(t)

        temp = uniqueTerms.copy() ## a copy of uniqueTerms to remove value from the orginal set
        
        ## Removes terms that are not in the dictionary
        for t in temp:
            if t not in invertedIndex:
                uniqueTerms.remove(t)
                
        ## takes out stop words
        for t in temp:
            if t in invalidIndex and len(uniqueTerms) > 1 and t in uniqueTerms:
                uniqueTerms.remove(t)
                
    except:
        return [False, 'No documents match your query']

            
def Calculate(term):
    global BKdictionary
    global invertedIndex
    global tfidfDictionary
    global invalidIndex

    searchResults = []
    getUserInput(term) ## takes userInput

    if len(uniqueTerms) == 0:
        return [False, 'No documents match your query']
        
    ## Calculate tf-idf
    for t in uniqueTerms:
        for k, v in invertedIndex[t].items():    ## k = doc, v = tf
            tf = float(v) / float(countDictionary[k])   ## countDictionary[k] = total terms in doc
            idf = log( float(numOfDocuments)/ float(len(invertedIndex[t])) )
            tf_idf = tf * idf
            tfidfDictionary[k] += round(tf_idf, 5)
        
    ## Adds the top 10 url into a list
    for k, v in sorted(tfidfDictionary.items(), key = lambda x: -x[1] ):
        searchResults.append(BKdictionary[k])
        if len(searchResults) == 10:
            return searchResults

    return searchResults

def getStopWords():
    global invalidIndex
    
    with open('views/stopwords.txt', "r") as f:
        for line in f:
            line = line.strip('\n')
            invalidIndex.append(line.strip())
            
        
if __name__ == "__main__":
    getStopWords()
    getAllFiles()
    Calculate()



            
