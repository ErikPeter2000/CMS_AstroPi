
import os
from speed_base import *
import math
import numpy as np

image_directory = r"C:\Erik\School\CMS_AstroPI\Images\satellite"
image_files = [f for f in os.listdir(image_directory) if f.endswith('.jpg')]

all_speeds = []

def dotProduct(v1, v2):
    return sum([a*b for a,b in zip(v1,v2)])

# compute weighted average of coordinates based on dot product of vector and overall vector
def processCoords(coordinates1, coordinates2):
    # todo reduce num of of iterations
    vectors = [np.array([c[0][0]-c[1][0], c[0][1]-c[1][1]]) for c in zip(coordinates1, coordinates2)]
    v_x = [v[0] for v in vectors]
    v_y = [v[1] for v in vectors]
    lengths = [np.sqrt(v[0]**2 + v[1]**2) for v in vectors]
    totalLength = np.sum(lengths)
    normalDir = np.array([np.sum(v_x)/totalLength, np.sum(v_y)/totalLength])
    dotProds = [np.dot(v, normalDir) for v in vectors]
    return np.average(lengths, weights=dotProds)


def processImagePair(image_1, image_2):
    time_difference = get_time_difference(image_1, image_2)
    image_1_cv, image_2_cv = convert_to_cv(image_1, image_2)
    points1, points2, desc1, desc2 = calculate_features(image_1_cv, image_2_cv, 1000)
    matches = calculate_matches(desc1, desc2)

    coordinates_1, coordinates_2 = find_matching_coordinates(points1, points2, matches)

    average_feature_distance = processCoords(coordinates_1, coordinates_2)
    speed = calculate_speed_in_kmps(average_feature_distance, 12648, time_difference)
    print(f"Image Pair {i + 1}: {speed} km/s")
    display_matches(image_1_cv, points1, image_2_cv, points2, matches)

    # Append the speed to the list
    all_speeds.append(speed)

for i in range(len(image_files) - 1):
    image_1 = os.path.join(image_directory, image_files[i])
    image_2 = os.path.join(image_directory, image_files[i + 1])

    processImagePair(image_1, image_2)

