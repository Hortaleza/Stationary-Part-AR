import cv2

def detect_colors():
    # Open the camera
    cap = cv2.VideoCapture(0)

    # Read four frames from the camera
    for _ in range(4):
        _, frame = cap.read()

    # Convert the frames to the HSV color space
    hsv_frames = [cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) for frame in frames]

    # Define the lower and upper bounds for red, blue, and green colors
    lower_red = (0, 100, 100)
    upper_red = (10, 255, 255)
    lower_blue = (110, 100, 100)
    upper_blue = (130, 255, 255)
    lower_green = (50, 100, 100)
    upper_green = (70, 255, 255)

    # Detect the red, blue, and green colors in each frame
    red_pixels = []
    blue_pixels = []
    green_pixels = []

    for hsv_frame in hsv_frames:
        red_mask = cv2.inRange(hsv_frame, lower_red, upper_red)
        blue_mask = cv2.inRange(hsv_frame, lower_blue, upper_blue)
        green_mask = cv2.inRange(hsv_frame, lower_green, upper_green)

        red_pixels.append(cv2.countNonZero(red_mask))
        blue_pixels.append(cv2.countNonZero(blue_mask))
        green_pixels.append(cv2.countNonZero(green_mask))

    # Release the camera
    cap.release()

    return red_pixels, blue_pixels, green_pixels

# Call the detect_colors function
red_pixels, blue_pixels, green_pixels = detect_colors()

# Print the number of red, blue, and green pixels detected in each frame
for i in range(4):
    print(f"Frame {i+1}: Red pixels: {red_pixels[i]}, Blue pixels: {blue_pixels[i]}, Green pixels: {green_pixels[i]}")
`