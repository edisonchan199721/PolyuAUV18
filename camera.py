import picamera
import threading
import time
import detect

class camera_thread(threading.Thread):
    def __init__(self):
      threading.Thread.__init__ (self)
      self._is_running = True

    def run(self):
       while (self._is_running):
           photoCapture()

    def stop(self):
        self._is_running = False

def photoCapture():
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
        time.sleep(2)
        print (detect.get_extreme_red_points(image))
        # for filename in camera.capture_continuous('img{counter:03d}.jpg'):
        #     print('Captured %s' % filename)
        #     time.sleep(2)
