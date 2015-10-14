__author__ = 'yokoi-h'

from threading import Condition, Thread
import random
import time


class BlockingQueue(object):

    def __init__(self):
        self.queue = []
        self.condition = Condition()

    def push(self, obj):
        with self.condition:
            self.queue.append(obj)
            self.condition.notify_all()

    def pop(self):
        while True:
            with self.condition:
                if self.queue:
                    return self.queue.pop()
                else:
                    print("wait")
                    self.condition.wait()


class Consumer(Thread):

    def __init__(self, queue):
        super(Consumer, self).__init__()
        self.daemon = True
        self.queue = queue

    def run(self):
        while True:
            print self.queue.pop()


class Producer(Thread):

    def __init__(self, queue):
        super(Producer, self).__init__()
        self.daemon = True
        self.queue = queue

    def run(self):
        while True:
            # self.queue.push(random.randint(0, 256))
            time.sleep(1)

if __name__ == '__main__':
    q = BlockingQueue()
    p = Producer(q)
    c = Consumer(q)
    p.start()
    c.start()

    while True:
        time.sleep(1)