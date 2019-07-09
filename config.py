"""
@author:    chenghao
@desc:      保存宏变量, 包括超参数和路径名
"""

import os
import data

base = os.path.dirname(data.__file__)

# Macros used by searchers

VECTORIZER_PATH = os.path.join(base, 'vectorizer.pkl')
TRIE_PATH = os.path.join(base, 'trie.pkl')
IDX2TITLE_PATH = os.path.join(base, 'idx2title.pkl')
TFIDF_PATH = os.path.join(base, 'tfidf.pkl')

# Macros used by preprocess
SKILL_PATH = '/data/tfidf/skills.txt'
DATA_PATH = '/data/jd_gt_10.pkl'
TITLE2IDX_PATH = '/data/tfidf/title2idx.pkl'
TFIDF_CACHE_PATH = '/data/tfidf/tfidf_cache.pkl'

# Macros used by evaluating
KG_PATH = '/data/tfidf/kg.json'
