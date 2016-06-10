from nltk import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import string
from collections import namedtuple
import numpy as np
from scipy import spatial
from scipy.spatial import distance
import math

def convertTextToVector(text):
    stop = stopwords.words('english') + list(string.punctuation)
    st = PorterStemmer()
    sent_token_list = sent_tokenize(text)
    words = []
    for sent in sent_token_list:
        words += word_tokenize(sent)
    return [st.stem(word.lower()) for word in words if word.lower() not in stop]
    #return [st.stem(i) for i in word_tokenize(text.lower()) if i not in stop]

class BinaryVSM(object):

    def createVocabulary(self, articles):
        self.vocabulary = set()
        self.articles = []
        for article in articles:
            article = article._replace(text=set(convertTextToVector(article.text)))
            self.articles.append(article)
            self.vocabulary |= self.articles[-1].text

    def hammingDistance(self, article_vector, query_vector):
        return len(article_vector) + len(query_vector) - 2*len(article_vector & query_vector)

    @staticmethod
    def cosine(article_vector, query_vector):
        return len(article_vector & query_vector) / math.sqrt(len(article_vector)) / math.sqrt(len(query_vector))
        
    @staticmethod
    def dice(article_vector, query_vector):
        return 2*len(article_vector & query_vector) / (len(article_vector) +len(query_vector))
        
    def retrieveArticles(self, query, similarity_measure="cosine"):
        query_vector = set(convertTextToVector(query.text))
        scores = []
        for article in self.articles:
            if similarity_measure == "cosine":
                scores.append(BinaryVSM.cosine(article.text, query_vector))
            elif similarity_measure == "dice":
                scores.append(BinaryVSM.dice(article.text, query_vector))
        return scores
        articles = sorted(zip(self.articles, scores), key = lambda scored_article: scored_article[1])
        articles.reverse()
        return articles

class Document(object):
    def __init__(self, article):
        self.name = article.name
        vector = convertTextToVector(article.text)
        self.terms = {}
        self.vector = None
        self.freq_vector = None
        for term in vector:
            self.terms[term] = self.terms.get(term, 0) + 1

    def freq(self, term):
        return self.terms.get(term, 0)

    #term frequency
    def tf(self, vocabulary=None):
        if (self.vector != None):
            return self.vector
        self.vector = np.zeros(len(vocabulary))
        for i, term in enumerate(vocabulary):
            self.vector[i] = self.freq(term)
        maxFreq = max(self.terms.values())
        self.vector = 0.5 + 0.5*self.vector/maxFreq
        return self.vector
    
    def freqVector(self, vocabulary=None):
        if (self.freq_vector != None):
            return self.freq_vector
        self.freq_vector = np.zeros(len(vocabulary))
        for i, term in enumerate(vocabulary):
            self.freq_vector[i] = self.freq(term)
        return self.freq_vector


def filter(a):
    if a != 0.5:
        return 1
    else:
        return 0

class VSM(object):

    def __init__(self, articles):
        self.vocabulary = {}
        self.articles = []
        for article in articles:
            self.articles.append(Document(article))
            for term in self.articles[-1].terms:
                self.vocabulary[term] = self.vocabulary.get(term, 0) + self.articles[-1].freq(term)

        self.idf = np.zeros(len(self.vocabulary))
        ones = np.ones(len(self.vocabulary))
        vfilter = np.vectorize(filter)
        for article in self.articles:
            tf = article.tf(self.vocabulary.keys())
            self.idf += vfilter(tf)
        self.idf = np.log(len(articles) / self.idf)

    def retrieveArticles(self, query):
        query = Document(query)
        scores = []
        for article in self.articles:
            document_vector = self.idf * article.tf()
            query_vector = self.idf * query.tf(self.vocabulary.keys())

            scores.append(1-distance.cosine(document_vector, query_vector))
        articles = sorted(zip(self.articles, scores), key = lambda scored_article: scored_article[1])
        return articles



#Article = namedtuple('Article', ['text', 'name'], verbose=True)
#a = "added a key"
#b = "The value of the key key"
#c = "boolean value."
#vsm = VSM([Article(a, "a"), Article(b, "b"), Article(c, "c")])
#query = Article("add value", "q")
#vsm.retrieveArticles(query)

