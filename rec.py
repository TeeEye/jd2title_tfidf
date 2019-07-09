import time
from collections import defaultdict

_total_time_cost = defaultdict(int)


class Timer:
    def __init__(self, task, verbose):
        super(Timer, self).__init__()
        self.task = task
        self.start = 0
        self.verbose = verbose

    def __enter__(self):
        if self.verbose:
            print('[%s] start..' % self.task)
        self.start = time.time()

    def __exit__(self, *args):
        global _total_time_cost
        time_cost = time.time() - self.start
        _total_time_cost[self.task] += time_cost
        if self.verbose:
            print('[%s] finished with time cost: %.3f' % (self.task, time_cost))


def rec(task, verbose=True):
    return Timer(task, verbose)


def reset(key):
    global _total_time_cost
    _total_time_cost[key] = 0


def get_total_time_cost(key):
    return _total_time_cost[key]
