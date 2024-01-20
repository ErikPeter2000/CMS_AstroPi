from queue import Queue

class Worker:
    """Represents a worker that can be cancelled and has a value"""
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
    
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_value, traceback):
        self.cancel()