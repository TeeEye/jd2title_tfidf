"""
@author:    chenghao
@desc:      统计耗时的小工具
"""

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
            print('[%s] starting..' % self.task)
        self.start = time.time()

    def __exit__(self, *args):
        global _total_time_cost
        time_cost = time.time() - self.start
        _total_time_cost[self.task] += time_cost
        if self.verbose:
            print('[%s] finished with time cost: %.5fs' % (self.task, time_cost))


def rec(task, verbose=True):
    """
    工厂函数, 返回一个 Timer 实例
    :param task: 任务描述字符串
    :param verbose: 是否打印耗时
    :return: Timer 实例
    """
    return Timer(task, verbose)


def reset(key):
    """
    根据 key 重置总耗时
    :param key: Timer 的 task 值
    """
    global _total_time_cost
    _total_time_cost[key] = 0


def get_total_time_cost(key):
    """
    根据 key 获取总耗时
    :param key: Timer 的 task 值
    """
    return _total_time_cost[key]
