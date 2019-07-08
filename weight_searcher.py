"""
基于传统加权和的检索方法
"""


from config import *
import pickle
from time import time
import numpy as np
from rec import rec


class WeightSearcher:
    def __init__(self):
        start = time()
        print('WeightSearcher initiating...')
        with open(TFIDF_PATH, 'rb') as f:
            self.tfidf = pickle.load(f)
        with open(VECTORIZER_PATH, 'rb') as f:
            self.vectorizer = pickle.load(f)
        with open(IDX2TITLE_PATH, 'rb') as f:
            self.idx2title = pickle.load(f)
        with open(TRIE_PATH, 'rb') as f:
            self.trie = pickle.load(f)
        print('Done with timecost: %.3f, title count: %d' % ((time() - start), len(self.tfidf)))

    def search(self, sentence, topk=3):
        with rec('WeightSearcher', False):
            sentence = self.trie.cut(sentence)
            if len(sentence) == 0:
                return ['No keyword detected']
            indices = []
            for word in sentence:
                if word in self.vectorizer.vocabulary_:
                    indices.append(self.vectorizer.vocabulary_[word])
            result = []
            for i in range(len(self.tfidf)):
                current = 0
                for j in indices:
                    current += self.tfidf[i][0, j]
                result.append((current, i))
            result.sort(reverse=True)
        return [self.idx2title[result[i][1]] for i in range(topk)]

    def eval(self, summary, jd, topk=1):
        assert len(summary) == len(jd)
        result = []
        for i in range(len(summary)):
            c_titles = self.search(summary[i], topk)
            j_titles = self.search(jd[i], topk)
            match = 0
            for j in c_titles:
                for k in j_titles:
                    if j == k:
                        match = 1

            result.append(match)
        return np.array(result)

    def match(self, jd, title, topk=1):
        result = []
        for i in range(len(jd)):
            j_titles = self.search(jd[i], topk)
            match = 0
            for j in j_titles:
                if j == title[i]:
                    match = 1

            result.append(match)
        return np.array(result)
