import sys,glob,os
import getpass
import logging
import datetime
import cPickle
import spacy
import numpy as np
from multiprocessing import Pool

global nlp
nlp = spacy.load('en')

def _Spacy_multicore(data):
    global nlp
    counter, txt = data
    doc = nlp(txt.decode('utf8'))
    spacy_data = []
    spacy_chunks = []

    for token in doc:
        spacy_data.append([token.text, token.lemma_, token.pos_, token.tag_])

    for chunk in doc.noun_chunks:
        spacy_chunks.append([chunk.text, chunk.start, chunk.end, chunk.root.text])

    return [counter, spacy_data, spacy_chunks]

class extract_spacy():
    """This class extract all paragraphs from wiki articles.
       To use this script, use the _process_all() to process all claims"""

    def __init__(self, logger, process="multi"):
        # logger = logging.getLogger("program")
        # logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
        # logging.root.setLevel(level=logging.INFO)
        # logger.info("running %s", ' '.join(sys.argv))
        self.process = process
        self.logger = logger
        self.user = getpass.getuser()
        self.p = Pool(5)

        # loading the spacy model
        self.nlp = spacy.load('en')

        # finding csv files of claims
        if os.path.isdir("/media/"+self.user+"/Data4/wiki/extracted_files/"):
            self.data_dir_ = "/media/"+self.user+"/Data4/wiki/extracted_files/"
        else:
            self.logger.info("check your directories..")
            sys.exit(1)

        self.data = []
        for folder in sorted([x[0] for x in os.walk(self.data_dir_)]):
            self.data += glob.glob(folder+"/wiki_*")
        self.data = sorted(self.data)

        # data store locations
        self.save_dir_ = "/media/"+self.user+"/Data4/ROSA/analysis/"

        self.logger.info("extracting spacy info system ready..")


    def _process_all(self):
        # creating the save dir for this search query
        x = datetime.datetime.now()
        name = "all-wiki"
        self.name = name.replace("/","",-1)
        if not os.path.isdir(self.save_dir_+self.name):
            os.mkdir(self.save_dir_+self.name)

        for file_ in self.data:

            self.f_name = file_.split("/")[-1]
            if not os.path.isdir(self.save_dir_+self.name+"/"+self.f_name):
                os.mkdir(self.save_dir_+self.name+"/"+self.f_name)

            self.wiki_page = {}

            # makding sure to not reprocess all weeks again
            if os.path.isfile(self.save_dir_+self.name+"/"+self.f_name+"/finished.meta"):
                self.logger.info("I have processed "+self.f_name+" before..")
                continue

            self.logger.info("Searching "+file_)
            f = open(file_,"r")

            for line in f:
                line = line.split("\n")[0]
                if line == "":
                    continue
                if "<doc id=" in line:
                    line = line.split("\"")
                    id_ = line[1]
                    title = line[5]
                    url = line[3]
                    self.wiki_page[id_] = {}
                    self.wiki_page[id_]["id"] = id_
                    self.wiki_page[id_]["title"] = title
                    self.wiki_page[id_]["url"] = url
                    self.wiki_page[id_]["text"] = []
                elif "</doc>" not in line:
                    if len(line.replace(" ","",-1))<10:
                        continue
                    line = self._clean(line)
                    self.wiki_page[id_]["text"].append(line)

            self.logger.info("done, %d articles were found. " %len(self.wiki_page))
            self._spacy_data()

    def _clean(self, text):
        return ''.join([i if ord(i) < 128 else '' for i in text])

    def _save_data(self):
        self.logger.info("  -- saving "+self.date+"-"+self.range_+" claims data in pickle..")
        if not os.path.isdir(self.save_dir_+self.name+"/"+self.date):
            os.mkdir(self.save_dir_+self.name+"/"+self.date)
        cPickle.dump(self.claims_range, open(self.save_dir_+self.name+"/"+self.date+"/"+self.range_+"-claims.p","w"))


    def _spacy_data(self):
        self.logger.info("processing claims using SpaCy..")

        if self.process == "multi":
            self.logger.info(" -using multi core for SpaCy..")
            self._spacy_multi()
        else:
            self.logger.info(" -using single core for SpaCy..")
            self._space_single()

        self.logger.info("-finished processing claims using SpaCy..")


    def _spacy_multi(self):
        # for R in sorted(self.claims):
        self.logger.info("  -- processing the spacy claims "+self.f_name+"..")
        # for ri in range(0,len(self.wiki_page),1000):
            # rs, rl = ri, min(ri+1000, len(self.claims))
            # self.range_ = str(rs)+"-"+str(rl)
            # data = []
            # self.claims_range = {}
            # for counter in range(rs,rl):
        for id_ in self.wiki_page:
            print id_
            txt = self.wiki_page[id_]["text"]
            print txt
        #         data.append([ counter, txt ])
        #         self.claims_range[counter] = self.claims[counter].copy()
        #
        #     results = self.p.map(_Spacy_multicore, data)
        #
        #     for data in results:
        #         counter, spacy_data, spacy_chunks = data
        #         # contains the pos, lemma and tag for every word in the claim
        #         self.claims_range[counter]["spacy_data"] = spacy_data
        #
        #         # contains the phrases found in the claim
        #         self.claims_range[counter]["spacy_chunks"] = spacy_chunks
        #     self._save_data()
        # self.logger.info("  -- finished processing the spacy claims "+self.date+"..")
        # F = open(self.save_dir_+self.name+"/"+self.date+"/finished.meta","w")
        # F.close()

    def _space_single(self):
        for R in sorted(self.claims):
            for counter in self.claims[R]:
                txt = self.claims[R][counter]["txt"]
                doc = self.nlp(txt.decode('utf8'))
                spacy_data = []
                spacy_chunks = []

                for token in doc:
                    spacy_data.append([token.text, token.lemma_, token.pos_, token.tag_])

                for chunk in doc.noun_chunks:
                    spacy_chunks.append([chunk.text, chunk.start, chunk.end, chunk.root.text])

                # contains the pos, lemma and tag for every word in the claim
                self.claims[R][counter]["spacy_data"] = spacy_data

                # contains the phrases found in the claim
                self.claims[R][counter]["spacy_chunks"] = spacy_chunks

                if np.mod(counter, 100)==0 and counter>0:
                    self.logger.info("  -processed %d claims so far." %counter)

            self._save_data(R)

        self.logger.info("-done processing claims using SpaCy...")

        # self.logger.info("saving spacy claims data in pickle..")
        # cPickle.dump(self.claims, open(self.save_dir_+name+"/claims_spacy.p","w"))
        # self.logger.info("-done saving spacy claims data in pickle.")

            # print " =================== tokens"
            # for token in doc:
            #     print token.text
            #     print token.lemma_
            #     print token.pos_
            #     print token.tag_
            #     print "--------"

            # print " =================== chunks"
            # for chunk in doc.noun_chunks:
            #     if "chamber" in chunk.text:
            #         # print dir(chunk)
            #         start = chunk.start
            #         end = start+len(chunk.text.split(" "))
            #         print [chunk.text, chunk.start, chunk.root.text]
            #         for token in doc[ start:end ]:
            #             print token.text
            #             print token.lemma_
            #             print token.pos_
            #             print token.tag_
            #             print "--------"


#
# def main():
#     logger = logging.getLogger("program")
#     logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
#     logging.root.setLevel(level=logging.INFO)
#     logger.info("running %s", ' '.join(sys.argv))
#
#     E = extract_claims(logger, "multi")
#     # E = extract_claims(logger, "single")
#     E._search_for("gas turbine")

if __name__=='__main__':
    main()
