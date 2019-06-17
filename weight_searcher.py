from config import *
import pickle

class WeightSearcher:
    def __init__(self):
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
        print('Done')

    def search(self, sentence, topk = 3):
        sentence = self.trie.cut(sentence)
        indices = []
        print(sentence)
        for word in sentence:
            print(word)
            if word in self.vectorizer.vocabulary_:
                print(self.vectorizer.vocabulary_[word])
                indices.append(self.vectorizer.vocabulary_[word])
        result = []
        for i in range(len(self.tfidf)):
            current = 0
            for j in indices:
                current += self.tfidf[i][0, j]
            result.append((current, i))
        result.sort(reverse=True)
        return [self.idx2title[result[i][1]] for i in range(topk)]
