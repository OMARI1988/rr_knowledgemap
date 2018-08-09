import sys,glob,os
import getpass
import logging
import datetime
import cPickle
import spacy
import numpy as np

class print_spacy():
    """This class extract claims with certain words in them from the extracted csv files.
       There are two ways to use this class,
       either use the _process_all() to process all claims
       or use the _search_for(query) to process claims that contain that query
       The output of this class is a pickle and txt file per week of claims."""

    def __init__(self, logger):
        # logger = logging.getLogger("program")
        # logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
        # logging.root.setLevel(level=logging.INFO)
        # logger.info("running %s", ' '.join(sys.argv))
        self.logger = logger
        self.user = getpass.getuser()

        # data store locations
        self.save_dir_ = "/home/"+self.user+"/Data4/ROSA/analysis/2018-08-06-11_45_28-(gas turbine)/"
        file_ = self.save_dir_+"0-499-claims.p"

        self.claims = cPickle.load( open(file_,"r") )

    def _print_all(self):
        for cnk in self.claims[0]["spacy_chunks"]:
            print cnk[0]
