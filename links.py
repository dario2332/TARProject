import numpy as np
from VSM import BinaryVSM

def getArticleNum(name):
    return int(name.split('-')[1].split('.')[0])

def getQueryNum(name):
    return int(name.split('.')[0][5:])

def createAdjacencyMatrix(articles):
    L = np.zeros((len(articles), len(articles)))
    for i, article1 in enumerate(articles):
        article_num1 = getArticleNum(article1.name)
        for j, article2 in enumerate(articles[i+1:]):
            article_num2 = getArticleNum(article2.name)
            if (abs(article_num2-article_num1) <= 200):
                L[i][j] = 1
                L[j][i] = 1
    return L


#binary articles expected
def createLinksSmart(articles):
    L = np.zeros((len(articles), len(articles)))
    for i, article1 in enumerate(articles):
        for j, article2 in enumerate(articles[i+1:]):
            similarity = BinaryVSM.cosine(article1, article2)
            if similarity > 0.8:
                L[i][j] = 1
                L[j][i] = 1
    return L

