"""
基于传统加权和的检索方法
"""


from config import *
import pickle
from rec import rec


class WeightSearcher:
    def __init__(self):
        with rec('WeightSearcher Initiation'):
            with open(TFIDF_PATH, 'rb') as f:
                self.tfidf = pickle.load(f)
            with open(VECTORIZER_PATH, 'rb') as f:
                self.vectorizer = pickle.load(f)
            with open(IDX2TITLE_PATH, 'rb') as f:
                self.idx2title = pickle.load(f)
            with open(TRIE_PATH, 'rb') as f:
                self.trie = pickle.load(f)

    def search(self, sentence, topk=3, verbose=False):
        with rec('WeightSearcher', verbose):
            sentence = self.trie.cut(sentence)
            if len(sentence) == 0:
                raise ValueError('No keyword detected!')
            indices = []
            for word in sentence:
                if word in self.vectorizer.vocabulary_:
                    indices.append(self.vectorizer.vocabulary_[word])
            result = []
            for i in range(self.tfidf.shape[0]):
                current = 0
                for j in indices:
                    current += self.tfidf[i][0, j]
                result.append((current, i))
            result.sort(reverse=True)
        return [self.idx2title[result[i][1]] for i in range(topk)]
