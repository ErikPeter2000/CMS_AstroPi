from picamera import PiCamera

RESOLUTION = (4056, 3040)

class CameraWrapper:
    """Manages the Raspberry Pi Camera. Images are 4056 x 3040 by default."""
    def __init__(self):
        self.camera = PiCamera()
        self.camera.resolution = RESOLUTION

    def capture(self, path):
        self.camera.capture(str(path))

    def close(self):
        self.camera.close()

    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_value, traceback):
        self.close()