"""For matching images using cv2."""

from exif import Image
from datetime import datetime
import cv2
import numpy as np

class ImagePair:
    """Stores a pair of two images for matching."""
    def __init__(self, cv2image1, cv2image2, timeDifference):
        self.image1 = cv2image1
        self.image2 = cv2image2
        self.resolution = (cv2image1.shape[1], cv2image1.shape[0])
        self.timeDifference = timeDifference

class MatchData:
    """Stores the data needed to calculate the speed."""
    def __init__(self, matches, timeDifference, keypoints1, keypoints2, resolution):
        self.coordinates_1 = []
        self.resolution = resolution
        self.coordinates_2 = []
        for match in matches:
            index1 = match.queryIdx
            index2 = match.trainIdx
            point1 = keypoints1[index1].pt
            point2 = keypoints2[index2].pt
            self.coordinates_1.append(point1)
            self.coordinates_2.append(point2)
        self.timeDifference = timeDifference
    def __len__(self):
        return len(self.coordinates_1)

def getTime(imagePath):
    """Returns the time the image was taken using EXIF and the image timestamp."""
    with open(imagePath, 'rb') as file:
        imagePath = Image(file)
        time = datetime.strptime(imagePath.get("datetime_original"), '%Y:%m:%d %H:%M:%S')
    return time

def timeDifference(imagePath1, imagePath2):
    """The time difference between the two images in seconds given their paths."""
    time1 = getTime(imagePath1)
    time2 = getTime(imagePath2)
    return abs(time1 - time2).total_seconds()

def pathToCv2(imagePath):
    """Converts an image to a cv2 image given its path."""
    image = cv2.imdecode(np.fromfile(imagePath, dtype=np.uint8), cv2.IMREAD_GRAYSCALE)
    return image

def calculateMatches(imagePair):
    """Calculates the matches pixel coordinates for a pair of two images. Returns MatchData."""
    image1 = imagePair.image1
    image2 = imagePair.image2
    # Use cv2 to calculate the matches
    orb = cv2.ORB_create()
    kp1, desc1 = orb.detectAndCompute(image1, None)
    kp2, desc2 = orb.detectAndCompute(image2, None)
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(desc1,desc2)
    # return data necessary to calculate speed
    return MatchData(matches, imagePair.timeDifference, kp1, kp2, imagePair.resolution)