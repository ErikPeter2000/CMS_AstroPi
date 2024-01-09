# This code is an example of using two threads to process data in 'parallel'.
# The main thread will be used to get data from the camera and send it to the worker thread via a queue.
# The 'Worker' class defines the basic behaviour of a background task. It contains a queue to store data to be processed.
# The 'Worker' is then inherited by a derived class that, in this example, calculates the mean by dequeuing numbers from the inherited queue.
# Please note that AstroPi will be picky about using threads. Please don't block execution in the background thread and handle exceptions properly.

import threading
from queue import Queue
import time

# Worker class that will contain the code for the second thread
class Worker:
    def __init__(self):
        self.cancelled = False # flag to cancel thread from main thread. Must not be changed in this code.
        self.queue = Queue() # queue to store data to be processed by the thread. This will probably be match data in the actual code.
    def work(self): # method to be overridden by derived class.
        pass
    def cancel(self): # method to cancel the thread from the main thread. We could just assign 'cancelled' to true from outside the thread, but this is better practice.
        self.cancelled = True

# Derived worker class that will calculate specific data - in this case a mean of the inputted values. In the actual code, this will calculate the speed of the satellite.
# Timur, David, Yotam and Jasper will work on this.
class MeanWorker(Worker):
    def __init__(self): # constructor, any constants such as GSD can also be specified here as parameters, but shouldn't be changed from outside the thread.
        super().__init__() # call constructor of base class. This is necessary.
        self.__mean = 0 # data to be processed by the thread. This will be the speed of the satellite in the actual code.
    def work(self):
        try:            
            count = 0 # local variables for number of items in the queue
            while not self.cancelled: # loop until cancelled
                if not self.queue.empty():
                    item = self.queue.get(False) # False ensures that we do not wait for an item, which is why why wrap this in an if statement
                    self.__mean = (self.__mean*count + item)/(count+1) # calculate mean
                    count+=1
        except Exception as e:
            print(e) # we'd want to log this somehow in the actual code
            self.cancel() # cancel thread if an exception occurs

    @property
    def mean(self): # getter for mean. We could just access the variable from outside the class, but this is better practice for thread safety.
        return self.__mean

# main thread, will be written by Erik and Sam
if __name__ == "__main__":
    # setup worker and thread
    worker = MeanWorker()
    thread = threading.Thread(target=worker.work)
    thread.start()
    # main loop
    print("Enter a non-number to exit.")
    while True:
        try:
            #input data and push number to queue. In the actual code, the data can be the image matches, timestamps, estimated heading, etc.
            data = int(input("Number: "))
            worker.queue.put(data)
        except ValueError: # if input is not a number, exit loop
            print(f"Mean: {worker.mean}")
            worker.cancel()
            break
    

    # this is just a check to see if the thread has finished. It is not necessary for the program to work.
    time.sleep(0.1) # Sleep for 100ms
    if thread.is_alive():
        print("Thread should be finished by now...")
    
    
    thread.join() # wait for thread to finish. This is necessary to 'cleanly' exit the program.