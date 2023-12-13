from exif import Image
from datetime import datetime
import cv2
import math
import matplotlib.pyplot as plt
import time
import os

start_time = time.time()

def get_time(image):
    with open(image, 'rb') as image_file:
        img = Image(image_file)
        time_str = img.get("datetime_original")
        time = datetime.strptime(time_str, '%Y:%m:%d %H:%M:%S')
    return time

def get_time_difference(image_1, image_2):
    time_1 = get_time(image_1)
    time_2 = get_time(image_2)
    return (time_2 - time_1).seconds

def convert_to_cv(image_1, image_2):
    return cv2.imread(image_1, 0), cv2.imread(image_2, 0)

def calculate_features(image_1_cv, image_2_cv, feature_number):
    orb = cv2.ORB_create(nfeatures=feature_number)
    return orb.detectAndCompute(image_1_cv, None), orb.detectAndCompute(image_2_cv, None)

def calculate_matches(descriptors_1, descriptors_2):
    brute_force = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    return sorted(brute_force.match(descriptors_1, descriptors_2), key=lambda x: x.distance)

def find_matching_coordinates(keypoints_1, keypoints_2, matches):
    return [(keypoints_1[match.queryIdx].pt, keypoints_2[match.trainIdx].pt) for match in matches]

def calculate_mean_distance(coordinates_1, coordinates_2):
    merged_coordinates = list(zip(coordinates_1, coordinates_2))
    return sum(math.hypot(coordinate[0][0] - coordinate[1][0], coordinate[0][1] - coordinate[1][1]) for coordinate in merged_coordinates) / len(merged_coordinates)

def calculate_speed_in_kmps(feature_distance, GSD, time_difference):
    return (feature_distance * GSD / 100000) / time_difference

def display_matches(image_1_cv, keypoints_1, image_2_cv, keypoints_2, matches):
    match_img = cv2.drawMatches(image_1_cv, keypoints_1, image_2_cv, keypoints_2, matches[:100], None)
    resize = cv2.resize(match_img, (1600,600), interpolation = cv2.INTER_AREA)
    cv2.imshow('matches', resize)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

image_directory = 'C:\\Erik\School\\CMS_AstroPI\\Sam\\example-stuff\\images'
image_files = [f for f in os.listdir(image_directory) if f.endswith('.jpg')]