from weight_searcher import WeightSearcher
from cos_searcher import CosSearcher

if __name__ == '__main__':
    searcher = WeightSearcher()
    while True:
        try:
            s = input('>> ')
            print(searcher.search(s))
        except UnicodeDecodeError:
            continue