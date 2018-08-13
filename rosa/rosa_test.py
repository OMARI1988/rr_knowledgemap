import os, sys, glob
import logging
import getpass
from spacy.lemmatizer import Lemmatizer
from spacy.lang.en import LEMMA_INDEX, LEMMA_EXC, LEMMA_RULES
import networkx as nx
import cPickle

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
    def __init__(self, process):
        self.process = process
        logger = logging.getLogger("program")
        logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
        logging.root.setLevel(level=logging.INFO)
        logger.info("running %s", ' '.join(sys.argv))
        self.logger = logger
        self.lemmatizer = Lemmatizer(LEMMA_INDEX, LEMMA_EXC, LEMMA_RULES)
        self.user = getpass.getuser()
        if os.path.isdir("/media/"+self.user+"/Data4/ROSA/db/"):
            self.data_dir = "/media/"+self.user+"/Data4/ROSA/db/"
            self.save_dir = "/media/"+self.user+"/Data4/ROSA/graph/"
        else:
            self.data_dir = "/home/"+self.user+"/Data4/ROSA/db/"
            self.save_dir = "/home/"+self.user+"/Data4/ROSA/graph/"

        if self.process == "update":
            self._convert_raw_data_to_graph()
        # elif self.process == "run":
        self._load_graph()

        self.logger.info("ROSA is now live..")

        while(1):
            text = raw_input("ROSA says: What do you want to know about? ")  # Python 2
            self._query(text)

    def _load_graph(self):
        self.logger.info("loading ROSA graph...")
        self.G = nx.read_gpickle(self.save_dir+"knowledge_graph.p")

    def _convert_raw_data_to_graph(self):
        if os.path.isfile(self.save_dir+"learned_files.p"):
            self.learned_files = cPickle.load( open(self.save_dir+"learned_files.p", "r") )
            self.G = nx.read_gpickle(self.save_dir+"knowledge_graph.p")
        else:
            self.learned_files = []
            self.G = nx.DiGraph()

        self.folders = sorted([x[0] for x in os.walk(self.data_dir)])
        # counter = 0
        for folder in self.folders:
            for file_ in glob.glob(folder+"/*.txt"):
                file_flag = 1
                if file_ not in self.learned_files:
                    print "processing "+file_
                    F = open(file_, "r")
                    for line in F:
                        try:
                            line = line.split("\n")[0]
                            data, meta = line.split(" <--> ")
                            source, relation, dist =  data.split(" --> ")
                            lem_source = self._clean(source)        # cleaned and lemmatized
                            lem_dist = self._clean(dist)          # cleaned and lemmatized
                            if self.G.has_edge(lem_source, lem_dist):
                                self.G[lem_source][lem_dist]['weight'] += 1
                            else:
                                self.G.add_edge(lem_source, lem_dist, weight=1)
                        except:
                            file_flag = 0
                            print "Bad line"
                    if file_flag:
                        self.learned_files.append(file_)
                    # counter += 1
            #     if counter >= 10000:
            #         break
            # if counter >= 10000:
            #     break

        if not os.path.isdir(self.save_dir):
            os.mkdir(self.save_dir)
        self.logger.info("saving ROSA graph...")
        nx.write_gpickle(self.G, self.save_dir+"knowledge_graph.p")
        cPickle.dump(self.learned_files, open(self.save_dir+"learned_files.p", "w"))




                # break
            # break

    def _query(self, txt):
        Q = self._clean(txt)
        if self.G.has_node(Q):
             edges = self.G.edges(Q,data='weight')
             edges = sorted(edges, key=lambda x: x[2])
             for e in reversed(sorted(edges, key=lambda x: x[2])):
                 print bcolors.FAIL + e[0] + bcolors.ENDC, "-->", "can be", "-->",
                 print bcolors.OKBLUE + e[1] + bcolors.ENDC,
                 print "(" + bcolors.WARNING + str(e[2]) + bcolors.ENDC + ")"
        # nodes = []
        # for node in self.G.nodes():
        #     if Q in node:
        #         nodes.append(node)
        # nodes = sorted(nodes, key=len)
        #
        # edges = []
        #
        # print "\n"
        # print "============================================================="
        # print "results for",txt
        # print "============================================================="
        #
        # for edge in self.G.edges():
        #     try:
        #         if edge[0] == nodes[0]:
        #             edges.append((edge[0],edge[1], self.G[edge[0]][edge[1]]["weight"]))
        #     except:
        #         pass
        # for e in reversed(sorted(edges, key=lambda x: x[2])):
        #     print bcolors.FAIL + e[0] + bcolors.ENDC, "-->", "can be", "-->",
        #     print bcolors.OKBLUE + e[1] + bcolors.ENDC,
        #     print "(" + bcolors.WARNING + str(e[2]) + bcolors.ENDC + ")"
        #
        #
        # edges = []
        #
        # print "\n"
        # print "============================================================="
        # print "other results for",txt
        # print "============================================================="
        #
        # for edge in self.G.edges():
        #     try:
        #         if edge[0] in nodes[1:]:
        #             edges.append((edge[0],edge[1], self.G[edge[0]][edge[1]]["weight"]))
        #     except:
        #         pass
        # for e in reversed(sorted(edges, key=lambda x: x[0])):
        #     print bcolors.FAIL + e[0] + bcolors.ENDC, "-->", "can be", "-->",
        #     print bcolors.OKBLUE + e[1] + bcolors.ENDC,
        #     print "(" + bcolors.WARNING + str(e[2]) + bcolors.ENDC + ")"
        #
        # print "\n"

    def _clean(self, txt):
        for i in "-_$%":
            txt = txt.replace(i," ",-1)
        txt = txt.replace("  "," ",-1)
        txt = txt.replace("  "," ",-1)
        txt = txt.replace("  "," ",-1)
        return " "+self.lemmatizer(txt, "NOUN")[0]+" "


def main(argv):
    process = ""
    if "update" in argv[0]:
        process = "update"
    if "run" in argv[0]:
        process = "run"
    if process == "":
        print "please chose one of the following"
        print "python rosa/rosa_test.py run # to run and load the graph model"
        print "python rosa/rosa_test.py update # to update the graph model with new relations then run"
        sys.exit(1)

    R = ROSA(process)

if __name__=="__main__":
    main(sys.argv[1:])
