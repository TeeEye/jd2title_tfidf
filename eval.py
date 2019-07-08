from weight_searcher import WeightSearcher
import pickle
from config import DATA_PATH


if __name__ == '__main__':
    ws = WeightSearcher()
    data = pickle.load(open(DATA_PATH, 'rb'))

    data_len = 10000
    data = data.sample(frac=data_len/len(data))

    right = 0

    for _, row in data.iterrows():
        result = ws.search(row['job_description'], topk=3)
        flag = False
        for res in result:
            if res == row['standard_title']:
                flag = True
        if flag:
            right += 1

    print("accuracy: %lf" % (right/len(data)))
