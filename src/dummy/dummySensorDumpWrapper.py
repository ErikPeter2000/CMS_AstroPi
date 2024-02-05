import os
from logzero import logger

class SensorDumpWrapper:
    """(dummy) Manages dumping sensor data to a csv and saving images."""
    def __init__(self, directory):
        self.__counter = 0
        self.dumpFolder = os.path.join(directory,"dump")
        os.makedirs(self.dumpFolder, exist_ok=True)
        self.csvPath = os.path.join(self.dumpFolder, "data.csv")
        self.imageIndex = 0
        
    def record(self):
        """Records sensor data to the csv file."""
        logger.info(f"(dummy) Recorded data.")

    def copyImage(self, path):
        """Copies an image to the dump folder. The image is renamed to the current time."""
        self.__counter+=1
        logger.info(f"(dummy) Image {path} saved to {self.dumpFolder}")

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
        pass   

    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_value, traceback):
        pass