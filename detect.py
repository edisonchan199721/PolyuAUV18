# import the necessary packages
import math
import cv2
import numpy as np

def get_extreme_red_points(image, show_result = False):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    #common grey
    lower_grey = np.array([0, 0, 100])
    upper_grey = np.array([180, 20, 200])

    # red
    lower_red = np.array([0, 25, 110])
    upper_red = np.array([15, 55, 200])
    lower_red1 = np.array([150, 25, 110])
    upper_red1 = np.array([180, 55, 200])

    # mask
    mask_red = cv2.inRange(hsv, lower_red, upper_red)
    mask_red += cv2.inRange(hsv, lower_red1, upper_red1)
    mask_red += cv2.inRange(hsv, lower_grey, upper_grey)

    extreme_points_red = None

    ##_red contour
    image_red, contours_red, hierarchy_red = cv2.findContours(mask_red, cv2.RETR_EXTERNAL,
                                                              cv2.CHAIN_APPROX_NONE)  # cv2.CHAIN_APPROX_SIMPLE
    contours_red = sorted(contours_red, key=cv2.contourArea)
    c = None
    while True:
        if len(contours_red) == 0:
            break
        cx = contours_red[-1]
        if cv2.contourArea(cx) < 20:
            break
        (x, y), (MA, ma), angle = cv2.fitEllipse(cx)
        if (not ((angle < 45) or (angle > 135))) or (cv2.arcLength(cx, True) < 0):
            del contours_red[-1]
            print (cv2.arcLength(cx, True))
            print (angle)
        else:
            c = cx
            break
    # LRTB
    try:
        extreme_points_red = [tuple(c[c[:, :, 0].argmin()][0]), tuple(c[c[:, :, 0].argmax()][0]),
                              tuple(c[c[:, :, 1].argmin()][0]), tuple(c[c[:, :, 1].argmax()][0])]
    except:
        print ('No red')

    print (extreme_points_red)

    if show_result:
        try:
            for i in extreme_points_red:
                cv2.circle(image_red, i, 10, (80, 255, 255), -1)
        except:
            pass
        cv2.imshow('red mask', image_red)
        key = cv2.waitKey(0)
        cv2.destroyAllWindows()
    return extreme_points_red


def get_extreme_green_points(image, show_result = False):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    #common grey
    lower_grey = np.array([0, 0, 100])
    upper_grey = np.array([180, 20, 200])

    # green
    lower_green = np.array([40, 15, 100])
    upper_green = np.array([80, 55, 180])

    # mask
    mask_green = cv2.inRange(hsv, lower_green, upper_green)
    #mask_green += cv2.inRange(hsv, lower_grey, upper_grey)

    extreme_points_green = None

    ##_green contour
    image_green, contours_green, hierarchy_green = cv2.findContours(mask_green, cv2.RETR_EXTERNAL,
                                                                    cv2.CHAIN_APPROX_NONE)  # cv2.CHAIN_APPROX_SIMPLE
    contours_green = sorted(contours_green, key=cv2.contourArea)
    c = None
    while True:
        # Break when no more contour to consider
        # aka nothing good detected
        if len(contours_green) == 0:
            break
        # last one is the largest contour
        cx = contours_green[-1]
        # Remining contour to small to be significant
        if cv2.contourArea(cx) < 20:
            break
        # Get angle of the contour, prevent capturing the bottom green band
        # Or considering distant objects as blacks
        (x, y), (MA, ma), angle = cv2.fitEllipse(cx)
        if (not ((angle < 45) or (angle > 135))) or (cv2.arcLength(cx, True) < 40):
            del contours_green[-1]
        else:
            c = cx
            break
    # LRTB
    try:
        extreme_points_green = [tuple(c[c[:, :, 0].argmin()][0]), tuple(c[c[:, :, 0].argmax()][0])
            , tuple(c[c[:, :, 1].argmin()][0]), tuple(c[c[:, :, 1].argmax()][0])]
    except:
        print ('No green')

    print (extreme_points_green)

    if show_result:
        try:
            for i in extreme_points_green:
                cv2.circle(image_green, i, 10, (80, 255, 255), -1)
        except:
            pass
        cv2.imshow('green mask', image_green)
        key = cv2.waitKey(0)
        cv2.destroyAllWindows()
    return extreme_points_green

def length_calculation(extreme_points_red, extreme_points_green):
    # Would need yaw for distance calculation
    length_red, length_green = None, None
    if extreme_points_red is None:
        length_red = int(math.sqrt((extreme_points_red[2][0]-extreme_points_red[3][0])**2+(extreme_points_red[2][1]-extreme_points_red[3][1])**2))
        length_red =  length_red / 100 # or what tested later
    if extreme_points_green is None:
        length_green = int(math.sqrt((extreme_points_green[2][0]-extreme_points_green[3][0])**2+(extreme_points_green[2][1]-extreme_points_green[3][1])**2))
        length_green =  length_green / 100 # or what tested later
    return length_red, length_green


if __name__ == "__main__":
    frame = cv2.imread('test1.5m2.jpg')
    frame = cv2.imread('test12_cr.jpg')
    distance_calculation(get_extreme_red_points(frame))
    get_extreme_green_points(frame)