from picamera.array import PiRGBArray
from picamera import PiCamera
import threading
import time
import detect
import cv2

class camera_thread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__ (self)
        self._is_running = True

    def run(self):
        print("Hi")
        self.photoCapture()

    def stop(self):
        self._is_running = False

    def photoCapture(self):
        camera = PiCamera()
        camera.resolution = (640,480)
        camera.framerate = 10
        camera.shutter_speed = camera.exposure_speed
        camera.exposure_mode = 'on'
        rawCapture = PiRGBArray(camera)
        time.sleep(2)
        while (self._is_running):
            camera.capture(rawCapture, format="bgr")
            image = rawCapture.array
            cv2.imshow("raw", image)
    ##        print(detect.get_extreme_red_points(image))
    ##        print('a')

if __name__ == "__main__":
    camera = PiCamera()
    camera.resolution = (640,480)
    camera.framerate = 10
    camera.shutter_speed = camera.exposure_speed
    #camera.exposure_mode = 'off'
    rawCapture = PiRGBArray(camera)
    time.sleep(2)
    while (True):
        camera.capture(rawCapture, format="bgr")
        image = rawCapture.array
        cv2.imshow("raw", image)
##        print(detect.get_extreme_red_points(image))
##        print('a')
        if cv2.waitKey(0) & 0xFF == ord('q'):
            break
        # clear the stream in preparation for the next frame
        # if the `q` key was pressed, break from the loop

