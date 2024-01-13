from worker import Worker # to be replaced with a reference to teh calculation Team's worker
# from cameraWrapper import CameraWrapper
import threading
from datetime import datetime
from pathlib import Path
from logzero import logger, logfile
import time

BASE_FOLDER = Path(__file__).parent.resolve()
CALCULATION_TIME = 5 # seconds
logfile("events.log")

if __name__ == "__main__":
    startTime = datetime.now()

    logger.info(f"Starting program")

    speedWorker = Worker() #  replace with the calculation team's worker
    speedThread = threading.Thread(target=speedWorker.work)
    speedThread.start()

    # cameraWrapper = CameraWrapper()

    while (datetime.now() - startTime).total_seconds() < CALCULATION_TIME:
        # cameraWrapper.capture(BASE_FOLDER + "/images/test.jpg")
        #speedWorker.queue.put("test.jpg")
        time.sleep(1)

    speedWorker.cancel()
    # cameraWrapper.close()
    speedThread.join()
    logger.info(f"Finished program")