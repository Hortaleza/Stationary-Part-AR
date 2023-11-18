
import cv2
import numpy as np
import serial

# Global variable that holds the BGR values of your detection for the code to output
color_detection_list = [(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)]

target_color = 'red'

final_string = ''

laststring = ''

count = 0

ser = serial.Serial(
    port="COM8",  ## port name
    baudrate=115200,  ## baud rate
    bytesize=8,  ## number of databits
    parity=serial.PARITY_NONE,  ## enable parity checking
    stopbits=1,  ## number of stopbits
    timeout=1,  ## set a timeout value, None for waiting forever
)

color_ranges = {'red': {'Lower': np.array([0, 90, 80]), 'Upper': np.array([12, 255, 255])},
                'blue': {'Lower': np.array([95, 60, 90]), 'Upper': np.array([180, 255, 255])},
                'green': {'Lower': np.array([50, 20, 15]), 'Upper': np.array([80, 255, 255])}}

COLOR_TO_GRB = {
    "red": (0, 0, 255),
    "green": (0, 255, 0),
    "blue": (255, 0, 0),
}

# You should have no reason to modify this class
class ColorDisplayWindow:
    def __init__(
        self,
        color_array,
        window_height=300,
        window_width=2200,
        window_name="displayWindow",
        group_name="Group name here",
    ):
        # global color_detection_list
        self.group_name = group_name
        self.window_height = window_height
        self.window_width = window_width
        self.window_name = window_name

        self.title_height = 100
        self.window = np.zeros(
            (window_height + self.title_height, window_width, 3), dtype=np.uint8
        )

        self.color_array = color_array
        self.color_detection_count = len(color_array)
        self.color_box_width = int(self.window_width / self.color_detection_count)
        self.color_box_height = self.window_height

        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.font_scale = 2
        self.font_thickness = 5
    
    def update_color_array(self, color_array):
        self.color_array = color_array
        self.color_detection_count = len(color_array)
        self.color_box_width = int(self.window_width / self.color_detection_count)
        self.color_box_height = self.window_height

    # helper function to draw the color boxes
    def display(self):
        # global color_detection_list

        # add a white title bar
        self.window[self.window_height :, :] = (255, 255, 255)

        # add the title "RDC 2023 Color Detection"
        title = "RDC 2023 Color Detection : " + self.group_name
        title_size = cv2.getTextSize(
            title, self.font, self.font_scale, self.font_thickness
        )[0]
        title_x = (self.window_width - title_size[0]) // 2
        title_y = self.window_height + ((self.title_height + title_size[1]) // 2)
        cv2.putText(
            self.window,
            title,
            (title_x, title_y),
            self.font,
            self.font_scale,
            (0, 0, 0),
            self.font_thickness,
            cv2.LINE_AA,
        )

        for i in range(self.color_detection_count):
            # draw the color box
            color = self.color_array[i]
            color_box = np.zeros(
                (self.color_box_height, self.color_box_width, 3), dtype=np.uint8
            )
            color_box[:] = color
            self.window[
                : self.color_box_height,
                i * self.color_box_width : (i + 1) * self.color_box_width,
            ] = color_box

            # prepare the number at the center of each color box
            number = str(i + 1)
            text_size = cv2.getTextSize(
                number, self.font, self.font_scale, self.font_thickness
            )[0]
            text_x = (i * self.color_box_width) + (
                (self.color_box_width - text_size[0]) // 2
            )
            text_y = (self.color_box_height + text_size[1]) // 2

            # Draw a black square beneath the number
            square_size = text_size[1] + 40  # Add some padding
            square_top_left = (
                text_x - int(0.5 * (square_size // 2)),
                text_y - 3 * (text_size[1] // 2),
            )
            square_bottom_right = (
                text_x + int(1.5 * (square_size // 2)),
                text_y + (text_size[1] // 2),
            )
            cv2.rectangle(
                self.window,
                square_top_left,
                square_bottom_right,
                (0, 0, 0),
                -1,
                cv2.LINE_AA,
            )

            # Draw the number
            cv2.putText(
                self.window,
                number,
                (text_x, text_y),
                self.font,
                self.font_scale,
                (255, 255, 255),
                self.font_thickness,
                cv2.LINE_AA,
            )
        
        cv2.imshow(self.window_name, self.window)
        cv2.setWindowProperty(self.window_name, cv2.WND_PROP_TOPMOST, 2)
        #cv2.moveWindow(self.window_name, 20, 40)


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


# TODO: Change your team's name and modify the size of the window to your liking
color_display_1 = ColorDisplayWindow(
    window_height=500,
    window_width=1500,
    color_array=color_detection_list,
    window_name="displayWindow1",
    group_name="RDC Team 11",
)

def add_title(frame, title, color=(0, 0, 0), alpha = 0.4):
    overlay = frame.copy()
    # 在黑色色块上绘制矩形
    cv2.rectangle(overlay, (0, 0), (len(title)*19,40), color, -1)
    # 将黑色色块与帧进行混合
    frame = cv2.addWeighted(src1=overlay, alpha=alpha, src2=frame, beta=1 - alpha, gamma=0)

    cv2.putText(img=frame, text=title, org=(5, 30),
            fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1.8, thickness=2,
            color=(255, 255, 255))
    return frame

# camera
cap = cv2.VideoCapture(1)

while cap.isOpened():
    ret, raw_frame = cap.read()
    if not ret:
        print("Cannot load camera")
        continue

    if raw_frame is None:
        print("No picture, frame is empty")
        continue

    raw_frame = cv2.resize(raw_frame, (raw_frame.shape[1]//2, raw_frame.shape[0]//2))

    frame_blur = cv2.GaussianBlur(raw_frame, (31, 15), 0)
    frame_blur = cv2.cvtColor(frame_blur, cv2.COLOR_BGR2HSV)

    red_mask = cv2.inRange(frame_blur, color_ranges['red']['Lower'], color_ranges['red']['Upper'])
    green_mask = cv2.inRange(frame_blur, color_ranges['green']['Lower'], color_ranges['green']['Upper'])
    blue_mask = cv2.inRange(frame_blur, color_ranges['blue']['Lower'], color_ranges['blue']['Upper'])
    add_mask = red_mask+green_mask+blue_mask
    add_mask[add_mask>0]=255

    # 膨胀核
    kernel = np.ones((16, 16), np.uint8)
    # 进行膨胀处理
    add_mask = cv2.dilate(add_mask, kernel, iterations=1)
    # 进行收缩处理
    add_mask = cv2.erode(add_mask, kernel, iterations=1)
    
    contours, hierarchy = cv2.findContours(add_mask,
                                            cv2.RETR_TREE,
                                            cv2.CHAIN_APPROX_SIMPLE)

    cropped_frame = raw_frame
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if area > 2000:
            x, y, w, h = cv2.boundingRect(contour)
            cropped_frame = raw_frame[y:y + h, x:x + w]
            raw_frame = cv2.rectangle(raw_frame, (x, y),
                                    (x + w, y + h),
                                    (0, 0, 255), 2)

            cv2.putText(raw_frame, "ADD MASK", (x, y),
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
    color = [color1, color2, color3, color4]
    print(color1, color2, color3, color4)
    for i in range(4):
        if color[i] == target_color:
            final_string += str(i+1)
    if final_string == laststring:
        count += 1
    else:
        count = 0
    if (count > 64):
        ser.write(final_string.encode())
        print(final_string)
    laststring = final_string
    final_string = ''
    
    color_detection_list = [COLOR_TO_GRB[color1], COLOR_TO_GRB[color2], COLOR_TO_GRB[color3], COLOR_TO_GRB[color4]]

    # Updates display
    color_display_1.update_color_array(color_detection_list)
    color_display_1.display()


    frame_blur = cv2.cvtColor(frame_blur, cv2.COLOR_HSV2BGR)
    add_mask = cv2.cvtColor(add_mask, cv2.COLOR_GRAY2BGR)
    red_mask = cv2.cvtColor(red_mask, cv2.COLOR_GRAY2BGR)
    green_mask = cv2.cvtColor(green_mask, cv2.COLOR_GRAY2BGR)
    blue_mask = cv2.cvtColor(blue_mask, cv2.COLOR_GRAY2BGR)

    raw_frame = add_title(raw_frame, "Raw Frame")
    frame_blur = add_title(frame_blur, "Blur Frame")
    add_mask = add_title(add_mask, "Add Mask")
    red_mask = add_title(red_mask, "Red Mask", color=(0, 0, 255))
    green_mask = add_title(green_mask, "Green Mask", color=(0, 255, 0))
    blue_mask = add_title(blue_mask, "Blue Mask", color=(255, 0, 0))
   
    frame_show_1_1 = cv2.hconcat([raw_frame, frame_blur,add_mask])
    frame_show_1_2 = cv2.hconcat([red_mask, green_mask, blue_mask])
    
    cv2.imshow("frame", cv2.vconcat([frame_show_1_1, frame_show_1_2]))
    cv2.imshow("cropped_frame", cropped_frame)

    if cv2.waitKey(10) & 0xFF == ord("q"):  # waits for 'q' key to be pressed
        ser.close() 
        break

cv2.destroyAllWindows()