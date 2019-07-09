"""
@author:    chenghao
@desc:      基于传统加权和的检索方法的搜索器
"""


from config import *
from rec import rec

import pickle
import numpy as np


class WeightSearcher:
    def __init__(self, verbose=False):
        """
        初始化
        :param verbose: 是否显示耗时统计等信息
        """
        self.verbose = verbose
        self.name = 'WeightSearcher'
        with rec('%s Initiation' % self.name, verbose):
            with open(TFIDF_PATH, 'rb') as f:
                self.tfidf = pickle.load(f)
                self.tfidf = np.array(self.tfidf.toarray())
            with open(VECTORIZER_PATH, 'rb') as f:
                self.vectorizer = pickle.load(f)
            with open(IDX2TITLE_PATH, 'rb') as f:
                self.idx2title = pickle.load(f)
            with open(TRIE_PATH, 'rb') as f:
                self.trie = pickle.load(f)

    def search(self, jd, topk=3):
        """
        根据 jd 描述来返回匹配的 title
        :param jd: jd 描述字符串
        :param topk: 候选个数
        :return: title 字符串 list
        """
        with rec('%s Search' % self.name, verbose=self.verbose):
            sentence = self.trie.cut(jd)
            if len(sentence) == 0:
                raise ValueError('No keyword detected!')
            indices = np.zeros((len(self.vectorizer.vocabulary_), 1))
            for word in sentence:
                if word in self.vectorizer.vocabulary_:
                    indices[self.vectorizer.vocabulary_[word], 0] += 1
            result = []
            for i in range(self.tfidf.shape[0]):
                res = np.dot(self.tfidf[i, :], indices)
                result.append((res, i))
            result.sort(reverse=True)
        return [self.idx2title[result[i][1]] for i in range(topk)]
