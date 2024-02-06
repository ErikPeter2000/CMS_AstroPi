# This Worker class contains the method for a thread.
# It handles the cancellation of the thread using the thread-safe "threading.Event".
# The derived class must implement the "work()" method, and will check for the cancellation flag.
# The "Queue" is used to store the data that the worker method will process. The queue is a thread-safe collection.

from queue import Queue
import threading

class Worker:
    """Represents a worker that can be cancelled and has a value"""
    def __init__(self):
        self.__cancelFlag = threading.Event()
        self.queue = Queue()
        self.__value = 0
    def work(self):
        """While not cancelled, do work"""
        pass
    def cancel(self):
        """Cancels the worker. The `work()` method must check `cancelled` to see if it should stop working."""
        self.__cancelFlag.set()

    @property
    def value(self):
        return self.__value
    
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_value, traceback):
        self.cancel()