import picamera
import threading
import time

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
    with picamera.PiCamera() as camera:
        camera.resolution = (640,480)
        camera.framerate = 10
        camera.shutter_speed = camera.exposure_speed
        #camera.exposure_mode = 'off'
        time.sleep(2)
        for filename in camera.capture_continuous('img{counter:03d}.jpg'):
            print('Captured %s' % filename)
            time.sleep(0.5)

if __name__ == "__main__":
    cameraThread = camera_thread()
    cameraThread.daemon = True
    cameraThread.start()
    time.sleep(60)
