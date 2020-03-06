import cv2
from objects import Mouse, Canvas, Button
from numpy import full, uint8

"HI EVERYBODY!!!! Hello!"
"""
Add objects to screen
"""
def populate_frame():

    # Create elements to place on the screen
    canvas = Canvas(0, 70, 640, 410)

    elements = []
    elements.append(canvas)
    elements.append(Button(10, 10, 100, 50, "Clear", canvas.clear))
    elements.append(Button(120, 10, 100, 50, "Export", canvas.export))

    return elements


"""
Mouse callback function.
"""
def mouse_event(event, x, y, flags, objects):

    for obj in objects:
        obj.update(x, y, flags == 1)

    # Set the previous mouse position
    Mouse.x = x
    Mouse.y = y
    Mouse.press = Mouse.click != (flags == 1)
    Mouse.click = flags == 1


"""
Main function.
"""
def main():
    
    title = "MacroSoup Pain"                                # Windows title
    fps = 30                                                # Frames per second

    screen = full((480, 640, 3), (0, 0, 0), dtype=uint8)    # Frame to draw our object
    cv2.namedWindow(title, cv2.WINDOW_KEEPRATIO)            # Create a window

    elements = populate_frame()

    # Execute the 'mouse_event' function each time a mouse event is detected
    cv2.setMouseCallback(title, mouse_event, elements)

    # Application loop
    while True:

        for obj in elements:
            obj.draw(screen)

        # Display image
        cv2.imshow(title, screen)

        # Wait to display next image and get keystrokes
        key = cv2.waitKey(1000 // fps) & 0xFF

        # If escape key is pressed
        if key == 27:
            break

    # Close the window upon exiting application loop
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()    
