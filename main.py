import cv2
from numpy import full, uint8
from file_handler import open_file, save_file


"""
Previous mouse position.
"""
class Mouse:
    x, y, click = None, None, None


"""
Drawing element.
"""
class Canvas:
    def __init__(self, x, y, width, height):
        self.x, self.y = x, y
        self.width = width
        self.height = height
        self.canvas = full((height, width, 3), (255, 255, 255), dtype=uint8)

    # Detect mouse clicks and allow user to draw
    def update(self, x, y):
        draw_line(self.canvas, Mouse.x - self.x, Mouse.y - self.y, x - self.x, y - self.y, 2)

    # Draw this object on screen
    def draw(self, canvas):
        canvas[self.y:self.y+self.height, self.x:self.x+self.width] = self.canvas


"""
Draw text to the screen.
"""
def write_text(frame, text, x, y, color=(255, 255, 255), size=1):
    font = cv2.FONT_HERSHEY_SIMPLEX
    lineType = 2
    cv2.putText(frame, text, (x, y), font, size, color, lineType)


"""
Draw a line.
"""
def draw_line(image, x1, y1, x2, y2, thickness=1, color=(0, 0, 0)):

    # Draw a line on the image
    cv2.line(image, (x1, y1), (x2, y2), color, thickness)


"""
Mouse callback function.
"""
def draw(event, x, y, flags, objects):

    # If mouse is clicked
    if flags == 1 and Mouse.x is not None:

        for obj in objects:
            obj.update(x, y)

    # Set the previous mouse position
    Mouse.x, Mouse.y, Mouse.click = x, y, flags == 1


"""
Main function.
"""
def main():

    # Windows title
    title = "MacroSoup Pain"
    fps = 30

    # Frame to place objects on
    screen = full((480, 640, 3), (0, 0, 0), dtype=uint8)
    # canvas = open_file()

    # Create a window
    cv2.namedWindow(title, cv2.WND_PROP_FULLSCREEN)
    
    # # Set full screen
    # setWindowProperty(title, WND_PROP_FULLSCREEN, WINDOW_FULLSCREEN)

    # Create objects to place on the screen
    objects = []
    objects.append(Canvas(100, 100, 540, 380))

    # Execute the 'draw' function each time a mouse click is detected
    cv2.setMouseCallback(title, draw, objects)

    # Application loop
    while True:

        for obj in objects:
            obj.draw(screen)

        # Display image
        cv2.imshow(title, screen)

        # Wait to display next image and get keystrokes
        key = cv2.waitKey(1000 // fps) & 0xFF

        # If escape key is pressed
        if key == 27:
            break

    # Close the window
    cv2.destroyAllWindows()

    # # Save screen to a file
    # save_file(screen)


if __name__ == "__main__":
    main()    
