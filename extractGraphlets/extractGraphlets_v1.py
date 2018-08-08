#!/usr/bin/env python
# coding: utf8

''' extracts graphlets from sentence using spacy's noun_chunks and dependency parsing


    v1: 08/08/18: uses networkx to find shortest path between two terms

''' 
import spacy
import networkx as nx
from spacy.symbols import nsubj, VERB
import numpy as np
import itertools as it

nlp = spacy.load('en_core_web_sm')

sentence = (u"The engine includes a row connected to the shaft and a column attached to the beam.")
#sentence=(u"The booster engine includes a first compressor blade row1 attached to the first drive shaft1 and a second compressor blade row2 comprising the second drive shaft2.")
doc = nlp(sentence)
entities1=[]
entities2=[]
relations=[]

for chunk in doc.noun_chunks:
    print(chunk.text, chunk.root.text, chunk.root.dep_,
          chunk.root.head.text, [left for left in chunk.root.lefts], [right for right in chunk.root.rights], [ancestor for ancestor in chunk.root.ancestors], [child for child in chunk.root.children])
    
print("\r\n")
print("\r\n")
for token in doc:
   print(token.text, token.dep_, token.head.text,
          [left for left in token.lefts], [right for right in token.rights], [child for child in token.children], [ancestor for ancestor in token.ancestors])
   print("\r\n")


class extractGraphlets():

    def __init__(self, inputSentence):

        nlp = spacy.load('en_core_web_sm')
        self.sentence = inputSentence
        self.doc = nlp(self.sentence)
        self.graph = self.getNetworkxGraph()
        self.chunkCombs = self.getChunkCombs()
        self.graphlets = self.getGraphlets()


    def getNetworkxGraph1(self):
        edges = []
        for token in self.doc:
        # FYI https://spacy.io/docs/api/token
            for child in token.children:
                edges.append(('{0}-{1}'.format(token.lower_,token.i), '{0}-{1}'.format(child.lower_,child.i)))
        graph = nx.Graph(edges)
        return graph

    def getNetworkxGraph(self):
        edges = []
        for token in self.doc:
        # FYI https://spacy.io/docs/api/token
            for child in token.children:
                edges.append((token, child))
        graph = nx.Graph(edges)
        return graph

    def getChunkCombs1(self):
        #first get noun_chunks, then extract root and root position of each chunk
        chunkRootIndexList=[]
        for chunk in self.doc.noun_chunks:
            chunkRootIndex = "{}-{}".format(chunk.root.text,str(chunk.root.i))
            chunkRootIndexList.append(chunkRootIndex)
        # get all combinations of chunkRootIndexList
        chunkCombs = list(it.combinations(chunkRootIndexList, 2))    
        return chunkCombs

    def getChunkCombs(self):
        #first get noun_chunks, then extract root and root position of each chunk
        chunkRootIndexList=[]
        for chunk in self.doc.noun_chunks:
            chunkRootIndex = chunk.root
            chunkRootIndexList.append(chunkRootIndex)
        # get all combinations of chunkRootIndexList
        chunkCombs = list(it.combinations(chunkRootIndexList, 2))    
        return chunkCombs


    def getGraphlets(self):
        #get shortest dependecy path
        concept1= []
        concept2 = []
        relation = []
        for chunkComb in self.chunkCombs:
            shPath=(nx.shortest_path(self.graph, source=chunkComb[0], target=chunkComb[1]))
            #print("hllo")  
            #evaluate each dependency path to get entity and graphlets
            self.evaluateShPath(shPath, chunkComb)
        
        
    def evaluateShPath(self, shPath, chunkComb):
        
        #contains rules to extract concepts and relations
        #examine each item between first and last element in the path
        #for pathItem in shPath[1:-1]
            #check if there's another noun chunk
        if len(shPath) > 2:
            if any(elem in shPath[1:-1] for elem in [chunk.root for chunk in self.doc.noun_chunks]):
                a='b'
            else:
                print([word for word in shPath])
            


       
            




        



    
 

def main():
        sentence = (u"The engine includes a row connected to the shaft and a column attached to the beam.")
        extractGraphlets(sentence) 

if __name__ == "__main__":
    main()


