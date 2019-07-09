import os
import data

base = os.path.dirname(data.__file__)

SKILL_PATH = '/data/tfidf/skills.txt'
DATA_PATH = '/data/jd_gt_10.pkl'
TITLE2IDX_PATH = '/data/tfidf/title2idx.pkl'
IDX2TITLE_PATH = os.path.join(base, 'idx2title.pkl')
TFIDF_PATH = os.path.join(base, 'tfidf.pkl')
TFIDF_CACHE_PATH = '/data/tfidf/tfidf_cache.pkl'
VECTORIZER_PATH = os.path.join(base, 'vectorizer.pkl')
TRIE_PATH = os.path.join(base, 'trie.pkl')
KG_PATH = '/data/tfidf/kg.json'
