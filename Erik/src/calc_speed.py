
import os
from speed_base import *

image_directory = 'C:\\Erik\School\\CMS_AstroPI\\Images\\satellite'
image_files = [f for f in os.listdir(image_directory) if f.endswith('.jpg')]

all_speeds = []

for i in range(len(image_files) - 1):
    image_1 = os.path.join(image_directory, image_files[i])
    image_2 = os.path.join(image_directory, image_files[i + 1])

    time_difference = get_time_difference(image_1, image_2)
    image_1_cv, image_2_cv = convert_to_cv(image_1, image_2)
    keypoints_1, keypoints_2, descriptors_1, descriptors_2 = calculate_features(image_1_cv, image_2_cv, 1000)
    matches = calculate_matches(descriptors_1, descriptors_2)
    coordinates_1, coordinates_2 = find_matching_coordinates(keypoints_1, keypoints_2, matches)
    average_feature_distance = calculate_mean_distance(coordinates_1, coordinates_2)
    speed = calculate_speed_in_kmps(average_feature_distance, 12648, time_difference)
    print(f"Image Pair {i + 1}: {speed} km/s")
    display_matches(image_1_cv, keypoints_1, image_2_cv, keypoints_2, matches)

    # Append the speed to the list
    all_speeds.append(speed)

# Print all speeds
n=3
all_speeds_filtered = all_speeds[len(all_speeds)//n:(n-1)*len(all_speeds)//n]
print(sum(all_speeds)/len(all_speeds))
print("Speeds for each image pair:")
for i, speed in enumerate(all_speeds_filtered, start=1):
    print(f"Image Pair {i}: {speed} km/s")
print(f"Image Pair MEAN: {sum(all_speeds_filtered)/(len(all_speeds_filtered))} km/s")

print("RUNTIME:",time.time()-start_time)

plt.plot([ele for ele in range(len(all_speeds_filtered))],all_speeds_filtered)
plt.savefig("fig1.png")