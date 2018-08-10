import spacy


txt = "blue ball"
txt = "An aircraft engine is a component of the propulsion system for an aircraft that generates mechanical power. Aircraft engines are almost always either lightweight piston engines or gas turbines, except for small multicopter UAVs which are almost always electric aircraft."
txt = "In commercial aviation, the major players in the manufacturing of turbofan engines are Pratt & Whitney, General Electric, Rolls-Royce, and CFM International (a joint venture of Safran Aircraft Engines and General Electric).[1] A major entrant into the market launched in 2016 when Aeroengine Corporation of China was formed by organizing smaller companies engaged in designing and manufacturing aircraft engines into a new state owned behemoth of 96,000 employees."
txt = "pressurized air"

nlp = spacy.load('en')
doc = nlp(txt.decode('utf8'))


# for token in doc:
    # print [token.text, token.lemma_, token.pos_, token.tag_]

for i in range(len(doc)-1):
    if doc[i].pos_ == "ADJ" and doc[i+1].pos_ == "NOUN":
        print doc[i].text, doc[i+1].text
