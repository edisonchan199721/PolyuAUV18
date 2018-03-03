from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
from threading import Thread
import numpy as np

# initialize the camera and grab a reference to the raw camera capture

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))

# allow the camera to warmup

camera.start()
time.sleep(2)

# capture frames from the camera
while(1):
        # grab the raw NumPy array representing the image, then initialize the timestamp
        # and occupied/unoccupied text
    image = camera.read()
    cv2.imshow("raw", image)
    key = cv2.waitKey(0) & 0xFF
##        # clear the stream in preparation for the next frame
##        # if the `q` key was pressed, break from the loop
    if key == ord('q'):                
        break
        
cv2.destroyAllWindows()
vs.stop()
