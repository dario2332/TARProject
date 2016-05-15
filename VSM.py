from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import string
from collections import namedtuple


class VSM(object):

    def createVocabulary(self, articles):
        self.vocabulary = set()
        self.articles = []
        for article in articles:
            article = article._replace(text=self.convertTextToVector(article.text))
            self.articles.append(article)
            self.vocabulary |= self.articles[-1].text

    def convertTextToVector(self, text):
        stop = stopwords.words('english') + list(string.punctuation)
        st = PorterStemmer()
        return set([st.stem(i) for i in word_tokenize(text.lower()) if i not in stop])

    def hammingDistance(self, article_vector, query_vector):
        return len(article_vector) + len(query_vector) - 2*len(article_vector & query_vector)

    def retrieveArticles(self, query):
        query_vector = self.convertTextToVector(query)
        scores = []
        for article in self.articles:
            scores.append(self.hammingDistance(article.text, query_vector))
        articles = sorted(zip(self.articles, scores), key = lambda scored_article: scored_article[1])
        return articles




# vsm = VSM()
# Article = namedtuple('Article', ['text', 'name'], verbose=True)
# a = "added a key parameter to specify a function to be called on each list element prior to making"
# b = "The value of the key parameter should be a function that takes a single argument and returns a key to use for sorting purposes. This technique is fast because the key function is called exactly once for each input record."
# c = "Both list.sort() and sorted() accept a reverse parameter with a boolean value. This is using to flag descending sorts. For example, to get the student data in reverse age order:"
# vsm.createVocabulary([Article(a, "a"), Article(b, "b"), Article(c, "c")])
# query = "Both list.sort() and sorted() accept a reverse parameter with a boolean value"
# print map(lambda key: (key[0].name, key[1]), vsm.retrieveArticles(query))
