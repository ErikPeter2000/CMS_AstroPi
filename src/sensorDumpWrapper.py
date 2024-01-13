"""Manages dumping sensor data to a csv."""

from datetime import datetime
import os

class SensorDumpWrapper:
    def __init__(self, directory):
        os.makedirs(os.path.join(directory,"dump"), exist_ok=True)
        self.path = os.path.join(directory,"dump/data.csv")
        self.file = open(self.path, "w")
    def record(self):
        self.file.write(str(datetime.now()) + "\n")
    def close(self):
        self.file.close()