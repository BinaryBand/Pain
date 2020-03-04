import cv2
from numpy import full, uint8
from file_handler import open_file, save_file


"""
Previous mouse position.
"""
class Mouse:
    x, y = None, None
    click = False
    color = (0, 255, 0)


"""
Drawing element.
"""
class Canvas:
    def __init__(self, x, y, width, height):
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.canvas = full((height, width, 3), (255, 255, 255), dtype=uint8)

    # Detect mouse clicks and allow user to draw
    def update(self, x, y, clicked):
        if clicked:
            draw_line(self.canvas, Mouse.x - self.x, Mouse.y - self.y, x - self.x, y - self.y, 2, Mouse.color)

    # Draw this object on screen
    def draw(self, canvas):
        canvas[self.y:self.y+self.height, self.x:self.x+self.width] = self.canvas


"""
A clickable object.
"""
class Button:
    def __init__(self, x, y, width, height, text, function, param=None):
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.mouse_hover = False
        self.text = text
        self.function = function
        self.param = param

    def update(self, x, y, clicked):
        self.mouse_hover = self.x < x < self.x + self.width and self.y < y < self.y + self.height

        if self.mouse_hover and clicked:
            self.function(self.param)

    def draw(self, canvas):
        canvas[self.y:self.y+self.height, self.x:self.x+self.width] = (250, 250, 250) if self.mouse_hover else (225, 225, 225)
        write_text(canvas, self.text, self.x, self.y + self.height // 2)


"""
Draw text to the screen.
"""
def write_text(frame, text, x, y, size=1, color=(0, 0, 0)):
    font = cv2.FONT_HERSHEY_SIMPLEX
    lineType = 2
    cv2.putText(frame, text, (x, y), font, size, color, lineType)


"""
Draw a line.
"""
def draw_line(frame, x1, y1, x2, y2, thickness=1, color=(0, 0, 0)):

    # Draw a line on the image
    cv2.line(frame, (x1, y1), (x2, y2), color, thickness)


"""
Fill frame with white.
"""
def clear(frame):
    frame[:,:] = (255, 255, 255)


"""
Mouse callback function.
"""
def update(event, x, y, flags, objects):

    for obj in objects:
        obj.update(x, y, flags == 1)

    # Set the previous mouse position
    Mouse.x, Mouse.y, Mouse.click = x, y, flags == 1


"""
Main function.
"""
def main():
    
    title = "MacroSoup Pain"                                # Windows title
    fps = 30                                                # Frames per second

    screen = full((480, 640, 3), (0, 0, 0), dtype=uint8)    # Frame to draw our object
    cv2.namedWindow(title, cv2.WINDOW_KEEPRATIO)            # Create a window

    # Create objects to place on the screen
    objects = []
    objects.append(Canvas(0, 70, 640, 410))
    objects.append(Button(10, 10, 100, 50, "Clear", clear, objects[0].canvas))

    # Execute the 'update' function each time a mouse event is detected
    cv2.setMouseCallback(title, update, objects)

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

    # Close the window upon exiting application loop
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()    
