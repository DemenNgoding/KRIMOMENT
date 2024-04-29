from sensors.camera import Camera
from statistics import mode
import cv2 as cv
import time
from devices.arduino import Arduino

arduino = Arduino()

cams = {
    "360": Camera("360", 1)
}

# color_hsv = {
#     "orange": [[0, 191, 141], [17, 255, 255]],
#     "green": [[68, 91, 121], [111, 195, 212]],
#     "black": [[54, 21, 28], [137, 111, 78]],
#     "yellow": [[0, 75, 191], [76, 255, 255]],
#     "blue": [[95, 189, 183], [120, 255, 146]],
# }

color_hsv = {
    "orange": [[0, 108, 255], [179, 255, 255]],
    # "green": [[68, 91, 121], [111, 195, 212]],
    # "black": [[54, 21, 28], [137, 111, 78]],
    # "yellow": [[17, 94, 193], [43, 189, 227]],
    # "blue": [[95, 189, 183], [120, 255, 146]],
}

last_action = "x"


def decision(last_action):
    dec_chase = list()
    dec_avoid = list()
    images = list()
    for key, val in cams.items():
        action = val.chase(color_hsv["orange"])
        image, action = action.values()
        dec_chase.append(action)
        images.append({
            "k": key + " orange",
            "image": image
        })
    # for key, val in cams.items():
    #     action = val.avoid_line(color_hsv["yellow"])
    #     image, action = action.values()
    #     dec_avoid.append(action)
    #     images.append({
    #         "k": key + " line",
    #         "image": image
    #     })
    print(list(cams.keys()), dec_avoid + dec_chase)
    return [images, dec_chase]


ctr = 0

while True:

    action = decision(last_action)

    for i in action[0]:
        cv.imshow(i['k'], i["image"])

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

    key = list(filter(lambda x: x != '', action[1]))

    if key == []:
        if ctr == 4:
            arduino.send_serial("y")
        if ctr == 15:
            arduino.send_serial('=')
            ctr = 0
        ctr += 1
        arduino.send_serial(last_action)
        print(last_action)
    else:
        arduino.send_serial('n')
        arduino.send_serial(key[0])
        print(key[0])
        last_action = key[0]
