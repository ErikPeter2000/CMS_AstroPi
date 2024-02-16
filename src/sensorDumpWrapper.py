# Manages dumping sensor data to a csv.

from sense_hat import SenseHat
from datetime import datetime
import os
import shutil
from logzero import logger
from datetime import datetime

DATA_CAPACITY_BYTES = 260000000 # 260MB
IMAGE_LIMIT= 41
APPROXIMATE_IMAGE_SIZE_BYTES = 5000000 # 5MB

# The header of the all sensor data
HEADER = "time,yaw,pitch,roll,compassNorth,magnetometerX,magnetometerY,magnetometerZ,gyroscopeX,gyroscopeY,gyroscopeZ,accelerometerX,accelerometerY,accelerometerZ,humidity,temperature,pressure"

class SensorDumpWrapper:
    """Manages dumping sensor data to a csv and saving images."""
    def __init__(self, directory):
        # create and open the csv file
        self.csvPath = os.path.join(self.dumpFolder, "data.csv")
        self.file = open(self.csvPath, "w")
        # set an index to the number of images in the dump folder that are jpgs
        self.imageIndex = len([f for f in os.listdir(self.dumpFolder) if f.endswith('.jpg')])
        # write the csv header
        self.file.write(HEADER + '\n')
        self.sense_hat = SenseHat()
        
    def record(self):
        """Records sensor data to the csv file."""
        # get sensor data
        orientation = self.sense_hat.get_orientation()
        compassNorth = self.sense_hat.get_compass()
        magnetometer = self.sense_hat.get_compass_raw()
        gyroscope = self.sense_hat.get_gyroscope_raw()
        accelerometer = self.sense_hat.get_accelerometer_raw()
        humidity = self.sense_hat.get_humidity()
        temperature = self.sense_hat.get_temperature()
        pressure = self.sense_hat.get_pressure()
        # format data
        dataExact = [datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f'),orientation['yaw'],orientation['pitch'],orientation['roll'],compassNorth,magnetometer['x'],magnetometer['y'],magnetometer['z'],gyroscope['x'],gyroscope['y'],gyroscope['z'],accelerometer['x'],accelerometer['y'],accelerometer['z'],humidity,temperature,pressure]
        dataRounded = [round(x, 2) if isinstance(x, float) else x for x in dataExact]
        # write data to file
        dataStr = ",".join(map(str, dataRounded))
        self.file.write(dataStr + '\n')
        # also recorded rounded values to the log
        dataRoundedStr = ",".join(map(str, dataRounded))
        logger.info(f"Recorded Data: {dataRoundedStr}")

    def copyImage(self, path):
        """Copies an image to the dump folder. The image is renamed to the current time."""
        imageSize = os.path.getsize(path)
        if (not os.path.exists(path)):
            logger.error(f"Image {path} does not exist. Could not copy to data folder.")
            return
        elif (not self.spaceRemaining(imageSize)):
            logger.warn(f"Insufficient space remaining to store image {path}.")
            return
        elif (self.imageIndex >= IMAGE_LIMIT):
            logger.warn(f"Image limit reached. Could not store image {path}.")
            return
        else:
            imageName = f"image_{datetime.now().strftime('%Y-%m-%d_%H%M%S%f')}.jpg"
            imagePath = os.path.join(self.dumpFolder, imageName)
            shutil.copy(path, imagePath)
            self.imageIndex += 1
            logger.info(f"Image {path} by name {imageName}. {self.imageIndex}/{IMAGE_LIMIT} images marked for return.")

    @property
    def dataSize(self):
        "returns the size of the dump folder in bytes"
        return sum(os.path.getsize(f) for f in os.listdir(self.dumpFolder) if os.path.isfile(f))
    
    @property
    def remainingCapacity(self):
        "returns the remaining capacity of the data folder in bytes"
        return DATA_CAPACITY_BYTES - self.dataSize
    
    def spaceRemaining(self, size):
        "returns True if there is enough space remaining to store a file of size 'size'"
        return self.remainingCapacity > size

    def close(self):
        self.file.flush()
        self.file.close()

    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
