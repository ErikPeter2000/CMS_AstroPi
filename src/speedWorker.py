from worker import Worker




#__________________________________!!!!!!!!!!!!!!!!!!!__________________________
#To be worked on tomorrow
def calculate(match_data):
    #
    return 0

#__________________________________!!!!!!!!!!!!!!!!!!!__________________________
class speedWorker(Worker):
    def __init__(self):
        super().__init__()
        self._Worker__value = 0

    def work(self):
        try:
            pointer = 0  # local variables for number of items in the queue
            while not self.cancelled:  # loop until cancelled
                if not self.queue.empty():
                    item = self.queue.get(
                        False)  # False ensures that we do not wait for an item, which is why wrap this in an if statement as we assume the queue is not empty.

                    speed = calculate(item)

                    self._Worker__value = speed

                    pointer += 1
        except Exception as e:
            print("\n______________________________\n"+str(e)+"\n______________________________\n")  # we'd want to log this somehow in the actual code
        finally:
            self.cancel()

