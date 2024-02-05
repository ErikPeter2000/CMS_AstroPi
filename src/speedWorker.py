import math

from worker import Worker
from logzero import logger
from cv2Matcher import calculateMatches

class SpeedWorker(Worker):
    """Worker that calculates the speed from a queue of `ImagePairs`"""
    def __init__(self, gsd):
        """Initializes the worker with a specified Ground Sample Distance (gsd)"""
        super().__init__()
        self.gsd = gsd
        self._Worker__value = 0

    def calculate(self, match_data, gsd):
        coords1 = match_data.coordinates_1
        coords2 = match_data.coordinates_2
        aveDistance = 0
        aveGradient = 0
        score = 0
        if(len(coords1)==0): return (0, -1000000000)
        gradients = []
        speeds = []
        for i in range(0, len(coords1)): # iterate through all the matches and calculate the average distance
            x1 = coords1[i][0]
            y1 = coords1[i][1]
            x2 = coords2[i][0]
            y2 = coords2[i][1]
            d = math.sqrt((x2-x1)**2 + (y2-y1)**2)
            aveDistance += d/len(coords1)
            g = (y2-y1)/(x2-x1)
            gradients.append(g)
            speeds.append(d)
            aveGradient += g/len(coords1)

        for i in range(0, len(coords1)):
            score -= pow(gradients[i]-aveGradient,2)/len(coords1)
            score -= pow(speeds[i]-aveDistance,2)/len(coords1)


        return (aveDistance/match_data.timeDifference*gsd, score)

    def work(self):
        """While not cancelled, calculate and refine a value for speed using the queue of `ImagePairs`"""
        processedCount = 0  # local variables for number of speed values that have been processed
        speednscore = []
        aveScore = 0
        while not self.cancelled:  # loop until cancelled
            try:
                if not self.queue.empty():
                    imagePair = self.queue.get(False)
                    matchData = calculateMatches(imagePair)

                    nspeed, score = self.calculate(matchData, self.gsd)
                    speednscore.append([nspeed, score])
                    speed = self._Worker__value
                    aveScore = (aveScore*processedCount + score)/(processedCount+1)
                    newSpeed = (speed*processedCount + nspeed)/(processedCount+1)
                    processedCount+=1
                    self._Worker__value = newSpeed    
            except Exception as e:
                logger.error(e)

        fSpeed = 0

        for i in range(len(speednscore)):
            speed = speednscore[i][0]
            score = speednscore[i][1]
            normScore = aveScore + abs(score - aveScore)
            normSpeed = (aveScore/normScore)*speed

            fSpeed += normSpeed/len(speednscore)

        self.cancel()

