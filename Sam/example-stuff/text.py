from exif import Image
from datetime import datetime


def get_time(image):
    with open(image, 'rb') as image_file:
        img = Image(image_file)
        for data in img.list_all():
            print(data)


get_time('photo_0683.jpg')