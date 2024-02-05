from picamera import PiCamera

# Create an instance of the PiCamera class
cam = PiCamera()

# Set the resolution of the camera to 4056×3040 pixels
cam.resolution = (4056, 3040)

# Capture an image
cam.capture("image1.jpg")