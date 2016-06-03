from loadXML import get_texts
from VSM import VSM, BinaryVSM
import numpy as np
import sys
import pickle
from Evaluation import evaluate, getRelevances
from PageRank import pageRank
from links import createAdjacencyMatrix, createLinksSmart, getQueryNum
import math

def combineScores(vsm_score, pr_score, articles, w=0.7):
    results = sorted(zip(articles, vsm_score), key = lambda scored_article: scored_article[1])
    results.reverse()
    results = map(lambda x: x[0], results)

    rank = np.zeros((len(vsm_score)))
    for i, article in enumerate(articles):
        rank[i] = results.index(article) + 1

    return w * vsm_score + (1-w) * pr_score / (rank + math.log(5))
    

def main():
    #texts, queries = get_texts()

    #H = createAdjacencyMatrix(texts)
    #pickle.dump(H, open("Pickle/H200", "wb"))
    #H = pickle.load(open("Pickle/H200", "rb"))
  
    #pr_score = pageRank(H)
    #pickle.dump(pr_score, open("Pickle/PRScore", "wb"))
    #pr_score = pickle.load(open("Pickle/PRScore", "rb"))
    texts = pickle.load(open("Pickle/texts", "rb")) 
    queries = pickle.load(open("Pickle/queries", "rb")) 

    #vsm = BinaryVSM()
    #vsm.createVocabulary(texts)

    #pickle.dump(texts, open("Pickle/texts", "wb"))
    #pickle.dump(queries, open("Pickle/queries", "wb"))
    #pickle.dump(vsm, open("Pickle/BinaryVSM", "wb"))

    #vsm = pickle.load(open("Pickle/VSM", "rb")) 
    vsm = pickle.load(open("Pickle/BinaryVSM", "rb")) 

    #H = createLinksSmart(map(lambda x: x.text, vsm.articles))

    #pickle.dump(pr_score, open("Pickle/PRScoreSmart", "wb"))
    pr_score = pickle.load(open("Pickle/PRScoreSmart", "rb"))
    #vsm = VSM(texts)
    #pickle.dump(vsm, open("Pickle/VSM", "wb"))
    #print "loaded"
    #print vsm.vocabulary
    #print len(vsm.vocabulary)

    relevances = getRelevances()
    for query in queries:
        scores = vsm.retrieveArticles(query)
        #scores = np.array(scores)
        #scores = scores * pr_score

        scores = combineScores(np.array(scores), pr_score, map(lambda x: x.name, texts))
        results = sorted(zip(texts, scores), key = lambda scored_article: scored_article[1])
        results.reverse()

        lines = []
        for res in results:
            lines.append(res[0].name + " " + str(res[1]) + "\n")
        with open("Results/" + query.name, "w") as f:
            f.writelines(lines)
        evaluate("Results/" + query.name, getQueryNum(query.name), relevances)

if __name__ == "__main__":
    main()


