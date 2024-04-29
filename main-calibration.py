"""
calibrate camera position
"""
import cv2 as cv
from sensors.camera import Camera

cams = {
    "360": Camera("360", 1)
}

while True:
    for key, val in cams.items():
        image = val.get_frame()
        cv.imshow(key, image)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break
