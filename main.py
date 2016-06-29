from loadXML import get_texts
from VSM import VSM, BinaryVSM
import numpy as np
import sys
import pickle
from Evaluation import evaluate, getRelevances, evaluateEverything
from PageRank import pageRank
from HITS import HITS
from links import createAdjacencyMatrix, createLinksSmart, getQueryNum
import math
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.spatial import distance

def combineScores(vsm_score, pr_score, articles, with_rank=False, w=0.7):
    if with_rank:
        results = sorted(zip(articles, vsm_score), key = lambda scored_article: scored_article[1])
        results.reverse()
        results = map(lambda x: x[0], results)

        rank = np.zeros((len(vsm_score)))
        for i, article in enumerate(articles):
            rank[i] = results.index(article) + 1

        return w * vsm_score + (1-w) * pr_score / (np.log(rank) + math.log(5))
    return w * vsm_score + (1-w) * pr_score
    
def evaluate(texts, queries, vsm):
    relevances = getRelevances()
    vsm_scores = []
    for query in queries:
        vsm_scores.append(np.array(vsm.retrieveArticles(query)))

    for scores, query in zip(vsm_scores, queries):
        results = sorted(zip(texts, scores), key = lambda scored_article: scored_article[1])
        results.reverse()
            
        lines = []
        for res in results:
            lines.append(res[0].name + " " + str(res[1]) + "\n")
        with open("Results/" + query.name, "w") as f:
            f.writelines(lines)
    print "Only VSM:"
    evaluateEverything()

    for treshold in np.arange(0.4, 1, 0.1):
        L = createLinksSmart(map(lambda x: x.text, vsm.articles), treshold=treshold)
        pr_score = pageRank(L)
        hits_score, _ = HITS(L)
        for link_score, link_name in zip([pr_score, hits_score], ["PageRank", "HITS"]):
            for w in np.arange(0.5, 1, 0.1):
                for rank in [True, False]:
                    for scores, query in zip(vsm_scores, queries):
                        scores = combineScores(np.array(scores), link_score, map(lambda x: x.name, texts), with_rank=rank,  w=w)
                        results = sorted(zip(texts, scores), key = lambda scored_article: scored_article[1])
                        results.reverse()
                
                        lines = []
                        for res in results:
                            lines.append(res[0].name + " " + str(res[1]) + "\n")
                        with open("Results/" + query.name, "w") as f:
                            f.writelines(lines)
                    print "Treshold: ", treshold, " ", link_name, " w: ", w, " rank: ", rank
                    evaluateEverything()


def main():
    print "Loading documents..."
    texts, queries = get_texts()

    #pickle.dump(pr_score, open("Pickle/PRScore", "wb"))
    #pr_score = pickle.load(open("Pickle/PRScore", "rb"))
    #texts = pickle.load(open("Pickle/texts", "rb")) 
    #queries = pickle.load(open("Pickle/queries", "rb")) 

    print "Creating vocabulary..."
    vsm = BinaryVSM()
    vsm.createVocabulary(texts)

    #pickle.dump(texts, open("Pickle/texts", "wb"))
    #pickle.dump(queries, open("Pickle/queries", "wb"))
    #pickle.dump(vsm, open("Pickle/BinaryVSM", "wb"))

    #vsm = pickle.load(open("Pickle/VSM", "rb")) 
    #vsm = pickle.load(open("Pickle/BinaryVSM", "rb")) 

    
    #evaluate(texts, queries, vsm)
    print "Creating links..."
    H = createLinksSmart(map(lambda x: x.text, vsm.articles), 0.7)
    print "Creating PageRank scores..."
    pr_score = pageRank(H)
    print "Creating HITS scores..."
    hits_score, _ = HITS(H)
    #print len(vsm.vocabulary)

    #relevances = getRelevances()
    while True:
        print "[1] VSM, [2] VSM + PageRank, [3] VSM + HITS, [4] exit, Start: "
        answer = raw_input("")
        if answer == "4": break
        else:
            for query in queries:
                scores = vsm.retrieveArticles(query)

                if answer == "2":
                    scores = combineScores(np.array(scores), pr_score, map(lambda x: x.name, texts), True, w=0.7)
                elif answer == "3":
                    scores = combineScores(np.array(scores), hits_score, map(lambda x: x.name, texts), True, w=0.6)

                results = sorted(zip(texts, scores), key = lambda scored_article: scored_article[1])
                results.reverse()


                lines = []
                for res in results:
                    lines.append(res[0].name + " " + str(res[1]) + "\n")
                with open("Results/" + query.name, "w") as f:
                    f.writelines(lines)
            evaluateEverything()

if __name__ == "__main__":
    main()


