import math

from worker import Worker
from logzero import logger




#__________________________________!!!!!!!!!!!!!!!!!!!__________________________
#To be worked on tomorrow
def calculate(match_data):
    c1 = match_data.coordinates_1
    c2 = match_data.coordinates_2
    td = match_data.timeDifference
    av_d = 0
    for i in range(0, len(c1)):
        x1 = c1[i][0]
        y1 = c1[i][1]
        x2 = c2[i][0]
        y2 = c2[i][1]
        d = math.sqrt((x2-x1)**2 + (y2-y1)**2)
        av_d = (av_d*i + d)/(i+1)
    return av_d/td

#__________________________________!!!!!!!!!!!!!!!!!!!__________________________
class speedWorker(Worker):
    def __init__(self):
        super().__init__()
        self._Worker__value = 0

    def work(self):
        count = 0  # local variables for number of items in the queue
        while not self.cancelled:  # loop until cancelled
            try:
                if not self.queue.empty():
                    item = self.queue.get(False)
                    count+=1
                    speed = self._Worker__value
                    speed = (speed*count + calculate(item))/(count+1)
                    self._Worker__value = speed    
            except Exception as e:
                logger.error(e)
        self.cancel()

