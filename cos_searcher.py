"""
基于 cos 距离的检索方法，效果不佳
"""

from config import *
import pickle
from time import time
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


class CosSearcher:
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
        print('Done with timecost: %.3f' % (time() - start))

    def search(self, sentence, topk=3):
        sentence = self.trie.cut(sentence)
        if len(sentence) == 0:
            return ['No keyword detected']
        vec = self.vectorizer.transform(sentence)
        result = []
        for i in range(len(self.tfidf)):
            sim = cosine_similarity(vec, self.tfidf[i])
            result.append((sim[0, 0], i))
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