import os
import numpy as np
import shutil
from datetime import datetime
from logzero import logger


HEADER = "time,yaw,pitch,roll,compassNorth,magnetometerX,magnetometerY,magnetometerZ,gyroscopeX,gyroscopeY,gyroscopeZ,accelerometerX,accelerometerY,accelerometerZ,humidity,temperature,pressure"

class SenseHat:
    def randomXYZ(self, sigma=1.0, mu=0.0):
        x = np.random.normal(mu, sigma)
        y = np.random.normal(mu, sigma)
        z = np.random.normal(mu, sigma)
        return {'x': x, 'y': y, 'z': z}

    def randomRollPitchYaw(self, sigma=1.0, mu=0.0):
        roll = np.random.normal(mu, sigma)
        pitch = np.random.normal(mu, sigma)
        yaw = np.random.normal(mu, sigma)
        return {'roll': roll, 'pitch': pitch, 'yaw': yaw}

    def get_orientation(self):
        return self.randomRollPitchYaw()
    def get_compass(self):
        return np.random.normal(0, 1)
    def get_compass_raw(self):
        return self.randomXYZ(10)
    def get_gyroscope_raw(self):
        return self.randomXYZ(10)
    def get_accelerometer_raw(self):
        return self.randomXYZ(100)
    def get_humidity(self):
        return np.random.normal(30, 10)
    def get_temperature(self):
        return np.random.normal(21, 3)
    def get_pressure(self):
        return np.random.normal(1000, 20)

class SensorDumpWrapper:
    """Manages dumping sensor data to a csv and saving images."""
    def __init__(self, directory):
        self.__counter = 0
        # create the dump folder
        self.dumpFolder = os.path.join(directory,"dump")
        os.makedirs(self.dumpFolder, exist_ok=True)
        # create and open the csv file
        self.csvPath = os.path.join(self.dumpFolder, "data.csv")
        self.file = open(self.csvPath, "w")
        # set an index to the number of images in the dump folder
        self.imageIndex = len(os.listdir(self.dumpFolder))
        # write the csv header
        self.file.write(HEADER + '\n')

    def record(self):
        """Records sensor data to the csv file."""
        orientation = SenseHat().get_orientation()
        compassNorth = SenseHat().get_compass()
        magnetometer = SenseHat().get_compass_raw()
        gyroscope = SenseHat().get_gyroscope_raw()
        accelerometer = SenseHat().get_accelerometer_raw()
        humidity = SenseHat().get_humidity()
        temperature = SenseHat().get_temperature()
        pressure = SenseHat().get_pressure()
        dataExact = [datetime.now().strftime('%Y-%m-%d_%H:%M:%S.%f'),orientation['yaw'],orientation['pitch'],orientation['roll'],compassNorth,magnetometer['x'],magnetometer['y'],magnetometer['z'],gyroscope['x'],gyroscope['y'],gyroscope['z'],accelerometer['x'],accelerometer['y'],accelerometer['z'],humidity,temperature,pressure]
        dataStr = ",".join(map(str, dataExact))
        self.file.write(dataStr + '\n')
        dataRounded = [round(x, 2) if isinstance(x, float) else x for x in dataExact]
        # also recorded rounded values to the log
        dataRoundedStr = ",".join(map(str, dataRounded))
        logger.info(f"Recorded Sensor Data: {dataRoundedStr}")

    def copyImage(self, path):
        """Copies an image to the dump folder. The image is renamed to the current time."""
        imageSize = os.path.getsize(path)
        if (not os.path.exists(path)):
            logger.error(f"Image {path} does not exist. Could not copy to data folder.")
            return
        elif (not self.spaceRemaining):
            logger.error(f"Insufficient space remaining to store image {path}.")
            return
        else:
            imageName = f"image_{datetime.now().strftime('%Y-%m-%d_%H%M%S%f')}.jpg"
            imagePath = os.path.join(self.dumpFolder, imageName)
            shutil.copy(str(path), imagePath)
            self.imageIndex += 1
            logger.info(f"Image {path} saved to {imagePath}, {self.imageIndex} images in data folder.")

    @property
    def dataSize(self):
        return 0
    
    @property
    def remainingCapacity(self):
        "returns the remaining capacity of the data folder in bytes"
        return 100 - self.__counter * 10

    @property
    def spaceRemaining(self):
        "returns True if there is enough space remaining to store an image"
        return self.__counter < 10

    def close(self):
        self.file.flush()
        self.file.close()

    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_value, traceback):
        self.close()