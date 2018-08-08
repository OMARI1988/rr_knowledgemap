import sys,glob,os
import getpass
import logging
import datetime
import cPickle
import spacy
import numpy as np
import string

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
        elif os.path.isdir("/home/"+self.user+"/Data4"):
            self.data_dir = "/home/mo/Data4/ROSA/analysis/2018-08-06-11_45_28-(gas turbine)/"
        self.data_files = sorted(glob.glob(self.data_dir+"*.p"))

        self.claims = {}
        self._read_data()
        self._print_chunks()

    def _read_data(self):
        for count,file_ in enumerate(self.data_files):
            print "reading "+file_
            if count < 0 or count > 5:
                continue
            R = file_.split("/")[-1].replace("-claims.p","")
            self.claims[R] = cPickle.load( open(file_, "r") )

    def _clean_cnk(self, txt):
        txt = txt.replace("&lt;sub&gt;","",-1)
        return txt

    def _clean_words(self, words):
        for i in range(len(words)):
            words[i][0] = words[i][0].replace("&lt;sub&gt;","",-1)
            words[i][0] = words[i][0].replace("&lt;/sub&gt;","",-1)
            words[i][0] = words[i][0].replace("&lt;/sub&gt","",-1)
        return words

    def _print_chunks(self):
        self.unique_chunks = []
        self.unique_codes = {}
        bad_starting_words = ["and", "or"]
        for R in self.claims:
            for counter in self.claims[R]:
                for cnk in self.claims[R][counter]["spacy_chunks"]:
                    if "ed " in cnk[0]:
                        cnk[0] = self._clean_cnk(cnk[0])
                        if cnk[0] not in self.unique_chunks:
                            # if "bleed" not in cnk[0]:
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
                                    if noun == [] and words[j][0] in bad_starting_words:
                                        continue
                                    noun.append(words[j][0])


                            if noun != []:
                                phrase = " ".join(noun)
                                ## cleaning the phrase
                                for i in "/!$%^&*()_-":
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
                                        for prop in properties:
                                            print bcolors.FAIL + phrase + bcolors.ENDC, "-->", "can be", "-->", bcolors.OKBLUE + prop + bcolors.ENDC
                                print "----------------"


def main():
    S = spacy_chunks()

if __name__=="__main__":
    main()
