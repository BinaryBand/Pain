import cv2
import numpy as np
from objects import Mouse, Canvas, Button, MenuBar, ColorButton, CurrentColor, DropDown, CanvasDropDown, Label
from numpy import full, uint8


"""
Change mouse Color to new color.
"""
def set_color(color):
    Mouse.color = color

def pencil_size(size):
    Mouse.cursor_size = size + 1

def image_saturation_red(percent, canvas_class):
    new_image = np.copy(canvas_class.canvas)
    new_image[:, :, 0] = canvas_class.canvas[:,:,0] * ((10 - percent)/10)
    new_image[:, :, 1] = canvas_class.canvas[:,:,1] * ((10 - percent)/10)
    canvas_class.canvas = new_image

def image_saturation_green(percent,canvas_class):
    new_image = np.copy(canvas_class.canvas)
    new_image[:, :, 0] = canvas_class.canvas[:,:,0] * ((10 - percent)/10)
    new_image[:, :, 2] = canvas_class.canvas[:,:,1] * ((10 - percent)/10)
    canvas_class.canvas = new_image

def image_saturation_blue(percent,canvas_class):
    new_image = np.copy(canvas_class.canvas)
    new_image[:, :, 1] = canvas_class.canvas[:,:,1] * ((10 - percent)/10)
    new_image[:, :, 2] = canvas_class.canvas[:,:,2] * ((10 - percent)/10)
    canvas_class.canvas = new_image

def image_blur(percent,canvas_class):
    if percent > 0:
        new_image = cv2.blur(canvas_class.canvas,(2 * percent,2 * percent))
        canvas_class.canvas = new_image

