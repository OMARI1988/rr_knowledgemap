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

class extract_claims():
    """This class extract claims with certain words in them from the extracted csv files."""
    def __init__(self, logger, process):
        self.process = process
        self.logger = logger
        self.user = getpass.getuser()

        # loading the spacy model
        self.nlp = spacy.load('en')

        # finding csv files of claims
        if os.path.isdir("/media/"+self.user+"/Data1/patents/csv/claims/"):
            self.data_dir_ = "/media/"+self.user+"/Data1/patents/csv/claims/"
        else:
            self.logger.info("check your directories..")
            sys.exit(1)
        self.data = sorted(glob.glob(self.data_dir_+"*.csv"))

        # data store locations
        self.save_dir_ = "/media/"+self.user+"/Data4/ROSA/analysis/"

        self.logger.info("system ready..")

    def _search_for(self, query):
        # creating the save dir for this search query
        x = datetime.datetime.now()
        name = str(x).replace(" ","-").split(".")[0]
        name += "-("+query[:20]+")"
        self.name = name.replace("/","",-1)
        os.mkdir(self.save_dir_+self.name)

        # starting the search
        counter = 0
        self.claims = {}

        self.range_ = 500
        self.range_counter = 0
        r1 = str( self.range_counter*self.range_ )
        r2 = str( (self.range_counter+1)*self.range_ - 1 )
        R = r1 +"-"+ r2
        self.claims[R] = {}

        for file_ in self.data:
            date = file_.split("_")[-1].split(".")[0].replace("ipg","")
            date = "20"+date[:2]+"-"+date[2:4]+"-"+date[-2:]
            self.logger.info("Searching "+file_)
            f = open(file_,"r")
            for line in f:
                if query in line:
                    line = line.replace("\r","",-1)
                    line = line.split("\n")[0]
                    line = line.split(",")
                    patent_id = line[1]
                    claim_num = line[-1]
                    claim_dep = line[-2]
                    txt = ",".join(line[2:-2])

                    self.claims[R][counter] = {}
                    self.claims[R][counter]["txt"] = txt
                    self.claims[R][counter]["date"] = date
                    self.claims[R][counter]["patent_id"] = patent_id
                    self.claims[R][counter]["claim_num"] = claim_num
                    self.claims[R][counter]["claim_dep"] = claim_dep
                    counter += 1
                    if counter >= (self.range_counter+1)*self.range_ - 1:
                        self.range_counter += 1
                        r1 = str( self.range_counter*self.range_ )
                        r2 = str( (self.range_counter+1)*self.range_ - 1 )
                        R = r1 +"-"+ r2
                        self.claims[R] = {}
                        self.logger.info("  --the range has changed to "+R)
            # if counter > 2000:
            #     break
            self.logger.info("done, %d claims were found. " %counter)


        self._spacy_data()


    def _save_data(self, R):
        self.logger.info("  -- saving "+R+" claims data in txt..")
        # for R in self.claims:
        f = open(self.save_dir_+self.name+"/"+R+"-claims.txt","w")
        for counter in self.claims[R]:
            txt = self.claims[R][counter]["txt"]
            date = self.claims[R][counter]["date"]
            patent_id = self.claims[R][counter]["patent_id"]
            claim_num = self.claims[R][counter]["claim_num"]
            claim_dep = self.claims[R][counter]["claim_dep"]
            f.write(date + " -=- " + patent_id + " -=- " + claim_num + " -=- " + claim_dep + " -=- " + txt + "\n")
        f.close()
        # self.logger.info("-done saving claims data in txt.")

        self.logger.info("  -- saving "+R+" claims data in pickle..")
        # for R in self.claims:
        cPickle.dump(self.claims[R], open(self.save_dir_+self.name+"/"+R+"-claims.p","w"))
        # self.logger.info("-done saving claims data in pickle.")


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
        p = Pool(50)
        for R in sorted(self.claims):
            self.logger.info("  -- processing the "+R+" spacy claims..")
            data = []
            for counter in self.claims[R]:
                txt = self.claims[R][counter]["txt"]
                data.append([ counter, txt ])

            results = p.map(_Spacy_multicore, data)

            for data in results:
                counter, spacy_data, spacy_chunks = data
                # contains the pos, lemma and tag for every word in the claim
                self.claims[R][counter]["spacy_data"] = spacy_data

                # contains the phrases found in the claim
                self.claims[R][counter]["spacy_chunks"] = spacy_chunks
            self._save_data(R)

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



def main():
    logger = logging.getLogger("program")
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
    logging.root.setLevel(level=logging.INFO)
    logger.info("running %s", ' '.join(sys.argv))

    E = extract_claims(logger, "multi")
    # E = extract_claims(logger, "single")
    E._search_for("gas turbine")

if __name__=='__main__':
    main()
