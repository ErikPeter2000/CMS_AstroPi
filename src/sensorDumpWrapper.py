"""Manages dumping sensor data to a csv."""

from sense_hat import SenseHat
from datetime import datetime
import os
import shutil
from datetime import datetime

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

    def record(self):
        """Records sensor data to the csv file."""
        self.file.write(str(datetime.now()) + "\n")

    def copyImage(self, path):
        """Copies an image to the dump folder. The image is renamed to the current time."""
        if (not os.path.exists(path)):
            return
        imageName = datetime.now().strftime("image_%Y-%m-%d%_H%:M%:S:%f") + ".jpg"
        imagePath = os.path.join(self.dumpFolder, imageName)
        shutil.copy(path, imagePath)

    def close(self):
        self.file.close()
        
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_value, traceback):
        self.close()