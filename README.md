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

First) process claims with spacy (s)
```
python spacy_codes/learning_relations_patents.py s
```

Second) extract relations (r)
```
python spacy_codes/learning_relations_patents.py r
```

You can also print the spacy chunks using
```
python spacy_codes/learning_relations_patents.py p
```

## Extracting relations from wiki
We also aim to learn relations from wikipedia articles

### Download and preprocessing
To download the wikipedia latest xml dump go to the following and download the latest version
```
https://dumps.wikimedia.org/enwiki/
```

To extract text files from the wikipedia dump use the following package:
```
https://github.com/OMARI1988/wikiextractor
```

and simply run
```
./WikiExtractor.py /location_to_the_unzipped_xml_dump -o /location_to_the_folder_where_you_want_the_extracted_text_files
```

## ROSA
ROSA stands ROlls-ROyce Semantic Analysis tool.

ROSA is currently learning different snippets of information from various sources, including patents and wiki articles.

To run ROSA:
```
python rosa/rosa_test.py r
```

To update ROSA's knowledgebase
```
python rosa/rosa_test.py u
```
