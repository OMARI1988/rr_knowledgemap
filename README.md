# rr_knowledgemap

This repo is used to create the knowledgebase that will be used to intelligantly answer questions from Rolls Royce.

The konwledge will be mined from various textual sources (patents, technical reports, internal reports, papers, etc..) and then we can add other challenging sources such as images.

## installing requirements
runs the following command in your terminal to install the required packages for this repo.

Please make sure you have a good internet connection. This can take a few minutes.
```
sudo pip install -U -r requirements.txt
sudo python -m spacy download en
```

## Extracting relations from patent claims
To extract simple relations from patent claims (e.g. air --> can be --> cooled) use the following:
```
python spacy_codes/learning_relations_patents.py
```
This code will extract noun phrases from claims using spacy and then learn some relations.
