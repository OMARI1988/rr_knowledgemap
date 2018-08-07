import spacy
from spacy.symbols import nsubj, VERB
import numpy as np

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
        self.entitySubj, self.relationSubj, self.entityObj = self.findEntSubj()
        print(self.entitySubj.text)
        print(self.relationSubj.text)
        print(self.entityObj.text)

        for cons in self.doc[4].conjuncts:
            print(cons.text)

        #for chunk in doc.noun_chunks:
          #  self.extractGraphlet(chunk)

        for chunk in self.doc.noun_chunks:
            [entity1, relation, entity2] = self.getGraphlet(chunk)

    def findEntSubj(self):
        entityNSubj = 'None'
        relationNSubj ='None'
        entityObj = 'None'
        for chunk in self.doc.noun_chunks:
            if chunk.root.dep_ == 'nsubj':
                entityNSubj = chunk
                relationNSubj = chunk.root.head
            if chunk.root.head == relationNSubj:
                entityObj = chunk
        return entityNSubj, relationNSubj, entityObj


    
    def getGraphlet(self, chunk):
        entity1 = chunk
        token = chunk.root
        if chunk.root.dep_ == 'nsubj':
                relation = chunk.root.head
                token = chunk.root.head
                #find rights
                result = self.rightsTree(token)
                print("Hello")

    def rightsTree(self, node):
        if not node.rights:
            return []

        result = node.rights
        for right in node.rights:
            result.extend(self.rightsTree(right))

        

     




#for token in doc:
 #  print(token.text, token.pos_, token.dep_, token.head.text, token.head.pos_,
  #        [left for left in token.lefts], [right for right in token.rights], [child for child in token.children], [ancestor for ancestor in token.ancestors], [word for word in token.subtree])
   #print("\r\n")

# get noun chunks

#for entity in reversed(list(doc.noun_chunks)):
   # print(entity[-1]) # last element, usually the head word of entity
     
    # start with the last one

 

def main():
        sentence = (u"The engine includes a row connected to the shaft and a column attached to the beam.")
        extractGraphlets(sentence) 

if __name__ == "__main__":
    main()


