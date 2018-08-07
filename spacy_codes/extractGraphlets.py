import spacy
import numpy as np

nlp = spacy.load('en_core_web_sm')

sentence=(u"The booster engine includes a row and a column")
doc = nlp(sentence)
entities1=[]
entities2=[]
relations=[]
for chunk in doc.noun_chunks:
    print(chunk.text, chunk.root.text, chunk.root.dep_,
          chunk.root.head.text, [left for left in chunk.root.lefts], [right for right in chunk.root.rights], [ancestor for ancestor in chunk.root.ancestors], [child for child in chunk.root.children], [word for word in chunk.root.subtree])
    print("\r\n")
    
    '''
    if chunk.root.dep_ == 'nsubj':
        entities1.append(chunk)
        # find relation
        relations.append(chunk.root.head.text)
        # find second entity
    #for the next noun chunk
    #find relation in doc so we can use token tools
    relationMain = doc[sentence.split().index(chunk.root.head.text)]
    relationMainLefts=list(relationMain.lefts)
    relationsLeft =
    relationsLeft=np.setdiff1d(relationMainLefts, chunk.text.split())
    print(relationsLeft)
   # print(relationsLeft)

   
    '''

for token in doc:
   print(token.text, token.dep_, token.head.text,
          [left for left in token.lefts], [right for right in token.rights], [child for child in token.children], [ancestor for ancestor in token.ancestors], [word for word in token.subtree])
   print("\r\n")

print("\r\n")
lca = doc.get_lca_matrix()
print(lca[0])


#for token in doc:
 #  print(token.text, token.pos_, token.dep_, token.head.text, token.head.pos_,
  #        [left for left in token.lefts], [right for right in token.rights], [child for child in token.children], [ancestor for ancestor in token.ancestors], [word for word in token.subtree])
   #print("\r\n")

# get noun chunks

#for entity in reversed(list(doc.noun_chunks)):
   # print(entity[-1]) # last element, usually the head word of entity
     
    # start with the last one

