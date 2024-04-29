from devices.arduino import *

import time

action = "o"

arduino = Arduino()

while action != "\\":
    action = input("type movement: ")
    arduino.send_serial(action)

# while action != "\\":
#     action = "a"
#     arduino.send_serial(action)
#     time.sleep(1)
#     action = "d"
#     arduino.send_serial(action)
#     time.sleep(1)x    
