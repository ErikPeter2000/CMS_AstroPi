from exif import Image
from datetime import datetime
import cv2
from pathlib import Path
import math
import matplotlib.pyplot as plt
from picamera import PiCamera
import time
import os
start_time = time.time()
base_folder = Path(__file__).parent.resolve()
cam = PiCamera()






cam.capture('/home/pi/Desktop/image.jpg')




def get_time(image):
    with open(image, 'rb') as image_file:
        img = Image(image_file)
        time_str = img.get("datetime_original")
        time = datetime.strptime(time_str, '%Y:%m:%d %H:%M:%S')
    return time

def get_time_difference(image_1, image_2):
    time_1 = get_time(image_1)
    time_2 = get_time(image_2)
    time_difference = time_2 - time_1
    return time_difference.seconds

def convert_to_cv(image_1, image_2):
    image_1_cv = cv2.imread(image_1, 0)
    image_2_cv = cv2.imread(image_2, 0)
    return image_1_cv, image_2_cv

def calculate_features(image_1_cv, image_2_cv, feature_number):
    orb = cv2.ORB_create(nfeatures=feature_number)
    keypoints_1, descriptors_1 = orb.detectAndCompute(image_1_cv, None)
    keypoints_2, descriptors_2 = orb.detectAndCompute(image_2_cv, None)
    return keypoints_1, keypoints_2, descriptors_1, descriptors_2

def calculate_matches(descriptors_1, descriptors_2):
    brute_force = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = brute_force.match(descriptors_1, descriptors_2)
    matches = sorted(matches, key=lambda x: x.distance)
    return matches

def find_matching_coordinates(keypoints_1, keypoints_2, matches):
    coordinates_1 = []
    coordinates_2 = []
    for match in matches:
        image_1_idx = match.queryIdx
        image_2_idx = match.trainIdx
        (x1, y1) = keypoints_1[image_1_idx].pt
        (x2, y2) = keypoints_2[image_2_idx].pt
        coordinates_1.append((x1, y1))
        coordinates_2.append((x2, y2))
    return coordinates_1, coordinates_2

def calculate_mean_distance(coordinates_1, coordinates_2):
    all_distances = 0
    merged_coordinates = list(zip(coordinates_1, coordinates_2))
    for coordinate in merged_coordinates:
        x_difference = coordinate[0][0] - coordinate[1][0]
        y_difference = coordinate[0][1] - coordinate[1][1]
        distance = math.hypot(x_difference, y_difference)
        all_distances = all_distances + distance
    return all_distances / len(merged_coordinates)

def calculate_speed_in_kmps(feature_distance, GSD, time_difference):
    distance = feature_distance * GSD / 100000
    speed = distance / time_difference
    return speed

# Specify the directory containing the image files
image_directory = r'/mnt/c/Users/swmar/CMS/Subject/ComputerScience/code/misc_code/CMS_AstroPI/Sam/example-stuff/images'
# print(os.getcwd())
# Get a list of all image files in the directory
image_files = [f for f in os.listdir(image_directory) if f.endswith('.jpg')]

# Store the speeds for each image
all_speeds = []

# Loop through consecutive image pairs
for i in range(len(image_files) - 1):
    # Form the complete paths for consecutive image pairs
    image_1 = os.path.join(image_directory, image_files[i])
    image_2 = os.path.join(image_directory, image_files[i + 1])

    # Perform the existing analysis for each pair
    time_difference = get_time_difference(image_1, image_2)
    image_1_cv, image_2_cv = convert_to_cv(image_1, image_2)
    keypoints_1, keypoints_2, descriptors_1, descriptors_2 = calculate_features(image_1_cv, image_2_cv, 1000)
    matches = calculate_matches(descriptors_1, descriptors_2)
    coordinates_1, coordinates_2 = find_matching_coordinates(keypoints_1, keypoints_2, matches)
    average_feature_distance = calculate_mean_distance(coordinates_1, coordinates_2)
    speed = calculate_speed_in_kmps(average_feature_distance, 12648, time_difference)

    # Append the speed to the list
    all_speeds.append(speed)
cam.close()
# Print all speeds
n=3
all_speeds_filtered = [num for num in all_speeds]
# all_speeds_filtered = all_speeds_filter_one[len(all_speeds)//n:(n-1)*len(all_speeds)//n]
print(sum(all_speeds)/len(all_speeds))
print("Speeds for each image pair:")
for i, speed in enumerate(all_speeds_filtered, start=1):
    print(f"Image Pair {i}: {speed} km/s")
print(f"Image Pair MEAN: {sum(all_speeds_filtered)/(len(all_speeds_filtered))} km/s")

print("RUNTIME:",time.time()-start_time)

plt.plot([ele for ele in range(len(all_speeds_filtered))],all_speeds_filtered)
plt.savefig("fig1.png")