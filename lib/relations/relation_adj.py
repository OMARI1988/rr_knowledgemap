import sys,glob,os
import getpass
import logging
import datetime
import cPickle
import spacy
import numpy as np
import string
import gensim
from gensim.utils import lemmatize

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class relation_adj():
    """docstring for spacy_chunks."""
    def __init__(self, logger):
        self.logger = logger
        self.user = getpass.getuser()
        self.project = "all-claims"
        if os.path.isdir("/media/"+self.user+"/Data4"):
            self.data_dir = "/media/"+self.user+"/Data4/ROSA/analysis/"+self.project+"/"
            self.save_dir = "/media/"+self.user+"/Data4/ROSA/db/"
        elif os.path.isdir("/home/"+self.user+"/Data4"):
            self.data_dir = "/home/"+self.user+"/Data4/ROSA/analysis/2018-08-06-11_45_28-(gas turbine)/"
            self.save_dir = "/home/"+self.user+"/Data4/ROSA/db/all-claims/"

        self.logger.info("learning adj relations ready..")

    def _process_all(self):
        if not os.path.isdir(self.save_dir):
            os.mkdir(self.save_dir)
        self.save_dir += "adj/"
        if not os.path.isdir(self.save_dir):
            os.mkdir(self.save_dir)

        self.folders = sorted([x[0] for x in os.walk(self.data_dir)])

        for folder in self.folders:

            self.name = folder.split("/")[-1]
            if not os.path.isdir(self.save_dir+self.name):
                os.mkdir(self.save_dir+self.name)

            for file_ in sorted(glob.glob(folder+"/*.p")):
                self.file_name = file_.split("/")[-1].replace(".p",".txt")
                if os.path.isfile(self.save_dir+self.name+"/"+self.file_name):
                    continue
                self.logger.info("processing "+self.name+"-"+self.file_name)
                self.claims = cPickle.load( open(file_, "r") )
                self._process_chunks()

    def _process_chunks(self):
        # self.F_ed = open(self.save_dir+self.name+"/"+self.file_name+".processing","w")
        self.unique_chunks = []
        self.unique_codes = {}
        self.bad_starting_words = ["and", "or"]
        for counter in self.claims:
            self._1_adj_relations(counter)
        # src = self.save_dir+self.name+"/"+self.file_name+".processing"
        # dst = self.save_dir+self.name+"/"+self.file_name
        # os.rename(src, dst)


    def _clean_cnk(self, txt):
        txt = txt.replace("&lt;sub&gt;","",-1)
        return txt

    def _clean_words(self, words):
        for i in range(len(words)):
            words[i][0] = words[i][0].replace("&lt;sub&gt;"," ",-1)
            words[i][0] = words[i][0].replace("&lt;/sub&gt;"," ",-1)
            words[i][0] = words[i][0].replace("&lt;/sub&gt"," ",-1)
            words[i][0] = words[i][0].replace("  "," ",-1)
            words[i][0] = words[i][0].replace("  "," ",-1)
        return words

    def _1_adj_relations(self, counter):
        adj_flag = 0
        adjs = []
        nouns = []

        meta_data = self.claims[counter]["patent_id"] + ","+ self.claims[counter]["claim_num"]
        meta_data += ","+self.claims[counter]["claim_dep"]+","+self.claims[counter]["date"]

        for word in self.claims[counter]["spacy_data"]:
            if word[2] == "ADJ":
                adj_flag = 1
                adjs.append(word[0])
            elif adj_flag and word[2]=="NOUN":
                nouns.append(word[0])
            elif adj_flag:
                phrase = " ".join(nouns)
                prop = " ".join(adjs)

                print bcolors.FAIL + phrase + bcolors.ENDC, "-->", "can be", "-->",
                print bcolors.OKBLUE + prop + bcolors.ENDC, "<-->",
                print bcolors.WARNING + meta_data + bcolors.ENDC

                adj_flag = 0
                adjs = []
                nouns = []

        # for cnk in self.claims[counter]["spacy_chunks"]:
        #     print cnk
            # # if "ed " in cnk[0]:
            #     cnk[0] = self._clean_cnk(cnk[0])
            #     if cnk[0] not in self.unique_chunks:
            #         # if "MIN" not in cnk[0]:
            #         #     continue
            #         print cnk[0]
            #         s,e = cnk[1], cnk[2]
            #         noun = []
            #         properties = []
            #
            #         words = self.claims[counter]["spacy_data"][s:e]
            #         words = self._clean_words(words)
            #
            #         for j in range(len(words)):
            #             ## bleed air
            #             if "ed" == words[j][0][-2:] and "eed" != words[j][0][-3:] and words[j][2] != "NOUN":
            #                 # Ni-based
            #                 if "HYPH" == words[j-1][3]:
            #                     ww = words[j-2][0] + words[j-1][0] + words[j][0]
            #                     properties.append(ww)
            #
            #                 # nickel based
            #                 elif words[j][0] == "based":
            #                     ww = words[j-1][0] + " " + words[j][0]
            #                     properties.append(ww)
            #
            #                 #circumferentially spaced
            #                 elif "ly" == words[j-1][0][-2:]:
            #                     ww = words[j-1][0] + " " + words[j][0]
            #                     properties.append(ww)
            #
            #                 else:
            #                     properties.append(words[j][0])
            #                 # a strip-shaped or band-shaped material
            #                 noun = []
            #
            #             elif properties != []: # and words[j][0] not in string.punctuation:# and j[2] in ["NOUN", "ADJ"]:
            #                 if noun == [] and words[j][0] in self.bad_starting_words:
            #                     continue
            #                 noun.append(words[j][0])
            #
            #
            #         if noun != []:
            #             phrase = " ".join(noun)
            #             ## cleaning the phrase
            #             for i in "/!$%^&*()+_-":
            #                 phrase = phrase.replace(" "+i+" ",i,-1)
            #
            #             if " and " in phrase:
            #                 ph = phrase.split(" ")
            #                 ind = ph.index("and")
            #                 # limited relative radial and circumferential motion
            #                 if ph[ind-1][-3:] == "ial" and ph[ind+1][-3:]=="ial":
            #                     phrase1 = " ".join(ph[0:ind]+ph[ind+2:])
            #                     phrase2 = " ".join(ph[0:ind-1]+ph[ind+1:])
            #                     phrases = [phrase1, phrase2]
            #                 # the desired state and decreasing flow area
            #                 else:
            #                     phrases = phrase.split(" and ")
            #             else:
            #                 phrases = [phrase]
            #
            #             for phrase in phrases:
            #
            #                     while phrase[0] in ",.-_ ":
            #                         phrase = phrase[1:]
            #
            #                     ## print the learned graph
            #                     meta_data = self.claims[counter]["patent_id"] + ","+ self.claims[counter]["claim_num"]
            #                     meta_data += ","+self.claims[counter]["claim_dep"]+","+self.claims[counter]["date"]
            #
            #                     for prop in properties:
            #                         ## filter out some of the weird properties
            #                         if ")" in prop or "(" in prop or "=" in prop:
            #                             continue
            #                         ## make sure that the sentence is ascii
            #                         if not self._is_ascii(prop) or not self._is_ascii(phrase):
            #                             continue
            #
            #                         print bcolors.FAIL + phrase + bcolors.ENDC, "-->", "can be", "-->",
            #                         print bcolors.OKBLUE + prop + bcolors.ENDC, "<-->",
            #                         print bcolors.WARNING + meta_data + bcolors.ENDC
            #
            #                         self.F_ed.write(phrase + " --> can be --> " + prop + " <--> " + meta_data + "\n")
            #                             # print lemmatize(phrase+' can be '+prop)
            #             print "----------------"


    def _is_ascii(self, s):
        return all(ord(c) < 128 for c in s)
