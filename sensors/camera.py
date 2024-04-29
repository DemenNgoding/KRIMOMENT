import cv2 as cv
import numpy as np
import statistics


class Camera:
    def __init__(self, camera_name, camera: int, width=640, height=480) -> None:
        self.__camera_id = camera
        self.__camera_height = height
        self.__camera_width = width
        self.__image = list()   

        # initialize capture device
        self.__cap = cv.VideoCapture(camera,  cv.CAP_DSHOW)
        self.__cap.set(cv.CAP_PROP_FRAME_WIDTH, self.__camera_width)
        self.__cap.set(cv.CAP_PROP_FRAME_HEIGHT, self.__camera_height)

        # objects dict and coords
        self.__camera_name = camera_name

    def __repr__(self) -> str:
        pass

    def __eq__(self, __value: object) -> bool:
        pass

    def get_frame(self) -> np.ndarray:
        ret, img = self.__cap.read()
        
        if not ret:
            return f"Err in {self.__camera_id}"
        self.__image = img

        return img

    def get_processed_frame(self, color_hsv: list[list]) -> np.ndarray:
        img = self.get_frame()

        hsv_img = cv.cvtColor(img, cv.COLOR_BGR2HSV)
        _lower_bound = np.array(color_hsv[0])
        _upper_bound = np.array(color_hsv[1])
        mask = cv.inRange(hsv_img, _lower_bound, _upper_bound)

        return mask

    def get_single_center_object(self, color_hsv: list[list]) -> dict:
        """get an average single object based on the image 
        ! use object.get_frame() before using this function !

        Returns:
            list: [0] image, [1] a point
        """

        image = self.get_processed_frame(color_hsv)

        values = {
            "image": image
        }

        M = cv.moments(image)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            values["coordinates_xy"] = [[cX, cY]]
            return values
        else:
            values["coordinates_xy"] = [[]]
            return values

    def get_center_object(self, color_hsv: list[list]) -> dict:
        """get the averange center location of the multiple object
        ! use object.get_frame() before using this function !

        Returns:
            list: [0] image, [1] detected points
        """
        image = self.get_processed_frame(color_hsv)

        values = {
            "image": image,
            "coordinates_xy": []
        }

        contours, hierarchy = cv.findContours(image, 1, 2)
        maxArea = 0.5
        for c in contours:
            M = cv.moments(c)
            area = cv.contourArea(c)
            if area < maxArea:
                continue
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                values["coordinates_xy"].append([cX, cY])

        return values

    def get_object_location_grid(self, color_hsv: list[list]) -> dict:
        """find the object based on the x and y

        Args:
            image_wxh ([width, height]): aquire image height and width
            coordinates_xy ([[x0, y0], [x1, y1], ...]): lists of the detected image center

        Returns:
            list: where does the object located based on the coordinates
        |==================================================================
        |      (0,0)    |              |  |               |               |
        |               |              |  |               |               |
        |---------------|--------------|--|---------------|---------------|
        |               |              |  |               |               |
        |               |              |  |               |               |
        |---------------|--------------|--|---------------|---------------|
        |               |              |  |               |     (4,2)     |
        |               |              |  |               |               |
        |==================================================================
        """

        image, coordinates_xy = self.get_center_object(color_hsv).values()

        w, h = self.__camera_width, self.__camera_height
        result = list()

        def y_coord(x_segment: int, y: int) -> list:
            if y < h/3:
                return [x_segment, 0]
            elif y >= h/3 and y <= h*2/3:
                return [x_segment, 1]
            else:
                return [x_segment, 2]

        def unique(list):
            # initialize a null list
            unique_list = []

            # traverse for all elements
            for x in list:
                # check if exists in unique_list or not
                if x not in unique_list:
                    unique_list.append(x)
            return unique_list

        for coordinate_xy in coordinates_xy:
            if coordinate_xy == []:
                return []

            x, y = coordinate_xy[0], coordinate_xy[1]
            if x < w/3:
                result.append(y_coord(0, y))
            elif x >= w/3 and x < (w/2 - w/12):
                result.append(y_coord(1, y))
            elif x >= (w/2 - w/12) and x <= (w/2 + w/12):
                result.append(y_coord(2, y))
            elif x > (w/2 + w/12) and x <= w*2/3:
                result.append(y_coord(3, y))
            else:
                result.append(y_coord(4, y))

        values = {
            "image": image,
            "coordinates_xy": unique(result)
        }

        return values

    def chase(self, color_hsv: list[list]) -> dict:
        """makes the robot chase

        Args:
            coords (list): list of coords based on the picture

        Returns:
            str: one character to send to the arduino as an action
        """

        image, coordinates_xy = self.get_object_location_grid(
            color_hsv).values()

        values = {
            "image": image,
            "descision": str()
        }

        if coordinates_xy != []:
            if self.__camera_name == 'right':
                values["descision"] = "e"
                return values

            if self.__camera_name == "left":
                values["descision"] = "q"
                return values

        if coordinates_xy == [] and self.__camera_name == "front":
            values["descision"] = ''
            return values

        # get ball average position
        x = []

        for i in coordinates_xy:
            x.append(i[1])
        x_average = np.average(x)

        if self.__camera_name == "back":
            if x_average < 2:
                values["descision"] = "e"
                return values
            if x_average >= 2:
                values["descision"] = "q"
                return values

        if self.__camera_name == "front":
            if x_average > 1 and x_average < 3:
                values["descision"] = "w"
                return values
            if x_average <= 1:
                values["descision"] = "e"
                return values
            if x_average >= 3:
                values["descision"] = "q"
                return values

        return values

    def avoid_line(self, color_hsv: list[list]) -> dict:

        image, coordinates_xy = self.get_center_object(
            color_hsv).values()

        values = {
            "image": image,
            "descision": str()
        }

        def handle_filter(coordinate) -> bool:
            if coordinate[1] >= 715 and coordinate[0] >= self.__camera_width/3 and coordinate[0] <= self.__camera_width*2/3:
                return True
            return False
        y = list(
            filter(handle_filter, coordinates_xy))

        if y == []:
            return values

        if self.__camera_name == "front":
            values["descision"] = "s"
            return values
        if self.__camera_name == "back":
            values["descision"] = "w"
            return values
        if self.__camera_name == "left":
            values["descision"] = "e"
            return values
        if self.__camera_name == "right":
            values["descision"] = "q"
            return values

        return values

    def find_and_face_object(self, color_hsv: list[list]) -> dict:
        image, descision = self.chase(color_hsv).values()

        values = {
            "image": image,
            "descision": descision
        }

        if descision == "w":
            values["descision"] = "="
            return values

        return values

    def avoid_object(self, color_hsv: list[list]):
        image, coordinates_xy = self.get_center_object(color_hsv)

        values = {
            "image": image,
            "descision": ""
        }

        coordinates_xy = map(lambda x: x[0], coordinates_xy)

        filtered_coordinates_xy = list(
            filter(lambda i: i >= 1 and i <= 3, coordinates_xy))

        mode = statistics.mode(filtered_coordinates_xy)
        if mode == 3:
            values["descision"] = "e"
            return values
        elif mode == 1:
            values["descision"] = "q"
            return values

        return values
