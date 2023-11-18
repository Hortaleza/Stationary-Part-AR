import cv2
import numpy as np

color = 'red'

color_ranges = {'red': {'Lower': np.array([0, 90, 80]), 'Upper': np.array([12, 255, 255])},
                'blue': {'Lower': np.array([95, 60, 90]), 'Upper': np.array([180, 255, 255])},
                'green': {'Lower': np.array([50, 20, 15]), 'Upper': np.array([80, 255, 255])}}

color_positions = []

final_string = ''

cap = cv2.VideoCapture(1)


def get_color(frame):
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    max_pixels_count = 0
    best_color = 'red'
    for color, color_range in color_ranges.items():
        mask = cv2.inRange(hsv_frame, color_range['Lower'], color_range['Upper'])
        pixels_count = cv2.countNonZero(mask)

        if pixels_count > max_pixels_count:
            max_pixels_count = pixels_count
            best_color = color
    
    return best_color


while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Cannot load camera")
        break

    if frame is None:
        print("No picture, frame is empty")
        break


    frame_blur = cv2.GaussianBlur(frame, (63, 31), 0)

    hsvFrame = cv2.cvtColor(frame_blur, cv2.COLOR_BGR2HSV)
    

    red_mask = cv2.inRange(hsvFrame, color_ranges['red']['Lower'], color_ranges['red']['Upper'])
    green_mask = cv2.inRange(hsvFrame, color_ranges['green']['Lower'], color_ranges['green']['Upper'])
    blue_mask = cv2.inRange(hsvFrame, color_ranges['blue']['Lower'], color_ranges['blue']['Upper'])
    add_mask = red_mask+green_mask+blue_mask
    add_mask[add_mask>0]=255
    # 定义膨胀核（结构元素）
    kernel = np.ones((32, 32), np.uint8)
    # 进行膨胀处理
    add_mask = cv2.dilate(add_mask, kernel, iterations=1)
    # 进行收缩处理
    add_mask = cv2.erode(add_mask, kernel, iterations=1)
    
    contours, hierarchy = cv2.findContours(add_mask,
                                            cv2.RETR_TREE,
                                            cv2.CHAIN_APPROX_SIMPLE)

    cropped_frame = frame
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if area > 30000:
            x, y, w, h = cv2.boundingRect(contour)
            cropped_frame = frame[y:y + h, x:x + w]
            frame = cv2.rectangle(frame, (x, y),
                                    (x + w, y + h),
                                    (0, 0, 255), 2)

            cv2.putText(frame, "ADD MASK Colour", (x, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.0,
                        (0, 0, 255))
    
    height, width, _ = cropped_frame.shape
    quarter_width = width // 4

    frame1 = cropped_frame[:, 0:quarter_width]
    frame2 = cropped_frame[:, quarter_width:2 * quarter_width]
    frame3 = cropped_frame[:, 2 * quarter_width:3 * quarter_width]
    frame4 = cropped_frame[:, 3 * quarter_width:width]

    color1 = get_color(frame1)
    color2 = get_color(frame2)
    color3 = get_color(frame3)
    color4 = get_color(frame4)
    print(color1, color2, color3, color4)

    cv2.imshow("Final", frame)
    cv2.imshow("cropped_frame", cropped_frame)
    

    if cv2.waitKey(10) & 0xFF == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        break


        

