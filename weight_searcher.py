from config import *
import pickle
from time import time

class WeightSearcher:
    def __init__(self):
        start = time()
        print('WeightSearcher initiating...')
        with open(TFIDF_PATH, 'rb') as f:
            self.tfidf = pickle.load(f)
            print(len(self.tfidf))
        with open(VECTORIZER_PATH, 'rb') as f:
            self.vectorizer = pickle.load(f)
        with open(IDX2TITLE_PATH, 'rb') as f:
            self.idx2title = pickle.load(f)
        with open(TRIE_PATH, 'rb') as f:
            self.trie = pickle.load(f)
        print('Done with timecost: %.3f' % (time() - start))

    def search(self, sentence, topk = 3):
        sentence = self.trie.cut(sentence)
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
