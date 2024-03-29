# Manages the Raspberry Pi Camera. Images are 4056 x 3040 by default. Implements some context management for easier disposal.

from picamera import PiCamera

RESOLUTION = (4056, 3040) # Default resolution of the Raspberry Pi Camera


class CameraWrapper:
    """Manages the Raspberry Pi Camera. Images are 4056 x 3040 by default."""
    def __init__(self):
        self.camera = PiCamera()
        self.camera.resolution = RESOLUTION

    def capture(self, path):
        """Captures an image and saves it to the given path."""
        self.camera.capture(str(path))

    def close(self):
        """Closes the camera."""
        self.camera.close()

    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_value, traceback):
        self.close()