from pathlib import Path
import os
import shutil

PATH = BASE_FOLDER = Path(__file__).parent.resolve()
IMAGE_PATH = PATH / "../Images/Example"

class CameraWrapper:
    index = 0
    imageArray = []
    def __init__(self):
        for filename in os.listdir(IMAGE_PATH):
            if filename.endswith(".jpg") or filename.endswith(".png"):
                self.imageArray.append(os.path.join(IMAGE_PATH.resolve(), filename))

    def capture(self, pathString):
        imagePath = self.imageArray[self.index]
        shutil.copy(imagePath, pathString)        
        self.index = (self.index + 1) % len(self.imageArray)

    def close(self):
        pass