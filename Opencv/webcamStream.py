import numpy as np
import cv2
import time

cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)

while(cap.isOpened()):
    # Capture frame-by-frame
    ret, image = cap.read()

    cv2.imshow("rgb", image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
