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

    if show_result:
        print (extreme_points_red)
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

    if show_result:
        print (extreme_points_green)
        try:
            for i in extreme_points_green:
                cv2.circle(image_green, i, 10, (80, 255, 255), -1)
        except:
            pass
        cv2.imshow('green mask', image_green)
        key = cv2.waitKey(0)
        cv2.destroyAllWindows()
    return extreme_points_green

def get_extreme_yellow_points(image, show_result = False):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    #common grey
    lower_grey = np.array([0, 0, 100])
    upper_grey = np.array([180, 20, 200])

    # yellow
    lower_yellow = np.array([15, 15, 100])
    upper_yellow = np.array([45, 55, 180])

    # mask
    mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)
    #mask_green += cv2.inRange(hsv, lower_grey, upper_grey)

    extreme_points_yellow = None

    ##_green contour
    image_yellow, contours_yellow, hierarchy_yellow = cv2.findContours(mask_yellow, cv2.RETR_EXTERNAL,
                                                                    cv2.CHAIN_APPROX_NONE)  # cv2.CHAIN_APPROX_SIMPLE
    contours_yellow = sorted(contours_yellow, key=cv2.contourArea)
    c = None
    while True:
        # Break when no more contour to consider
        # aka nothing good detected
        if len(contours_yellow) == 0:
            break
        # last one is the largest contour
        cx = contours_yellow[-1]
        # Remining contour to small to be significant
        if cv2.contourArea(cx) < 20:
            break
        # Get angle of the contour, prevent capturing the bottom green band
        # Or considering distant objects as blacks
        (x, y), (MA, ma), angle = cv2.fitEllipse(cx)
        if (not ((angle < 45) or (angle > 135))) or (cv2.arcLength(cx, True) < 40):
            del contours_yellow[-1]
        else:
            c = cx
            break
    # LRTB
    try:
        extreme_points_yellow = [tuple(c[c[:, :, 0].argmin()][0]), tuple(c[c[:, :, 0].argmax()][0])
            , tuple(c[c[:, :, 1].argmin()][0]), tuple(c[c[:, :, 1].argmax()][0])]
    except:
        print ('No green')

    if show_result:
        print (extreme_points_yellow)
        try:
            for i in extreme_points_yellow:
                cv2.circle(image_yellow, i, 10, (80, 255, 255), -1)
        except:
            pass
        cv2.imshow('yellow mask', image_yellow)
        key = cv2.waitKey(0)
        cv2.destroyAllWindows()
    return extreme_points_yellow

def location_calculation(extreme_points_red, extreme_points_green):
    length_red, length_green = 0, 0
    if extreme_points_red is not None:
        length_red = int(math.sqrt((extreme_points_red[2][0]-extreme_points_red[3][0])**2+(extreme_points_red[2][1]-extreme_points_red[3][1])**2))
    if extreme_points_green is not None:
        length_green = int(math.sqrt((extreme_points_green[2][0]-extreme_points_green[3][0])**2+(extreme_points_green[2][1]-extreme_points_green[3][1])**2))
    # Compare both length, take the longer one, the length will likely be shorten due to incorrect recognition
    length = max(length_red, length_green)


def location_calculation(extreme_points_yellow):
    yellow_distance, yellow_angle = 0, 0
    if extreme_points_yellow is not None:
        yellow_distance = int(math.sqrt((extreme_points_yellow[2][0]-extreme_points_yellow[3][0])**2+(extreme_points_yellow[2][1]-extreme_points_yellow[3][1])**2))
        yellow_distance = 100/yellow_distance # or what ever measured real pixel at 1 m
        #assume 100 pixels at 1m, 10 pixels mean same object at 10m
        yellow_mid_point = (int((extreme_points_yellow[2][0]+extreme_points_yellow[3][0])/2), int((extreme_points_yellow[2][1]+extreme_points_yellow[3][1])/2))



if __name__ == "__main__":
    frame = cv2.imread('test1.5m2.jpg')
    frame = cv2.imread('test12_cr.jpg')
    distance_calculation(get_extreme_red_points(frame))
    get_extreme_green_points(frame)
