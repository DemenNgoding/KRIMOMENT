'''
this script in for finding the ideal hsl values for colors
'''

import cv2 as cv
from sensors.camera import Camera
# init camera
camObj = Camera("f", 0)

# hsv color
green = [[68, 91, 121], [111, 195, 212]]
orange = [[0, 21, 87], [258, 107, 255]]


def nothing(x):
    pass


# Init
wd_name = "Trackbars"
cv.namedWindow(wd_name)

cv.createTrackbar("LH", wd_name, 0, 255, nothing)
cv.createTrackbar("LS", wd_name, 0, 255, nothing)
cv.createTrackbar("LV", wd_name, 0, 255, nothing)
cv.createTrackbar("HH", wd_name, 0, 255, nothing)
cv.createTrackbar("HS", wd_name, 0, 255, nothing)
cv.createTrackbar("HV", wd_name, 0, 255, nothing)

while True:
    LH = cv.getTrackbarPos("LH", wd_name)
    LS = cv.getTrackbarPos("LS", wd_name)
    LV = cv.getTrackbarPos("LV", wd_name)
    HH = cv.getTrackbarPos("HH", wd_name)
    HS = cv.getTrackbarPos("HS", wd_name)
    HV = cv.getTrackbarPos("HV", wd_name)

    dynamic_hsv = [[LH, LS, LV], [HH, HS, HV]]
    frame = camObj.get_processed_frame(dynamic_hsv)

    # ctr = camObj.get_center_object(frame)
    # print(camObj.get_object_location(ctr[1]))

    cv.imshow("frame", frame)

    if cv.waitKey(1) == ord('q'):
        break

cv.destroyAllWindows()