"""
Add objects to screenzzzz
"""
def populate_frame(width):

    # Create elements to place on the screen
    canvas = Canvas(5, 75, 600, 390) # Must remain item 0 in OBJ array

    # Button(x,y,width,height,text,texsize,function)
    elements = []
    elements.append(canvas)
    elements.append(MenuBar(canvas, width))

    # Elements.append(Button(10, 10, 100, 50, "Clear", canvas.clear))
    elements.append(Button(10, 10, 50, 25, "Save", 0.75, canvas.export))
    elements.append(Button(10, 40, 50, 25, "Load" , 0.75, canvas.load))
    # elements.append(Button(550, 30, 50,25, "Undo" , 0.75, ))

    # Color pallet default set (BGR) 
    elements.append(ColorButton(230, 30, 15, 15, (255, 255, 255), set_color))   # Black
    elements.append(ColorButton(230, 10, 15, 15, (0, 0, 0), set_color))         # White
    elements.append(ColorButton(250, 30, 15, 15, (200, 200, 200), set_color))   # DarkGray
    elements.append(ColorButton(250, 10, 15, 15, (0, 0, 128), set_color))       # DarkRed
    elements.append(ColorButton(270, 30, 15, 15, (64, 64, 128), set_color))     # Brown
    elements.append(ColorButton(270, 10, 15, 15, (0, 0, 255), set_color))       # Red
    elements.append(ColorButton(290, 30, 15, 15, (128, 128, 255), set_color))   # Pink
    elements.append(ColorButton(290, 10, 15, 15, (0, 128, 255), set_color))     # Orange
    elements.append(ColorButton(310, 30, 15, 15, (128, 255, 255), set_color))   # Gold
    elements.append(ColorButton(310, 10, 15, 15, (0, 255, 255), set_color))     # Yellow
    elements.append(ColorButton(330, 30, 15, 15, (64, 128, 255), set_color))    # Tan
    elements.append(ColorButton(330, 10, 15, 15, (0, 255, 0), set_color))       # Green
    elements.append(ColorButton(350, 30, 15, 15, (0, 255, 128), set_color))     # Lime
    elements.append(ColorButton(350, 10, 15, 15, (255, 0, 0), set_color))       # Blue
    elements.append(ColorButton(370, 30, 15, 15, (255, 255, 0), set_color))     # Light Blue
    elements.append(ColorButton(370, 10, 15, 15, (160, 0, 0), set_color))       # Dark Blue
    
    # elements.append(ColorButton(230, 10, 15, 15, "Eraser",set_color))         # White
    elements.append(Label(80, 0, 0.6, "Eraser"))
    # Dropdown menu pencil size
    elements.append(DropDown(80, 10, 70, 20, ["small", "medium", "large"],(255,255,255) ,pencil_size, 0.6 ,canvas))

    # CanvasDropdown menu RGB saturation
    elements.append(Label(555,0,0.6,"B#"))

    elements.append(CanvasDropDown(550,15,30,18, ["0%","10%","20%","30%","40%","50%","60%","70%","80%","90%","100%"], image_saturation_blue, 0.5, canvas.history, canvas.update, canvas.x, canvas.y, canvas.width, canvas.height, canvas.first, canvas.canvas, canvas))
    elements.append(Label(503,0,0.6,"G#"))
    elements.append(CanvasDropDown(498,15,30,18, ["0%","10%","20%","30%","40%","50%","60%","70%","80%","90%","100%"], image_saturation_green, 0.5, canvas.history, canvas.update, canvas.x, canvas.y, canvas.width, canvas.height, canvas.first, canvas.canvas, canvas))
    elements.append(Label(449,0,0.6,"R#"))
    elements.append(CanvasDropDown(444,15,30,18, ["0%","10%","20%","30%","40%","50%","60%","70%","80%","90%","100%"], image_saturation_red, 0.5,canvas.history, canvas.update, canvas.x, canvas.y, canvas.width, canvas.height, canvas.first, canvas.canvas, canvas))
    # 555 0, 550 15
    # CanvasDropdown menu ImageBlur
    elements.append(Label(393,0,0.6,"Blur"))
    elements.append(CanvasDropDown(390,15,30,18, ["0%","10%","20%","30%","40%","50%","60%","70%","80%","90%","100%"], image_blur, 0.5, canvas.history, canvas.update, canvas.x, canvas.y, canvas.width, canvas.height, canvas.first, canvas.canvas, canvas))

    # This object displays the currently selected color
    elements.append(CurrentColor(180, 10, 35, 35))

    return elements, canvas


"""
Mouse callback function.
"""
def mouse_event(event, x, y, flags, elements):

    for obj in elements:
        obj.update(x, y, flags == 1)

    # Set the previous mouse position
    Mouse.x = x
    Mouse.y = y
    Mouse.press = Mouse.click != (flags == 1) and Mouse.click
    Mouse.release = Mouse.click != (flags == 1) and not Mouse.click
    Mouse.click = flags == 1


"""
Draw all elements on screen.
"""
def draw(elements, screen):
    screen[:] = (225, 225, 225)
    for obj in elements:
        obj.draw(screen)


"""
Main function.
"""
def main():
    
    title = "MacroSoup Pain"                                # Windows title
    fps = 30                                                # Frames per second

    window_width, window_height = 640, 480
    screen = full((window_height, window_width, 3), (0, 0, 0), dtype=uint8)     # Frame to draw our object
    cv2.namedWindow(title)                                                      # Create a window

    elements, canvas = populate_frame(window_width)

    # Execute the 'mouse_event' function each time a mouse event is detected
    cv2.setMouseCallback(title, mouse_event, elements)

    draw(elements, screen)

    # Application loop
    while cv2.getWindowProperty(title, cv2.WND_PROP_VISIBLE) != 0:

        draw(elements, screen)

        # Display image
        cv2.imshow(title, screen)

        # Wait to display next image and get keystrokes
        key = cv2.waitKey(1000 // fps) & 0xFF

        if key == ord("z"):
            canvas.undo()

    # Close the window upon exiting application loop
    cv2.destroyWindow(title)


if __name__ == "__main__":
    main()
