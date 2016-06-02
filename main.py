from loadXML import get_texts
from VSM import VSM, BinaryVSM
import numpy as np
import sys
import pickle
from Evaluation import evaluate, getRelevances

def getArticleNum(name):
    return int(name.split('-')[1].split('.')[0])

def getQueryNum(name):
    return int(name.split('.')[0][5:])

def createAdjacencyMatrix(articles):
    H = np.zeros((len(articles), len(articles)))
    for i, article1 in enumerate(articles):
        article_num1 = getArticleNum(article1)
        for j, article2 in enumerate(articles[i+1:]):
            article_num2 = getArticleNum(article2)
            if (abs(article_num2-article_num1) <= 200):
                H[i][j] = 1
                H[j][i] = 1
            
    row_sums = H.sum(axis=1)
    for i, s in enumerate(row_sums):
        if s > 0:
            H[i] /= s
    return H


def main():
    #texts, queries = get_texts()

    texts = pickle.load(open("Pickle/texts", "rb")) 
    queries = pickle.load(open("Pickle/queries", "rb")) 

    #vsm = BinaryVSM()
    #vsm.createVocabulary(texts)

    #pickle.dump(texts, open("Pickle/texts", "wb"))
    #pickle.dump(queries, open("Pickle/queries", "wb"))
    #pickle.dump(vsm, open("Pickle/BinaryVSM", "wb"))

    #vsm = pickle.load(open("Pickle/VSM", "rb")) 
    vsm = pickle.load(open("Pickle/BinaryVSM", "rb")) 

    #vsm = VSM(texts)
    #pickle.dump(vsm, open("Pickle/VSM", "wb"))
    print "loaded"
    #print vsm.vocabulary
    print len(vsm.vocabulary)

    relevances = getRelevances()
    for query in queries:
        results = vsm.retrieveArticles(query)
        lines = []
        for res in results:
            lines.append(res[0].name + " " + str(res[1]) + "\n")
        with open("Results/" + query.name, "w") as f:
            f.writelines(lines)
        evaluate("Results/" + query.name, getQueryNum(query.name), relevances)

if __name__ == "__main__":
    main()


