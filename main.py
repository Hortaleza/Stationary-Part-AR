import cv2
import numpy as np

# Global variable that holds the BGR values of your detection for the code to output
color_detection_list = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 0, 0)]


# You should have no reason to modify this class
class ColorDisplayWindow:
    def __init__(
            self,
            window_height=300,
            window_width=2200,
            window_name="displayWindow",
            group_name="Group name here",
    ):
        global color_detection_list
        self.group_name = group_name
        self.window_height = window_height
        self.window_width = window_width
        self.window_name = window_name

        self.title_height = 100
        self.window = np.zeros(
            (window_height + self.title_height, window_width, 3), dtype=np.uint8
        )

        self.color_detection_count = len(color_detection_list)
        self.color_box_width = int(self.window_width / self.color_detection_count)
        self.color_box_height = self.window_height

        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.font_scale = 2
        self.font_thickness = 5

    # helper function to draw the color boxes
    def display(self):
        global color_detection_list

        # add a white title bar
        self.window[self.window_height:, :] = (255, 255, 255)

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
            color = color_detection_list[i]
            color_box = np.zeros(
                (self.color_box_height, self.color_box_width, 3), dtype=np.uint8
            )
            color_box[:] = color
            self.window[
            : self.color_box_height,
            i * self.color_box_width: (i + 1) * self.color_box_width,
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


if __name__ == "__main__":
    # TODO: Change your team's name and modify the size of the window to your liking
    color_display_1 = ColorDisplayWindow(
        window_height=500,
        window_width=500,
        window_name="displayWindow1",
        group_name="RDC Team 11",
    )

    # for fun only
    x = 0

    while True:
        # for fun only
        if x < 256:
            x += 1
        else:
            x = 0

        # TODO: You should constantly update the values of color_detection_list based on the BGR values you get
        color_detection_list = [(x, 0, 0), (0, x, 0), (0, 0, x), (x, 0, x)]

        # Updates display
        color_display_1.display()

        if cv2.waitKey(10) & 0xFF == ord("q"):  # waits for 'q' key to be pressed
            break

    cv2.destroyAllWindows()