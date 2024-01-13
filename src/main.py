from worker import Worker # to be replaced with a reference to teh calculation Team's worker
from dummyCameraWrapper import CameraWrapper # replace with actual camera wrapper
from cv2Matcher import MatchData, calculateMatches
import threading
from datetime import datetime
from pathlib import Path
from logzero import logger, logfile
import time
import os
from queue import Queue

BASE_FOLDER = Path(__file__).parent.resolve()
MAX_CALC_TIME = 10 # seconds
INTERVAL = 1 # seconds
logfile(str(BASE_FOLDER / "events.log"))

def writeSpeed(speed):
    """Writes the speed to a speed.txt."""
    with open(str(BASE_FOLDER / "speed.txt"), "w") as file:
        file.write(str(speed))

if __name__ == "__main__":
    startTime = datetime.now()

    logger.info(f"Starting program")
    speedWorker = Worker() # to be replaced with the calculation team's worker
    speedThread = threading.Thread(target=speedWorker.work) # initialise the worker thread
    speedThread.start() # start the worker thread

    cameraWrapper = CameraWrapper()
    imageQueue = Queue() # store the last two images needed to compute matches    
    try:
        imageIndex = 0
        while (datetime.now() - startTime).total_seconds() < MAX_CALC_TIME: # run for MAX_CALC_TIME seconds
            currentImagePath = BASE_FOLDER / Path(f"./image{imageIndex}.jpg") # the path to store the captured image
            cameraWrapper.capture(currentImagePath)
            imageQueue.put(currentImagePath) # enqueue the image for future match calculation
            
            if (imageQueue.qsize() == 2): # if there are two images to match...
                image1 = imageQueue.get() # dequeue the oldest image
                image2 = imageQueue.queue[0] # peek at the newer image
                matchData = calculateMatches(image1, image2)
                logger.info(f"Matches: {len(matchData)} Time Difference: {matchData.timeDifference}")
                os.remove(image1) # delete the oldest image; we dont need it any more

                speedWorker.queue.put(matchData) # enqueue the match data for the speed worker
            imageIndex+=1
            time.sleep(INTERVAL) # wait for INTERVAL seconds before capturing the next image

        os.remove(imageQueue.get(False)) # delete the last image

        writeSpeed(speedWorker.value)
    except Exception as e:
        logger.exception(e)
    finally:
        logger.info(f"Exiting program")
        speedWorker.cancel()
        speedThread.join()
        cameraWrapper.close()
        logger.info(f"Program exited safely")
    