# This is the implementation of the "Worker" class
# The "Work()" method will run in the background and calculate the speed from the queue of "ImagePairs".
# When cancelled, the "work()" method will return promptly.

import math

from worker import Worker
from logzero import logger
from statisticsUtils import meanAndDeviation, standardDeviationAngles, weightedMeanPairsWithDiscard
import cv2Matcher

# Constants
# These values are used to determine the score for speed according to a function.
# Speeds outside the 1kms^-1 start to become penalised considerably.
ACCEPTANCE = 1 # Value that increases the power in the score calculation. Higher acceptance means values with a higher deviation get a higher score
EXPECTED = 7.66
EXPECTED_FALLOFF = 4 # The acceptance for deviations around the mean. Higher falloff means the acceptance is higher for speed values further from 7.66
REJECTION = 2 # Value that increases the denomination in the score calculation. Higher rejection means values with a higher deviation get a lower score
DISTANCE_DEV_SCALE = 0.1 # Value that scales the deviation of the distance. Corrects the deviation to be more in line with the deviation of the angle
ANGLE_DEV_SCALE = 10 # Value that scales the deviation of the angle. Corrects the deviation to be more in line with the deviation of the distance
DISCARD_PERCENTILE = 20 # Percentile of values to discard before calculating the weighted mean

class SpeedWorker(Worker):
    """Worker that calculates the speed from a queue of `ImagePairs`"""
    def __init__(self, gsd):
        """Worker that calculates the speed from a queue of `ImagePairs`"""
        super().__init__()
        self.gsd = gsd
        self._Worker__value = 0

    def calculateScore(self, speed, d0, d1):
        """Calculate the score from speed and two deviations (distance and angle)."""
        # A bell curve is formed by considering the speed, distance deviation.
        m = REJECTION ** ACCEPTANCE
        devDenominator = m*(d0**2+d1**2)**ACCEPTANCE
        speedDenominator = (REJECTION*(speed-EXPECTED)**EXPECTED_FALLOFF)
        return 1/(devDenominator*speedDenominator+1)

    def calculateSpeedFromMatches(self, match_data, gsd):
        """Returns the speed and score from a set of matches and a specified Ground Sample Distance (gsd)"""
        # extract coordinates from match data
        coords1 = match_data.coordinates_1
        coords2 = match_data.coordinates_2
        time = match_data.timeDifference
        if len(coords1) == 0:
            return (0,0)
        
        # iterate through matches and find gradients and distances
        distances = []
        angles = []
        for i in range(0, len(coords1)):
            x1 = coords1[i][0]
            y1 = coords1[i][1]
            x2 = coords2[i][0]
            y2 = coords2[i][1]
            distance = math.sqrt((x2-x1)**2 + (y2-y1)**2)*gsd
            distances.append(distance)
            angle = math.atan2((y2-y1),(x2-x1))
            angles.append(angle)

        # calculate the mean and deviations for distance and angle
        meanDistance, devDistance = meanAndDeviation(distances)
        meanSpeed = meanDistance/time
        devAngle = standardDeviationAngles(angles)
        devDistance*=DISTANCE_DEV_SCALE
        devAngle*=ANGLE_DEV_SCALE
        
        score = self.calculateScore(meanSpeed, devDistance, devAngle)
        return (meanSpeed, score)

    def work(self):
        """While not cancelled, calculate and refine a value for speed using the queue of `ImagePairs`"""
        try:
            speedScorePairs = [] # list of speed and score pairs, for calculating the weighted mean
            logger.info("SpeedWorker: Working...")
            while not self._Worker__cancelFlag.is_set(): # loop until cancelled. Uses the thread-safe `Event` to check if the worker is cancelled.
                if not self.queue.empty():
                    # get pair and compute matches
                    imagePair = self.queue.get(False)
                    try:
                        matchData = cv2Matcher.calculateMatches(imagePair)

                        # calculate speed score and append to list
                        speed, score = self.calculateSpeedFromMatches(matchData, self.gsd)
                        speedScorePairs.append((speed, score))

                        # calculate new speed from list by a weighted mean, discarding anomalies
                        newSpeed = weightedMeanPairsWithDiscard(speedScorePairs, DISCARD_PERCENTILE)
                        logger.info(f"Calculated Speed: {speed}, {score}. Average Speed: {newSpeed}")
                        self._Worker__value = newSpeed
                    except Exception as e:
                        logger.error(f"Error occurred while calculating speed with: \n{e}")
        finally:
            self.cancel() # ensure the worker is marked as cancelled when the loop ends.

