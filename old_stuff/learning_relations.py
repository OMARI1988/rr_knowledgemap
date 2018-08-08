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

class spacy_chunks():
    """docstring for spacy_chunks."""
    def __init__(self):
        self.user = getpass.getuser()
        self.project = "2018-08-06-11:45:28-(gas turbine)"
        if os.path.isdir("/media/"+self.user+"/Data4"):
            self.data_dir = "/media/"+self.user+"/Data4/ROSA/analysis/"+self.project+"/"
            self.save_dir = "/media/"+self.user+"/Data4/ROSA/db/"
        elif os.path.isdir("/home/"+self.user+"/Data4"):
            self.data_dir = "/home/"+self.user+"/Data4/ROSA/analysis/2018-08-06-11_45_28-(gas turbine)/"
            self.save_dir = "/home/"+self.user+"/Data4/ROSA/db/"

        self.data_files = sorted(glob.glob(self.data_dir+"*.p"))

        self.claims = {}
        self._read_data()
        self._process_chunks()

    def _read_data(self):
        self.count1 = 60
        self.count2 = 61
        for count,file_ in enumerate(self.data_files):
            print "reading "+file_
            # if "28000-28499" not in file_:
            #     continue

            # if count < self.count1 or count > self.count2:
            #     continue
            R = file_.split("/")[-1].replace("-claims.p","")
            self.claims[R] = cPickle.load( open(file_, "r") )

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

    def _process_chunks(self):
        if not os.path.isdir(self.save_dir):
            os.mkdir(self.save_dir)

        self.F_ed = open(self.save_dir+"raw_ed.txt","w")
        self.unique_chunks = []
        self.unique_codes = {}
        self.bad_starting_words = ["and", "or"]
        for R in self.claims:
            for counter in self.claims[R]:
                self._1_ed_relations(R, counter)


    def _1_ed_relations(self, R, counter):
        for cnk in self.claims[R][counter]["spacy_chunks"]:
            if "ed " in cnk[0]:
                cnk[0] = self._clean_cnk(cnk[0])
                if cnk[0] not in self.unique_chunks:
                    # if "MIN" not in cnk[0]:
                    #     continue
                    print cnk[0]
                    s,e = cnk[1], cnk[2]
                    noun = []
                    properties = []

                    words = self.claims[R][counter]["spacy_data"][s:e]
                    words = self._clean_words(words)

                    for j in range(len(words)):
                        ## bleed air
                        if "ed" == words[j][0][-2:] and "eed" != words[j][0][-3:] and words[j][2] != "NOUN":
                            # Ni-based
                            if "HYPH" == words[j-1][3]:
                                ww = words[j-2][0] + words[j-1][0] + words[j][0]
                                properties.append(ww)

                            # nickel based
                            elif words[j][0] == "based":
                                ww = words[j-1][0] + " " + words[j][0]
                                properties.append(ww)

                            #circumferentially spaced
                            elif "ly" == words[j-1][0][-2:]:
                                ww = words[j-1][0] + " " + words[j][0]
                                properties.append(ww)

                            else:
                                properties.append(words[j][0])
                            # a strip-shaped or band-shaped material
                            noun = []

                        elif properties != []: # and words[j][0] not in string.punctuation:# and j[2] in ["NOUN", "ADJ"]:
                            if noun == [] and words[j][0] in self.bad_starting_words:
                                continue
                            noun.append(words[j][0])


                    if noun != []:
                        phrase = " ".join(noun)
                        ## cleaning the phrase
                        for i in "/!$%^&*()+_-":
                            phrase = phrase.replace(" "+i+" ",i,-1)

                        if " and " in phrase:
                            ph = phrase.split(" ")
                            ind = ph.index("and")
                            # limited relative radial and circumferential motion
                            if ph[ind-1][-3:] == "ial" and ph[ind+1][-3:]=="ial":
                                phrase1 = " ".join(ph[0:ind]+ph[ind+2:])
                                phrase2 = " ".join(ph[0:ind-1]+ph[ind+1:])
                                phrases = [phrase1, phrase2]
                            # the desired state and decreasing flow area
                            else:
                                phrases = phrase.split(" and ")
                        else:
                            phrases = [phrase]

                        for phrase in phrases:

                                while phrase[0] in ",.-_ ":
                                    phrase = phrase[1:]

                                ## print the learned graph
                                meta_data = self.claims[R][counter]["patent_id"] + ","+ self.claims[R][counter]["claim_num"]
                                meta_data += ","+self.claims[R][counter]["claim_dep"]+","+self.claims[R][counter]["date"]

                                for prop in properties:
                                    ## filter out some of the weird properties
                                    if ")" in prop or "(" in prop or "=" in prop:
                                        continue
                                    ## make sure that the sentence is ascii
                                    if not self._is_ascii(prop) or not self._is_ascii(phrase):
                                        continue

                                    print bcolors.FAIL + phrase + bcolors.ENDC, "-->", "can be", "-->",
                                    print bcolors.OKBLUE + prop + bcolors.ENDC, "<-->",
                                    print bcolors.WARNING + meta_data + bcolors.ENDC

                                    print R
                                    self.F_ed.write(phrase + " --> can be --> " + prop + " <--> " + meta_data + "\n")
                                        # print lemmatize(phrase+' can be '+prop)
                        print "----------------"


    def _is_ascii(self, s):
        return all(ord(c) < 128 for c in s)




def main():
    S = spacy_chunks()

if __name__=="__main__":
    main()
