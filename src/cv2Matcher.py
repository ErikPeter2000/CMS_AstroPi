"""For matching images using cv2."""

from exif import Image
from datetime import datetime
import cv2
import numpy as np

class MatchData:
    """Stores the data needed to calculate the speed."""
    def __init__(self, matches, timeDifference, keypoints1, keypoints2):
        self.coordinates_1 = []
        self.coordinates_2 = []
        for match in matches:
            index1 = match.queryIdx
            index2 = match.trainIdx
            (x1,y1) = keypoints1[index1].pt
            (x2,y2) = keypoints2[index2].pt
            self.coordinates_1.append((x1,y1))
            self.coordinates_2.append((x2,y2))
        self.timeDifference = timeDifference
    def __len__(self):
        return len(self.coordinates_1)

def getTime(imagePath):
    """Returns the time the image was taken using EXIF."""
    with open(imagePath, 'rb') as file:
        imagePath = Image(file)
        time = datetime.strptime(imagePath.get("datetime_original"), '%Y:%m:%d %H:%M:%S')
    return time

def timeDifference(imagePath1, imagePath2):
    """The time difference between the two images in seconds given their paths."""
    time1 = getTime(imagePath1)
    time2 = getTime(imagePath2)
    return abs(time1 - time2).total_seconds()

def imageToCv2(imagePath):
    """Converts an image to a cv2 image given its path."""
    image = cv2.imread(str(imagePath), 0)
    return image


def calculateMatches(imagePath1, imagePath2):
    """Calculates the matches pixel coordinates for two images given their paths. Returns MatchData."""
    image1 = imageToCv2(imagePath1)
    image2 = imageToCv2(imagePath2)
    orb = cv2.ORB_create()
    kp1, desc1 = orb.detectAndCompute(image1, None)
    kp2, desc2 = orb.detectAndCompute(image2, None)
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(desc1,desc2)
    return MatchData(matches, timeDifference(imagePath1, imagePath2), kp1, kp2)