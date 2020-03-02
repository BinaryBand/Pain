from cv2 import line, namedWindow, setMouseCallback, imshow, waitKey, destroyAllWindows, WND_PROP_FULLSCREEN, WINDOW_FULLSCREEN, setWindowProperty
from numpy import full, uint8
from file_handler import open_file, save_file

"HI EVERYBODY!!!! Hello!"
"""
Previous mouse position.
"""
class Mouse:
    x, y, click = None, None, None


"""
Draw a line.
"""
def draw_line(image, x1, y1, x2, y2, thickness=1, color=(0, 0, 0)):

    # Draw a line on the image
    line(image, (x1, y1), (x2, y2), color, thickness)


"""
Mouse callback function.
"""
def draw(event, x, y, flags, param):

    # If mouse is clicked
    if flags == 1 and Mouse.x is not None:

        # Draw a line from the previous mouse position to the current
        draw_line(param, x, y, Mouse.x, Mouse.y, 2)

    # Set the previous mouse position
    Mouse.x, Mouse.y, Mouse.click = x, y, flags == 1


"""
Main function.
"""
def main():

    # Windows title
    title = "MacroSoup Pain"
    fps = 30

    # Frame to draw on
    canvas = open_file()

    # Create a window
    namedWindow(title, WND_PROP_FULLSCREEN)
    
    # # Set full screen
    # setWindowProperty(title, WND_PROP_FULLSCREEN, WINDOW_FULLSCREEN)

    # Execute the 'draw' function each time a mouse click is detected
    setMouseCallback(title, draw, canvas)

    # Application loop
    while True:

        # Display image
        imshow(title, canvas)

        # Wait to display next image and get keystrokes
        key = waitKey(1000 // fps) & 0xFF

        # If escape key is pressed
        if key == 27:
            break

    # Close the window
    destroyAllWindows()

    save_file(canvas)


if __name__ == "__main__":
    main()    
