from weight_searcher import WeightSearcher
from cos_searcher import CosSearcher

if __name__ == '__main__':
    searcher = CosSearcher()
    while True:
        s = input('>> ')
        print(searcher.search(s))
