import time


class Timer:
    def __init__(self, task):
        super(Timer, self).__init__()
        self.task = task
        self.start = 0

    def __enter__(self):
        print('[%s] start..' % self.task)
        self.start = time.time()

    def __exit__(self, *args):
        print('[%s] finished with time cost: %.3f' % (self.task, time.time() - self.start))


def rec(task):
    return Timer(task)
