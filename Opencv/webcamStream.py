import numpy as np
import cv2
import time

cap = cv2.VideoCapture(0)
##cap.set(3,1280)
##cap.set(4,1024)

##while(cap.isOpened()):
    # Capture frame-by-frame
time.sleep(5)
ret, image = cap.read()

cv2.imshow("rgb", image)
cv2.imwrite("test1.jpg",image)

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()