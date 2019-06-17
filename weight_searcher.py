from config import *
import pickle

class WeightSearcher:
    def __init__(self):
        print('WeightSearcher initiating...')
        with open(TFIDF_PATH, 'rb') as f:
            self.tfidf = pickle.load(f).toarray()
        with open(VECTORIZER_PATH, 'rb') as f:
            self.vectorizer = pickle.load(f)
        with open(TITLE2IDX_PATH, 'rb') as f:
            self.idx2title = pickle.load(f)
        with open(TRIE_PATH, 'rb') as f:
            self.trie = pickle.load(f)
        print('Done')

    def search(self, sentence):
        sentence = self.trie.cut(sentence)
        indices = []
        for word in sentence:
            if word in self.vectorizer.vocabulary_:
                indices.append(self.vectorizer.vocabulary_[word])
        idx = 0
        max_val = 0
        for i in range(len(self.tfidf)):
            current = 0
            for j in indices:
                current += self.tfidf[i][j]
            if current > max_val:
                max_val = current
                idx = i
        return self.idx2title[idx]
