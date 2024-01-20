from exif import Image
from datetime import datetime
import cv2
import math
import numpy as np
from pathlib import Path

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

def convert_to_cv(image_1, image_2, gamma=2):
    image_1_cv = cv2.imread(image_1)
    image_2_cv = cv2.imread(image_2)

    # Crop the central part of the images
    central_fraction = 0.6  # Adjust the fraction as needed
    h, w = image_1_cv.shape
    central_h, central_w = int(h * central_fraction), int(w * central_fraction)
    start_h, start_w = (h - central_h) // 2, (w - central_w) // 2

    image_1_cv = image_1_cv[start_h:start_h + central_h, start_w:start_w + central_w]
    image_2_cv = image_2_cv[start_h:start_h + central_h, start_w:start_w + central_w]

    # Apply gamma correction for contrast adjustment
    image_1_cv = np.power(image_1_cv / 255.0, gamma) * 255.0
    image_2_cv = np.power(image_2_cv / 255.0, gamma) * 255.0
    image_1_cv = np.uint8(image_1_cv)
    image_2_cv = np.uint8(image_2_cv)

    # Apply blur to the images
    blur_size = (15, 15)  # Adjust the kernel size as needed
    image_1_blurred = cv2.GaussianBlur(image_1_cv, blur_size, 5)
    image_2_blurred = cv2.GaussianBlur(image_2_cv, blur_size, 5)

    # Save the first blurred image as "BLURBLURBLAH.jpg"
    cv2.imwrite("BLURBLURBLAH.jpg", image_1_blurred)

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
    coordinates_1 = [(keypoints_1[match.queryIdx].pt[0], keypoints_1[match.queryIdx].pt[1]) for match in matches]
    coordinates_2 = [(keypoints_2[match.trainIdx].pt[0], keypoints_2[match.trainIdx].pt[1]) for match in matches]
    return coordinates_1, coordinates_2

def calculate_speed_in_kmps(line_distance, GSD, time_difference):
    distance = line_distance * GSD / 100000
    speed = distance / time_difference
    return speed

def calculate_line_distance(coordinates_1, coordinates_2, original_size, cropped_size):
    # Fit a line through the matching points
    line_params = np.polyfit(np.array(coordinates_1)[:, 0], np.array(coordinates_1)[:, 1], 1)

    # Calculate the distance along the line between the first and last points
    x1, y1 = coordinates_1[0]
    x2, y2 = coordinates_1[-1]
    original_line_distance = np.abs(line_params[0] * x2 - y2 + line_params[1]) / np.sqrt(line_params[0]**2 + 1)

    # Scale the distance based on the ratio of original image size to cropped image size
    size_ratio = original_size[0] / cropped_size[0]
    line_distance = original_line_distance * size_ratio

    return line_distance, line_params

# Assuming the images are in the same directory as the script
script_directory = Path(__file__).resolve().parent
image_files = sorted([f for f in script_directory.glob('*.jpg')])

all_speeds = []

for i in range(len(image_files) - 1):
    image_1 = image_files[i]
    image_2 = image_files[i + 1]

    time_difference = get_time_difference(image_1, image_2)
    image_1_cv, image_2_cv = convert_to_cv(str(image_1), str(image_2))
    keypoints_1, keypoints_2, descriptors_1, descriptors_2 = calculate_features(image_1_cv, image_2_cv, 1000)
    matches = calculate_matches(descriptors_1, descriptors_2)
    coordinates_1, coordinates_2 = find_matching_coordinates(keypoints_1, keypoints_2, matches)
    line_distance, line_params = calculate_line_distance(coordinates_1, coordinates_2, image_1_cv.shape, image_1_cv.shape)
    speed = calculate_speed_in_kmps(line_distance, 12648, time_difference)
    all_speeds.append(speed)

    # Save the image with the line displaying the median gradient
    line_img = np.zeros_like(image_1_cv)
    for coord in coordinates_1:
        cv2.circle(line_img, (int(coord[0]), int(coord[1])), 1, 255, -1)
    x_vals = np.array([coord[0] for coord in coordinates_1])
    y_vals = line_params[0] * x_vals + line_params[1]
    for i in range(len(x_vals) - 1):
        cv2.line(line_img, (int(x_vals[i]), int(y_vals[i])), (int(x_vals[i + 1]), int(y_vals[i + 1])), 255, 1)

    cv2.imwrite(f"line_image_{i}.jpg", line_img)

# Exclude anomalies using standard deviation
mean_speed = np.mean(all_speeds)
std_dev_speed = np.std(all_speeds)
filter_multiplier = 2
filtered_speeds = [spd for spd in all_speeds if abs(spd - mean_speed) < filter_multiplier * std_dev_speed]

# Calculate the average speed
average_speed = np.mean(filtered_speeds)

# Print the results
print(f"Mean Speed for all pairs (excluding anomalies): {mean_speed} km/s")
print(f"Average Speed for all pairs (excluding anomalies): {average_speed} km/s")

# Calculate and print the values as you did
val1 = (mean_speed / (0.6 ** 2))
val2 = (average_speed / (0.6 ** 2))
print("Mean Speed:", mean_speed)
print("Average Speed:", average_speed)
print("Value 1:", val1)
print("Value 2:", val2)
print("Average of Values:", (val1 + val2) / 2)
