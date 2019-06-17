from weight_searcher import WeightSearcher

if __name__ == '__main__':
    ws = WeightSearcher()
    while True:
        s = input('>> ')
        print(ws.search(s))
