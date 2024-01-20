from speedWorker import SpeedWorker as Worker # to be replaced with a reference to teh calculation Team's worker
from dummyCameraWrapper import CameraWrapper # replace with actual camera wrapper
from cv2Matcher import ImagePair, imageToCv2, timeDifference
from sensorDumpWrapper import SensorDumpWrapper
import threading
from datetime import datetime
from pathlib import Path
from logzero import logger, logfile
import time
import os
from queue import Queue

ROOT_FOLDER = (Path(__file__).parent).resolve()
DATA_FOLDER = ROOT_FOLDER
MAX_CALC_TIME = 10 # seconds
INTERVAL = 1 # seconds
GSD = 1.8 # km/pixel

def writeSpeed(speed):
    """Writes the speed to speed.txt."""
    with open(str(DATA_FOLDER / "speed.txt"), "w") as file:
        file.write(str(speed))

def main():
    with SensorDumpWrapper(DATA_FOLDER) as sensorDumper:
        logger.info("Initialised Sensor Dumper")
        try:
            with Worker(GSD) as speedWorker:
                speedThread = threading.Thread(target=speedWorker.work) # initialise the worker thread
                logger.info("Initialised Speed Worker")
                try:
                    with CameraWrapper() as camera:
                        logger.info("Initialised Camera")
                        imageQueue = Queue() # store the last two images needed to compute matches
                        speedThread.start() # start the worker thread
                        imageIndex = 0
                        logger.info("Started thread, capturing images")

                        while (datetime.now() - startTime).total_seconds() < MAX_CALC_TIME: # run for MAX_CALC_TIME seconds
                            currentImagePath = DATA_FOLDER / Path(f"./image{imageIndex}.jpg") # the path to store the captured image
                            camera.capture(currentImagePath)
                            imageQueue.put(currentImagePath) # enqueue the image for future match calculation
                            
                            if (imageQueue.qsize() == 2): # if there are two images to match...
                                image1 = imageQueue.get() # dequeue the oldest image
                                image2 = imageQueue.queue[0] # peek at the newer image
                                image1cv2 = imageToCv2(image1) # convert the images to cv2 images
                                image2cv2 = imageToCv2(image2)
                                timeDiff = timeDifference(image1, image2) # calculate the time difference between the images
                                matchData = ImagePair(image1cv2, image2cv2, timeDiff)
                                os.remove(image1) # delete the oldest image; we dont need it any more
                                speedWorker.queue.put(matchData) # enqueue the match data for the speed worker
                                logger.info(f"Captured Image Pair, Time Difference: {matchData.timeDifference}")

                            imageIndex+=1
                            sensorDumper.record()
                            time.sleep(INTERVAL) # wait for INTERVAL seconds before capturing the next image 
                            
                        logger.info("Finished Capturing Images")                            
                        os.remove(imageQueue.get(False)) # delete the last image
                        speed = speedWorker.value
                        logger.info(f"Calculated Speed: {speed}")
                        writeSpeed(speed)                    
                    
                finally:
                    speedWorker.cancel()
                    speedThread.join() # ensure that the thread is closed
            #endwith speedWorker
        except Exception as e:
            logger.error(f"Critical Error Occurred. Attempting to only capture sensor data. \n{e}")
            # in the event of an error, just try and capture sensor data instead
            while (datetime.now() - startTime).total_seconds() < MAX_CALC_TIME:
                sensorDumper.record()
                time.sleep(INTERVAL)

if __name__ == "__main__":
    startTime = datetime.now()
    logger.info(f"Started program {startTime.strftime('%Y-%m-%d %H:%M:%S')}")
    logfile(str(DATA_FOLDER / "events.log"))
    logger.info(f"Directory: {DATA_FOLDER}")
    try:
        main()
    except Exception as e:
        logger.error(f"Critical Error: \n{e}\nProgram aborted")
    finally:
        logger.info(f"Ended program")
        