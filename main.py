from weight_searcher import WeightSearcher
# from cos_searcher import CosSearcher

if __name__ == '__main__':
    print('--* Interactive JD2Title *--')
    searcher = WeightSearcher(verbose=True)
    while True:
        try:
            s = input('>> ')
            print(searcher.search(s))
        except UnicodeDecodeError:
            print('UnicodeDecode Error')
            continue
