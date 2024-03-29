# Team Pie-Guys AstroPi code for the 2023-2024 mission SpaceLab
# Author: Erik, Timur, Yotam, Samuel, 2023-2024
# Our program uses one background thread in addition to the main. As instructed, we will document and explain our usage thoroughly.
# By using a background thread, we can capture images and data; and process them simultaneously. An alternative is to capture all data and process them at the end, but we decided against this.
# We chose to use another thread to maximise the time we have to record data, and also calculate the speed in real-time.
# We do this by loading a pair of images taken by the camera in the main thread. We push these images to a queue, and the background thread processes them. We decided to load them in the main thread as to avoid using file handles in the background. Since capturing images takes around 2 seconds and we had to wait some idle time between captures, we decided that the use of a background thread was the most suitable solution.
# The use of try...finally clauses ensures that the threads are closed properly.
# with... statements in wrapper objects also ensure that resources are closed properly.
# The repo can be found in ErikPeter2000's GitHub account. Links are not allowed in code.

from sensorDumpWrapper import SensorDumpWrapper
from cameraWrapper import CameraWrapper
from speedWorker import SpeedWorker
from cv2Matcher import ImagePair, imageToCv2, timeDifference

import threading
from datetime import datetime
from pathlib import Path
from logzero import logger, logfile
import time
import os
from queue import Queue

# Constants
ROOT_FOLDER = (Path(__file__).parent).resolve()
MAX_CALC_TIME = 585 # seconds 585s=9m45s
INTERVAL = 2 # seconds. Bear in mind that the camera takes an additional two seconds to capture an image
IMAGE_INTERVAL = 3 # Save every nth image
REQUIRED_IMAGES_FOR_MATCH = 2 # The number of images needed to calculate a match

# Globals
imageCaptureCounter = 0
startTime = None

def writeSpeed(value):
    """Writes the speed to speed.txt."""
    with open(str(ROOT_FOLDER / "result.txt"), "w") as file:
        file.write(value)
    return value

def roundSpeed(value):
    """Rounds the speed to 6 digits maximum, and returns a string."""
    string = str(value)
    return string[0:min(6, len(string))]

def processImageToSave(imagePath, sensorDump):
    """Copies the image to the data folder and renames if the counter % IMAGE_INTERVAL == 0."""
    global imageCaptureCounter
    if imageCaptureCounter % IMAGE_INTERVAL == 0:
        sensorDump.copyImage(imagePath)
    imageCaptureCounter +=1

def speedLoop(speedWorker, camera, sensorDumper, imageQueue):
    """Captures images and calculates speed from matches for MAX_CALC_TIME seconds. Also records sensor data to a csv file."""
    imageIndex = 0
    while (datetime.now() - startTime).total_seconds() < MAX_CALC_TIME: # run for MAX_CALC_TIME seconds
        currentImagePath = ROOT_FOLDER / Path(f"./image{imageIndex}.jpg") # the path to store the captured image
        time1 = datetime.now()
        camera.capture(currentImagePath)
        time2 = datetime.now()
        logger.debug(f"Time to capture: {(time2-time1).total_seconds()}")
        logger.info(f"Captured Image: {currentImagePath}")
        processImageToSave(currentImagePath, sensorDumper)
        imageQueue.put(currentImagePath) # enqueue the image for future match calculation
        
        # if there are two images to match, calculate the time difference and enqueue the match data for the speed worker
        if (imageQueue.qsize() >= REQUIRED_IMAGES_FOR_MATCH): # if there are two images to match...
            imageOld = imageQueue.get() # dequeue the oldest image
            imageNew = imageQueue.queue[0] # peek at the newer image
            imageOldCv2 = imageToCv2(imageOld) # convert the images to cv2 images
            imageNewCv2 = imageToCv2(imageNew)
            timeDiff = timeDifference(imageOld, imageNew) # calculate the time difference between the images
            matchData = ImagePair(imageOldCv2, imageNewCv2, timeDiff)
            os.remove(imageOld) # delete the oldest image; we dont need it any more
            speedWorker.queue.put(matchData) # enqueue the match data for the speed worker
            logger.info(f"Captured Pair, Diff: {matchData.timeDifference}s")
        #endif
            
        # increment the image index and record sensor data
        imageIndex+=1
        sensorDumper.record()
        time.sleep(INTERVAL) # wait for INTERVAL seconds before capturing the next image
    #endwhile
    os.remove(imageQueue.get(False)) # delete the last image

def main():
    """Main algorithm. Loop to capture images and calculate speed from matches. Also records sensor data to a csv file"""
    with SensorDumpWrapper(ROOT_FOLDER) as sensorDumper:
        logger.info("Initialised SensorDumper")
        try:
            with SpeedWorker() as speedWorker:
                # initialise the worker thread. We ensure that it is closed in the finally block
                # the target function is the work loop in the speedworker class, that will dequeue image pairs and calculate the speed until cancelled
                speedThread = threading.Thread(target=speedWorker.work)

                logger.info("Initialised SpeedWorker Thread")
                try:
                    with CameraWrapper() as camera:
                        # setup the camera and worker thread
                        logger.info("Initialised Camera")
                        imageQueue = Queue() # stores the last two image paths needed to compute matches
                        speedThread.start() # start the worker thread

                        # start the main loop to record sensor data and calculate speed from matches
                        logger.info("Started SpeedWorker, capturing images...")                        
                        speedLoop(speedWorker, camera, sensorDumper, imageQueue)                          
                        logger.info("Finished Capturing")
                        
                        # calculate the speed and write to file
                        speed = speedWorker.value
                        rounded = roundSpeed(speed)
                        logger.info(f"Calc Speed: {speed} ({rounded}). Writing to file...")
                        writeSpeed(rounded)                    
                finally:
                    # ensure that the speedWorker thread is closed
                    logger.info("Closing SpeedWorker Thread")
                    speedWorker.cancel()
                    if speedThread.is_alive():
                        speedThread.join() # ensure that the thread is closed
            #endwith speedWorker                        
        except Exception as e:
            # in the event of an error, just try and capture some sensor data without bothering to calculate speed
            logger.error(f"Error Occurred in main loop. Attempting to only capture sensor data. \n{e}")
            while (datetime.now() - startTime).total_seconds() < MAX_CALC_TIME:
                sensorDumper.record()
                time.sleep(INTERVAL)

if __name__ == "__main__":
    startTime = datetime.now()
    logfile(str(ROOT_FOLDER / "events.log")) # setup log file

    logger.info(f"Started program {startTime.strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info(f"Directory: {ROOT_FOLDER}")
    try:
        main()
    except Exception as e:
        logger.error(f"Critical Error: \n{e}\nProgram aborted")
    finally:
        logger.info(f"Ended program")
        