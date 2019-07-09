"""
@author:    chenghao
@desc:      交互式测试
"""

from weight_searcher import WeightSearcher

if __name__ == '__main__':
    print('--* Interactive JD2Title *--')
    searcher = WeightSearcher(verbose=True)
    while True:
        try:
            s = input('>> ')
            if s == 'quit' or s == 'exit':
                print('Bye.')
                break
            print(searcher.search(s))
        except UnicodeDecodeError:
            print('UnicodeDecodeError')
            continue
