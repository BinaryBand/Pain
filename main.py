import cv2
from objects import Mouse, Canvas, Button, MenuBar, ColorButton, CurrentColor, DropDown
from numpy import full, uint8


"""
Change mouse Color to new color.
"""
def set_color(color):
    Mouse.color = color

def font_size(size):
    Mouse.cursor_size = size + 1

"""
Add objects to screen
"""
def populate_frame():

    # Create elements to place on the screen
    canvas = Canvas(0, 70, 640, 410) ## must remain item 0 in OBJ array

    # Button(x,y,width,height,text,texsize,function)
    elements = []
    elements.append(canvas)
    elements.append(MenuBar(canvas))

    # Elements.append(Button(10, 10, 100, 50, "Clear", canvas.clear))
    elements.append(Button(10, 10, 50, 25, "Save", 0.75, canvas.export))
    elements.append(Button(10, 40, 50, 25, "Load" , 0.75, None))

    # Color pallet default set (BGR) 
    elements.append(ColorButton(230, 30, 15, 15, (255, 255, 255), set_color))    # Black
    elements.append(ColorButton(230, 10, 15, 15, (0, 0, 0),set_color))           # White
    elements.append(ColorButton(250, 30, 15, 15, (200, 200, 200),set_color))     # DarkGray
    elements.append(ColorButton(250, 10, 15, 15, (0, 0, 128),set_color))         # DarkRed
    elements.append(ColorButton(270, 30, 15, 15, (64, 64, 128),set_color))       # Brown
    elements.append(ColorButton(270, 10, 15, 15, (0, 0, 255),set_color))         # Red
    elements.append(ColorButton(290, 30, 15, 15, (128, 128, 255),set_color))     # Pink
    elements.append(ColorButton(290, 10, 15, 15, (0, 128, 255),set_color))       # Orange
    elements.append(ColorButton(310, 30, 15, 15, (128, 255, 255),set_color))     # Gold
    elements.append(ColorButton(310, 10, 15, 15, (0, 255, 255),set_color))       # Yellow
    elements.append(ColorButton(330, 30, 15, 15, (64, 128, 255),set_color))      # Tan
    elements.append(ColorButton(330, 10, 15, 15, (0, 255, 0),set_color))         # Green
    elements.append(ColorButton(350, 30, 15, 15, (0, 255, 128),set_color))       # Lime
    elements.append(ColorButton(350, 10, 15, 15, (255, 0, 0),set_color))         # Blue
    elements.append(ColorButton(370, 30, 15, 15, (255, 255, 0),set_color))       # Light Blue
    elements.append(ColorButton(370, 10, 15, 15, (160, 0, 0),set_color))         # Dark Blue
    
    # Dropdown menu pencil size
    elements.append(DropDown(80, 10, 70, 20, ["small", "medium", "large"], font_size, 0.6 ,canvas))

    # This object displays the currently selected color
    elements.append(CurrentColor(180, 10, 35, 35))

    return elements, canvas


"""
Mouse callback function.
"""
def mouse_event(event, x, y, flags, objects):

    for obj in objects:
        obj.update(x, y, flags == 1) # canvas

    # Set the previous mouse position
    Mouse.x = x
    Mouse.y = y
    Mouse.press = Mouse.click != (flags == 1) and not Mouse.click
    Mouse.click = flags == 1


"""
Main function.
"""
def main():
    
    title = "MacroSoup Pain"                                # Windows title
    fps = 30                                                # Frames per second

    screen = full((480, 640, 3), (0, 0, 0), dtype=uint8)    # Frame to draw our object
    cv2.namedWindow(title)                                  # Create a window

    elements, canvas = populate_frame()

    # Execute the 'mouse_event' function each time a mouse event is detected
    cv2.setMouseCallback(title, mouse_event, elements)

    # Application loop
    while cv2.getWindowProperty(title, cv2.WND_PROP_VISIBLE) != 0:

        for obj in elements:
            obj.draw(screen)

        # Display image
        cv2.imshow(title, cv2.blur(screen,(1, 1)))

        # Wait to display next image and get keystrokes
        key = cv2.waitKey(1000 // fps) & 0xFF

        if key == ord("z"):
            canvas.undo()

    # Close the window upon exiting application loop
    cv2.destroyWindow(title)


if __name__ == "__main__":
    main()
