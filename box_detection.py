import cv2
import numpy as np

ball_colors = {'red', 'green', 'blue'}

color_ranges = {'red': {'Lower': np.array([0, 90, 80]), 'Upper': np.array([12, 255, 255])},
                'blue': {'Lower': np.array([95, 60, 90]), 'Upper': np.array([180, 255, 255])},
                'green': {'Lower': np.array([50, 20, 15]), 'Upper': np.array([80, 255, 255])}}

cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if ret:
        if frame is not None:

            hsvFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            red_mask = cv2.inRange(hsvFrame, color_ranges['red']['Lower'], color_ranges['red']['Upper'])
            green_mask = cv2.inRange(hsvFrame, color_ranges['green']['Lower'], color_ranges['green']['Upper'])
            blue_mask = cv2.inRange(hsvFrame, color_ranges['blue']['Lower'], color_ranges['blue']['Upper'])

            """kernel = np.ones((5, 5), "uint8")
            frame = cv2.morphologyEx(frame, cv2.MORPH_OPEN, kernel)"""

            """red_mask = cv2.dilate(red_mask, kernel) 
            res_red = cv2.bitwise_and(imageFrame, imageFrame,  
                              mask = red_mask) 


            green_mask = cv2.dilate(green_mask, kernel) 
            res_green = cv2.bitwise_and(imageFrame, imageFrame, 
                                mask = green_mask) 

            blue_mask = cv2.dilate(blue_mask, kernel) 
            res_blue = cv2.bitwise_and(imageFrame, imageFrame, 
                               mask = blue_mask)"""

            contours, hierarchy = cv2.findContours(red_mask,
                                                   cv2.RETR_TREE,
                                                   cv2.CHAIN_APPROX_SIMPLE)

            for pic, contour in enumerate(contours):
                area = cv2.contourArea(contour)
                if area > 30000:
                    x, y, w, h = cv2.boundingRect(contour)
                    frame = cv2.rectangle(frame, (x, y),
                                          (x + w, y + h),
                                          (0, 0, 255), 2)

                    cv2.putText(frame, "Red Colour", (x, y),
                                cv2.FONT_HERSHEY_SIMPLEX, 1.0,
                                (0, 0, 255))

            contours, hierarchy = cv2.findContours(green_mask,
                                                   cv2.RETR_TREE,
                                                   cv2.CHAIN_APPROX_SIMPLE)

            for pic, contour in enumerate(contours):
                area = cv2.contourArea(contour)
                if area > 30000:
                    x, y, w, h = cv2.boundingRect(contour)
                    frame = cv2.rectangle(frame, (x, y),
                                          (x + w, y + h),
                                          (0, 255, 0), 2)

                    cv2.putText(frame, "Green Colour", (x, y),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                1.0, (0, 255, 0))

            contours, hierarchy = cv2.findContours(blue_mask,
                                                   cv2.RETR_TREE,
                                                   cv2.CHAIN_APPROX_SIMPLE)
            for pic, contour in enumerate(contours):
                area = cv2.contourArea(contour)
                if area > 30000:
                    x, y, w, h = cv2.boundingRect(contour)
                    frame = cv2.rectangle(frame, (x, y),
                                          (x + w, y + h),
                                          (255, 0, 0), 2)

                    cv2.putText(frame, "Blue Colour", (x, y),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                1.0, (255, 0, 0))

            cv2.imshow("Multiple Color Detection in Real-TIme", frame)
            if cv2.waitKey(10) & 0xFF == ord('q'):
                cap.release()
                cv2.destroyAllWindows()
                break

        else:
            print("No picture, frame is empty")
    else:
        print("Cannot load camera")
