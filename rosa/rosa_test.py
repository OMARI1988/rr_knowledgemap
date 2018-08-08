import os, sys, glob
import logging
import getpass
from spacy.lemmatizer import Lemmatizer
from spacy.lang.en import LEMMA_INDEX, LEMMA_EXC, LEMMA_RULES
import networkx as nx

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class ROSA():
    """docstring for ROSA."""
    def __init__(self):
        logger = logging.getLogger("program")
        logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
        logging.root.setLevel(level=logging.INFO)
        logger.info("running %s", ' '.join(sys.argv))
        self.logger = logger
        self.lemmatizer = Lemmatizer(LEMMA_INDEX, LEMMA_EXC, LEMMA_RULES)
        self.user = getpass.getuser()
        self.data_dir = "/media/"+self.user+"/Data4/ROSA/db/"

        self._convert_raw_data_to_graph()

        self.logger.info("ROSA is now live..")

        # self._query()
        while(1):
            text = raw_input("ROSA says: What do you want to know about? ")  # Python 2
            self._query(text)

    def _convert_raw_data_to_graph(self):
        self.G = nx.DiGraph()
        self.folders = sorted([x[0] for x in os.walk(self.data_dir)])
        for folder in self.folders:
            for file_ in glob.glob(folder+"/*.txt"):
                F = open(file_, "r")
                for line in F:
                    line = line.split("\n")[0]
                    data, meta = line.split(" <--> ")
                    source, relation, dist =  data.split(" --> ")
                    lem_source = self._clean(source)        # cleaned and lemmatized
                    lem_dist = self._clean(dist)          # cleaned and lemmatized
                    if self.G.has_edge(lem_source, lem_dist):
                        self.G[lem_source][lem_dist]['weight'] += 1
                    else:
                        self.G.add_edge(lem_source, lem_dist, weight=1)




                break
            # break

    def _query(self, txt):
        Q = self._clean(txt)
        nodes = []
        for node in self.G.nodes():
            if Q in node:
                nodes.append(node)
        nodes = sorted(nodes, key=len)

        edges = []

        print "\n"
        print "============================================================="
        print "results for",txt
        print "============================================================="

        for edge in self.G.edges():
            try:
                if edge[0] == nodes[0]:
                    edges.append((edge[0],edge[1], self.G[edge[0]][edge[1]]["weight"]))
            except:
                pass
        for e in reversed(sorted(edges, key=lambda x: x[2])):
            print bcolors.FAIL + e[0] + bcolors.ENDC, "-->", "can be", "-->",
            print bcolors.OKBLUE + e[1] + bcolors.ENDC,
            print "(" + bcolors.WARNING + str(e[2]) + bcolors.ENDC + ")"


        edges = []

        print "\n"
        print "============================================================="
        print "other results for",txt
        print "============================================================="

        for edge in self.G.edges():
            try:
                if edge[0] in nodes[1:]:
                    edges.append((edge[0],edge[1], self.G[edge[0]][edge[1]]["weight"]))
            except:
                pass
        for e in reversed(sorted(edges, key=lambda x: x[0])):
            print bcolors.FAIL + e[0] + bcolors.ENDC, "-->", "can be", "-->",
            print bcolors.OKBLUE + e[1] + bcolors.ENDC,
            print "(" + bcolors.WARNING + str(e[2]) + bcolors.ENDC + ")"

        print "\n"

    def _clean(self, txt):
        for i in "-_$%":
            txt = txt.replace(i," ",-1)
        txt = txt.replace("  "," ",-1)
        txt = txt.replace("  "," ",-1)
        txt = txt.replace("  "," ",-1)
        return " "+self.lemmatizer(txt, "NOUN")[0]+" "


def main():
    R = ROSA()

if __name__=="__main__":
    main()
