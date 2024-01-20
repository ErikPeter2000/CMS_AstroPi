from exif import Image
from datetime import datetime
import cv2
from pathlib import Path
import matplotlib.pyplot as plt
import time
import os
from picamera import PiCamera

"""
This program finds all matching points in a pair of consecutive images (and does so for all images) then returns it in an array:
[(x1,y1),(x2,y2),timediff] <-would be image pair 'n'

In this version, it only takes k images and finds matching points (not tested on the taking images part on a physical raspberry pi).
It does not use a queue or parallel processing to make this faster.


"""


def matchPoints():
    start_time = time.time()
    base_folder = Path(__file__).parent.resolve()
    image_dir = base_folder / "images"
    cam = PiCamera()
    no_photos = 2 # number of photos to be taken
    timeslice = 1000 # put this in seconds, timeslice is the amount of seconds you have to take all of the photos
    time_inc = ((0.9*timeslice*1000) // no_photos)
    cam.start_preview()

    for i in range(no_photos):
        time.sleep(time_inc)
        cam.capture((image_dir / f'image_{i}.jpg'))

    cam.stop_preview()
    cam.close()

    #here we are just taking a certain number of images (no_photos and time_slice)
    def get_time(image):
        """
        reads metadata of an image and gets the time it was taken
        """
        with open(image, 'rb') as image_file:
            img = Image(image_file)
            time_str = img.get("datetime_original")
            time = datetime.strptime(time_str, '%Y:%m:%d %H:%M:%S')
        return time
    

    def get_time_difference(image_1, image_2):
        """
        Given two images, it gets the time between when each of them were taken
        """
        time_1 = get_time(image_1)
        time_2 = get_time(image_2)
        time_difference = time_2 - time_1
        return time_difference.seconds

    def convert_to_cv(image_1, image_2):
        """
        converts to grayscale, just testing if this improves it at all
        """
        image_1_cv = cv2.imread(str(image_1), 0)
        image_2_cv = cv2.imread(str(image_2), 0)
        return image_1_cv, image_2_cv

    def calculate_features(image_1_cv, image_2_cv, feature_number):
        """
        extracts key points and descriptors from the two images
        """
        orb = cv2.ORB_create(nfeatures=feature_number)
        keypoints_1, descriptors_1 = orb.detectAndCompute(image_1_cv, None)
        keypoints_2, descriptors_2 = orb.detectAndCompute(image_2_cv, None)
        return keypoints_1, keypoints_2, descriptors_1, descriptors_2

    def calculate_matches(descriptors_1, descriptors_2):
        """
        uses cv2s Brute Force Matcher to find matches between the descriptors of the two sets of keypoints
        also sorts the matches based on their distances (matching scores)
        """
        brute_force = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        matches = brute_force.match(descriptors_1, descriptors_2)
        matches = sorted(matches, key=lambda x: x.distance)
        return matches

    def find_matching_coordinates(keypoints_1, keypoints_2, matches):
        """
        Extracts matching (x, y) coordinates for keypoints between two images.

        Parameters:
        - keypoints_1: Keypoints from the first image.
        - keypoints_2: Keypoints from the second image.
        - matches: List of matches between keypoints from both images.

        Returns:
        - coordinates: List of lists, each containing matched (x, y) coordinates.
        """
        coordinates = []
        for match in matches:
            image_1_idx = match.queryIdx
            image_2_idx = match.trainIdx
            (x1, y1) = keypoints_1[image_1_idx].pt
            (x2, y2) = keypoints_2[image_2_idx].pt
            coordinates.append([(x1, y1), (x2, y2)])
        return coordinates

    def analyze_image_pair(image_1, image_2, feature_number=1000):
        """
        Analyzes a pair of images by computing matching keypoints and their coordinates.

        Parameters:
        - image_1: Path to the first image file.
        - image_2: Path to the second image file.
        - feature_number: Number of features to be extracted (default: 1000).

        Returns:
        - List containing matching coordinates and time difference between images.
        """
        time_difference = get_time_difference(image_1, image_2)
        image_1_cv, image_2_cv = convert_to_cv(image_1, image_2)
        keypoints_1, keypoints_2, descriptors_1, descriptors_2 = calculate_features(image_1_cv, image_2_cv,
                                                                                     feature_number)
        matches = calculate_matches(descriptors_1, descriptors_2)
        coordinates = find_matching_coordinates(keypoints_1, keypoints_2, matches)
        return [coordinates, time_difference]

    all_matching_points = []
    image_files = [f for f in os.listdir(image_dir) if f.endswith('.jpg')]

    for i in range(len(image_files) - 1):
        image_1 = image_dir / image_files[i]
        image_2 = image_dir / image_files[i + 1]
        matching_points, time_difference = analyze_image_pair(image_1, image_2)
        all_matching_points.append([matching_points, time_difference])

    print(time.time() - start_time)
    return all_matching_points

if __name__ == "__main__":
    points = matchPoints()

    # Write matching points to a text file
    with open("matching_points.txt", "w") as file:
        for i, matching_data in enumerate(points):
            file.write(f"Image Pair {i + 1}:\n")
            for pair in matching_data[0]:
                file.write(f"Matching Points: {pair}\n")
            file.write(f"TimeDiff: {matching_data[1]}\n")
            file.write("\n")
