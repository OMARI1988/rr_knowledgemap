import sys,glob,os
sys.path.insert(0, os.getcwd())
import getpass
import logging
import datetime
import cPickle
import spacy
import numpy as np
import string
from lib.preprocessing import extract_spacy
from lib.preprocessing import print_spacy
from lib.relations import relation_ed


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class spacy_process():
    """docstring for spacy_chunks."""
    def __init__(self, argv):
        logger = logging.getLogger("program")
        logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
        logging.root.setLevel(level=logging.INFO)
        logger.info("running %s", ' '.join(sys.argv))
        self.logger = logger

        # self.spacy = extract_spacy.extract_spacy(logger)
        self.spacy_printing = print_spacy.print_spacy(logger)
        # self.relation_ed = relation_ed.relation_ed(logger)

        self.user = getpass.getuser()
        self.project = "2018-08-06-11:45:28-(gas turbine)"
        if os.path.isdir("/media/"+self.user+"/Data4"):
            self.data_dir = "/media/"+self.user+"/Data4/ROSA/analysis/"+self.project+"/"
            self.save_dir = "/media/"+self.user+"/Data4/ROSA/db/"
        elif os.path.isdir("/home/"+self.user+"/Data4"):
            self.data_dir = "/home/"+self.user+"/Data4/ROSA/analysis/2018-08-06-11_45_28-(gas turbine)/"
            self.save_dir = "/home/"+self.user+"/Data4/ROSA/db/"
        self.logger.info("extract relations system ready..")

        if "s" in argv:
            self.spacy._process_all()
        if "r" in argv:
            self.relation_ing._process_all()
            # self.relation_ed._process_all()
        if "p" in argv:
            self.spacy_printing._print_all()




def main(argv):
    if argv == []:
        print "please choose if you want to process spacy or extract relations"
        print "python learning_relations_patents s (for spacy only)"
        print "python learning_relations_patents r (for relations extraction only)"
        print "python learning_relations_patents p (for printing spacy chunks)"
        print "python learning_relations_patents s r (for both)"
        sys.exit(1)
    else:
        for a in argv:
            if a not in ["s","r","p"]:
                print "please enter correct arguments"
                sys.exit(1)

    S = spacy_process(argv)

if __name__=="__main__":
    main(sys.argv[1:])
