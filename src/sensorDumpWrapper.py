"""Manages dumping sensor data to a csv."""

from sense_hat import SenseHat
from datetime import datetime
import os
import shutil
from datetime import datetime
import logging

HEADER = "time,yaw,pitch,roll,compassNorth,magnetometerX,magnetometerY,magnetometerZ,gyroscopeX,gyroscopeY,gyroscopeZ,accelerometerX,accelerometerY,accelerometerZ,humidity,temperature,pressure"

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
        dataExact = [datetime.now().strftime('%Y-%m-%d %H:%M:%s:%f'),orientation['yaw'],orientation['pitch'],orientation['roll'],compassNorth,magnetometer['x'],magnetometer['y'],magnetometer['z'],gyroscope['x'],gyroscope['y'],gyroscope['z'],accelerometer['x'],accelerometer['y'],accelerometer['z'],humidity,temperature,pressure]
        dataRounded = [round(x, 2) if isinstance(x, float) else x for x in dataExact]
        dataStr = ",".join(map(str, dataRounded))
        self.file.write(dataStr + '\n')
        # also recorded rounded values to the log
        dataRoundedStr = ",".join(map(str, dataRounded))
        logging.logger.info(f"Recorded Sensor Data: {dataRoundedStr}")

    def copyImage(self, path):
        """Copies an image to the dump folder. The image is renamed to the current time."""
        if (not os.path.exists(path)):
            return
        imageName = datetime.now().strftime("image_%Y-%m-%d%_H%:M%:S:%f") + ".jpg"
        imagePath = os.path.join(self.dumpFolder, imageName)
        shutil.copy(path, imagePath)

    def close(self):
        self.file.flush()
        self.file.close()
        
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_value, traceback):
        self.close()