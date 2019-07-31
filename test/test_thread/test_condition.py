import threading
from collections import deque
import queue as queue2
"""
FIFO队列
with对应内置函数__enter__,__exit__
"""


class Queue:

    def __init__(self):
        self.queue = deque()
        self.mutex = threading.Lock()
        self.not_empty = threading.Condition(self.mutex)
        self.not_full = threading.Condition(self.mutex)
        self.maxsize = 3

    def _qsize(self):
        return len(self.queue)

    def get(self):
        with self.not_empty:
            while not self._qsize():
                self.not_empty.wait()
            item = self.queue.popleft()
            self.not_full.notify()
            return item

    def put(self, item):
        with self.not_full:
            while self._qsize() >= self.maxsize:
                self.not_full.wait()
            self.queue.append(item)
            self.not_empty.notify()


def put(queue):
    for i in range(100):
        queue.put(i)


def get(queue):
    for i in range(100):
        item = queue.get()
        print(item)


queue = Queue()
thread1 = threading.Thread(target=put, args=(queue,))
thread2 = threading.Thread(target=get, args=(queue,))
thread1.start()
thread2.start()
# queue.queue.popleft()
thread1.join()
thread2.join()
