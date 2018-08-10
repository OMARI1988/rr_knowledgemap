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
import matplotlib.pyplot as plt

nlp = spacy.load('en_core_web_sm')

#sentence = (u"I like strawberries")
#sentence = (u"The engine includes  a row connected to the shaft and a column attached to the beam.")
# sentence=(u"The booster engine includes a first compressor blade row attached to the first drive shaft and a second compressor blade row comprising the second drive shaft.")
#sentence=(u"Very important engine components in modern automobile engines are the blade, the flywheel, the crankshaft and the piston.")
sentence = (u"A gas turbine engine comprising a unitary gas generator effective for generating combustion gases, a counterrotatable power turbine completely aft of said gas generator including first and second interdigitated counterrotatable turbine blade rows effective for rotating first and second drive shafts, respectively; a counterrotatable fan section completely forward of said gas generator including a first fan blade row connected to said first drive shaft and a second fan blade row connected to said second drive shaft; and a counterrotatable booster compressor completely forward of said gas generator including a first compressor blade row connected to said first drive shaft and a second compressor blade row interdigitated with said first compressor blade row and connected to said second drive shaft, whereby each turbine row of the first and second turbine blade rows respectively drives both a fan blade row and a compressor blade row. ")
doc = nlp(sentence)
entities1=[]
entities2=[]
relations=[]

for chunk in doc.noun_chunks:
    print(chunk.text, chunk.root.text, chunk.root.dep_,
          chunk.root.head.text, [left for left in chunk.root.lefts], [right for right in chunk.root.rights], [ancestor for ancestor in chunk.root.ancestors], [child for child in chunk.root.children])
    

for token in doc:
   print(token.text, token.dep_, token.head.text,
          [left for left in token.lefts], [right for right in token.rights], [child for child in token.children], [ancestor for ancestor in token.ancestors])
   a='b'
   


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
        graph = nx.DiGraph(edges)
        return graph

    def getNetworkxGraphLast(self):
        edges = []
        for token in self.doc:
        # FYI https://spacy.io/docs/api/token
            for child in token.children:
                edges.append((token, child))
        graph = nx.DiGraph(edges)
        #draw graph
        pos = nx.spectral_layout(graph)
        nx.draw(graph)
        #nx.draw_networkx_nodes(graph, pos, self.doc)
        #nx.draw_networkx_edges(graph,pos, edges) 
        nx.draw_networkx_labels(graph, pos)
        plt.show()
        return graph

    def getNetworkxGraph(self):
        edges = []
        for token in self.doc:
        # FYI https://spacy.io/docs/api/token
            if token.dep_ == 'nsubj':
                edges.append((token, token.head))
            if token.rights:
                for right in token.rights:
                    edges.append((token, right))
            if token.head.dep_ == 'nsubj':
                for ancestor in token.ancestors:
                    edges.append((token, ancestor))
        graph = nx.DiGraph(edges)
        #draw graph
        #pos = nx.spring_layout(graph)
        #nx.draw(graph)
        #nx.draw_networkx_nodes(graph, pos, nodelist = [x for x in self.doc])
        #nx.draw_networkx_edges(graph, pos, edgelist = edges)
         
        #nx.draw_networkx_labels(graph, pos)
        #plt.show()
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
            try:
                #print(chunkComb)
                shPath=(nx.shortest_path(self.graph, source=chunkComb[0], target=chunkComb[1]))
                #print("hllo")  
                #evaluate each dependency path to get entity and graphlets               
                shPathEv = self.evaluateShPath(shPath, chunkComb)
                if shPathEv:
                    
                    C1, C2, R = self.generateOutput(shPathEv, chunkComb)
                    concept1.append(C1)
                    concept2.append(C2)
                    relation.append(R)
            except:
                #print("no graph connection")   
                pass
            #print output
        if concept1 and concept2 and relation:  
            #draw graph
            self.drawGraph(concept1, concept2, relation)

    def drawGraph(self, concept1, concept2, relation):
        G = nx.DiGraph()
        cCounter=0
        edge_labels={}
        for r in relation:
            G.add_edge(concept1[cCounter], concept2[cCounter])
            relationStr = ' '.join([x.text for x in r])
            edge_labels[(concept1[cCounter], concept2[cCounter])] = relationStr
            cCounter=cCounter+1       
        #draw graph
        pos = nx.spectral_layout(G)
        nx.draw(G, pos)
        nx.draw_networkx_labels(G, pos)
        nx.draw_networkx_edge_labels(G, pos, edge_labels)
        plt.show()      
            
    def generateOutput(self, shPathEv, chunkComb):
        concept1 = self.getConceptText(chunkComb[0])
        concept2 = self.getConceptText(chunkComb[1])
        relation = shPathEv[1:-1]
        '''
        if "comprising" in ' '.join([x.text for x in relation]):
            print(concept1)
            print(' '.join([x.text for x in relation]))
            print (concept2)
            print("\r\n")
        '''
        print(concept1)
        print(' '.join([x.text for x in relation]))
        print (concept2)
        print("\r\n")
        return concept1, concept2, relation
        


    def getConceptText(self, chunk):
        for chunkItem in self.doc.noun_chunks:
            if chunk == chunkItem.root:
                concept = chunkItem.text
        return concept
        
        
    def evaluateShPath(self, shPath, chunkComb):      
        #contains rules to extract concepts and relations
        #examine each item between first and last element in the path
        #for pathItem in shPath[1:-1]
            #check if there's another noun chunk
        #print([word for word in shPath])
        if len(shPath) > 2:
            if any(x in shPath[1:-1] for x in [chunk.root for chunk in self.doc.noun_chunks]):
                a='b'
                #find lists 
                    
                elemPrev = ''
                elemCounter =0
                shPath1 = []
                for elem in shPath:
                    elemCounter = elemCounter +1
                    if elem == chunkComb[1] and elemPrev in [chunk.root for chunk in self.doc.noun_chunks]:
                        #shPath1=shPath[:-2] 
                        shPath2=[item for item in shPath if item not in [chunk.root for chunk in self.doc.noun_chunks]]
                        shPath1.append(chunkComb[0])
                        shPath1.extend(shPath2)
                        shPath1.append(chunkComb[1])
                        a='b'
        
                        
                    if shPath1:
                        #print([word for word in shPath1])
                        a='b'
                    elemPrev = elem
                    a='b'

            else:
                shPath1 = shPath
                #print([word for word in shPath])
                a='b'
            
            return shPath1
            
      
        
def main():
        #sentence = (u"The engine1 partially includes a row connected to the shaft and a column attached to the beam.")
        extractGraphlets(sentence) 

if __name__ == "__main__":
    main()


