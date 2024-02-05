"""Manages dumping sensor data to a csv."""

from sense_hat import SenseHat
from datetime import datetime
import os
import shutil
from logzero import logger
from datetime import datetime

DATA_CAPACITY_BYTES = 250000000 # 250MB
APPROXIMATE_IMAGE_SIZE_BYTES = 5000000 # 5MB

class SensorDumpWrapper:
    """Manages dumping sensor data to a csv and saving images."""
    def __init__(self, directory):
        # create the dump folder
        self.dumpFolder = os.path.join(directory,"dump")
        os.makedirs(self.dumpFolder, exist_ok=True)
        # create and open the csv file
        self.csvPath = os.path.join(self.dumpFolder, "data.csv")
        self.file = open(self.csvPath, "w")
        # set an index to the number of images in the dump folder
        self.imageIndex = len(os.listdir(self.dumpFolder))
        # write the csv header
        self.file.write("time,yaw,pitch,roll,compassNorth,magnetometerX,magnetometerY,magnetometerZ,gyroscopeX,gyroscopeY,gyroscopeZ,accelerometerX,accelerometerY,accelerometerZ\n")
        
    def record(self):
        """Records sensor data to the csv file."""
        orientation = SenseHat().get_orientation()
        compassNorth = SenseHat().get_compass()
        magnetometer = SenseHat().get_compass_raw()
        gyroscope = SenseHat().get_gyroscope_raw()
        accelerometer = SenseHat().get_accelerometer_raw()
        data = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%s:%f')}{orientation['yaw']},{orientation['pitch']},{orientation['roll']},{compassNorth},{magnetometer['x']},{magnetometer['y']},{magnetometer['z']},{gyroscope['x']},{gyroscope['y']},{gyroscope['z']},{accelerometer['x']},{accelerometer['y']},{accelerometer['z']}"
        logger.info(f"Sensor Data: {data}")
        self.file.write(data + "\n")

    def copyImage(self, path):
        """Copies an image to the dump folder. The image is renamed to the current time."""
        if (not os.path.exists(path)):
            logger.error(f"Image {path} does not exist. Could not copy to data folder.")
            return
        imageName = datetime.now().strftime("image_%Y-%m-%d%_H%:M%:S:%f") + ".jpg"
        imagePath = os.path.join(self.dumpFolder, imageName)
        shutil.copy(path, imagePath)
        self.imageIndex += 1
        logger.info(f"Image {path} saved to {imagePath}")

    @property
    def dataSize(self):
        "returns the size of the data folder in bytes"
        return sum(os.path.getsize(f) for f in os.listdir(self.dumpFolder) if os.path.isfile(f))
    
    @property
    def remainingCapacity(self):
        "returns the remaining capacity of the data folder in bytes"
        return DATA_CAPACITY_BYTES - self.dataSize()

    @property
    def spaceRemaining(self):
        "returns True if there is enough space remaining to store an image"
        return self.remainingCapacity() > self.approxImageSize

    def close(self):
        self.file.flush()
        self.file.close()    

    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_value, traceback):
        self.close()