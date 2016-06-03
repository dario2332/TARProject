import numpy as np
from VSM import BinaryVSM

def getArticleNum(name):
    return int(name.split('-')[1].split('.')[0])

def getQueryNum(name):
    return int(name.split('.')[0][5:])

def createAdjacencyMatrix(articles):
    H = np.zeros((len(articles), len(articles)))
    for i, article1 in enumerate(articles):
        article_num1 = getArticleNum(article1.name)
        for j, article2 in enumerate(articles[i+1:]):
            article_num2 = getArticleNum(article2.name)
            if (abs(article_num2-article_num1) <= 200):
                H[i][j] = 1
                H[j][i] = 1
            
    row_sums = H.sum(axis=1)
    for i, s in enumerate(row_sums):
        if s > 0:
            H[i] /= s
    return H


#binary articles expected
def createLinksSmart(articles):
    H = np.zeros((len(articles), len(articles)))
    for i, article1 in enumerate(articles):
        for j, article2 in enumerate(articles[i+1:]):
            similarity = BinaryVSM.cosine(article1, article2)
            if similarity > 0.8:
                H[i][j] = 1
                H[j][i] = 1
            
    row_sums = H.sum(axis=1)
    for i, s in enumerate(row_sums):
        if s > 0:
            H[i] /= s
    return H

