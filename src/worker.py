# A class that represents a worker thread that can be cancelled

from queue import Queue

class Worker:
    def __init__(self):
        self.cancelled = False
        self.queue = Queue()
        self.__value = 0
    def work(self):
        pass
    def cancel(self):
        self.cancelled = True

    @property
    def value(self):
        return self.__value