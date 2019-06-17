"""
@author: 成昊
@desc: 对 dataframe 进行分词处理, 生成 tfidf 模型用于匹配
"""
import os
import sys
import pickle
import numpy as np
from config import *
from trie import TrieTree
from sklearn.feature_extraction.text import TfidfVectorizer


def max_pooling(tfidf, title_idx, title_count):
    print('dims: ', tfidf.shape, title_idx.shape, title_count)
    words_dim = tfidf.shape[1]
    result = []
    for _ in range(title_count):
        result.append(np.zeros((1, words_dim)))

    for i in range(tfidf.shape[0]):
        idx = title_idx[i]
        result[idx] = np.max([result[idx], tfidf[i, :].toarray()], axis=0)
    return result


def text2tfidf(text):
    tv = TfidfVectorizer(token_pattern=r"(?u)\b\w+\b")
    try:
        tfidf = tv.fit_transform(text)
    except ValueError:
        print(text)
        assert False
    return tfidf, tv


def run():
    print('Preprocess start')
    with open(DATA_PATH, 'rb') as data_file:
        jds = pickle.load(data_file)
    jds = jds[['职位描述', 'standard_title']]
    print('JD data loaded')

    if os.path.exists('./tfidf_cache.pkl'):
        tfidf, tv = pickle.load(open('./tfidf_cache.pkl', 'rb'))
    else:
        print('Cutting sentence...')
        trie = TrieTree()
        with open(SKILL_PATH, 'r') as f:
            for line in f:
                trie.insert(line.strip())

        with open(TRIE_PATH, 'wb') as f:
            pickle.dump(trie, f)

        cut_jd = []

        for idx, row in jds.iterrows():
            temp = []
            cut = trie.contains(row['职位描述'], dump=True)
            for word in cut:
                temp.append(''.join(word[0]))
            cut_jd.append(' '.join(temp))
            if idx % 1000 == 0 or idx == len(jds)-1:
                sys.stdout.write('\rProcessing %.2f%%' % (100*(idx+1)/len(jds)))
                sys.stdout.flush()
        del jds['职位描述']
        print('Done!')

        print('Converting to TF-IDF...')
        tfidf, tv = text2tfidf(cut_jd)
        print('Done')
        with open('./tfidf_cache.pkl', 'wb') as f:
            pickle.dump((tfidf, tv), f)

    print('Max pooling...')
    title_set = set()
    for title in jds['standard_title']:
        title_set.add(title)
    title2idx = {val: idx for idx, val in enumerate(title_set)}
    idx2title = {idx: val for idx, val in enumerate(title_set)}
    title_idx = [title2idx[title] for title in jds['standard_title']]
    tfidf = max_pooling(tfidf, title_idx, len(title2idx))
    print('Done')

    print('Saving result...')
    with open(TFIDF_PATH, 'wb') as f:
        pickle.dump(tfidf, f)
    with open(TITLE2IDX_PATH, 'wb') as f:
        pickle.dump(title2idx, f)
    with open(IDX2TITLE_PATH, 'wb') as f:
        pickle.dump(idx2title, f)
    with open(VECTORIZER_PATH, 'wb') as f:
        pickle.dump(tv, f)
    print('All done!')


if __name__ == '__main__':
    run()
