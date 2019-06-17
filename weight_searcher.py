from config import *
import pickle

class WeightSearcher:
    def __init__(self):
        print('WeightSearcher initiating...')
        with open(TFIDF_PATH, 'rb') as f:
            self.tfidf = pickle.load(f).toarray()
        with open(VECTORIZER_PATH, 'rb') as f:
            self.vectorizer = pickle.load(f)
        with open(IDX2TITLE_PATH, 'rb') as f:
            self.idx2title = pickle.load(f)
        print('Done')

    def search(self, sentence):
        pass
