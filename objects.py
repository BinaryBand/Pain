from drawing import draw_line, write_text
from numpy import full, uint8
from file_handler import open_file, save_file
import cv2


"""
Previous mouse position.
"""
class Mouse:
    x, y = None, None
    click = False
    press = False
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
        if clicked and Mouse.x is not None:
            draw_line(self.canvas, Mouse.x - self.x, Mouse.y - self.y, x - self.x, y - self.y, 3, Mouse.color)

    # Draw this object on screen
    def draw(self, canvas):
        canvas[self.y:self.y+self.height, self.x:self.x+self.width] = self.canvas

    # Fill canvas with white
    def clear(self):
        self.canvas[:,:] = (255, 255, 255)

    # Save image to local storage
    def export(self):
        save_file(self.canvas)


"""
A clickable object.
"""
class Button:
    def __init__(self, x, y, width, height, text, text_size, function):
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.mouse_hover = False
        self.text = text
        self.function = function
        self.text_size = text_size

    # Execute function on click.
    def update(self, x, y, clicked):
        self.mouse_hover = self.x < x < self.x + self.width and self.y < y < self.y + self.height

        if self.mouse_hover and Mouse.press:
            self.function()

    # Draw button on screen.
    def draw(self, canvas):
        canvas[self.y:self.y+self.height, self.x:self.x+self.width] = (250, 250, 250) if self.mouse_hover else (225, 225, 225)
        write_text(canvas, self.text, self.x + int((self.width // len(self.text)) - 1.6 * len(self.text)), self.y  + (self.height // 2) , self.text_size, 2)

class Color_Button:
    def __init__(self, x, y, width, height,color, function):
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.mouse_hover = False
        self.color = color
        self.function = function

    # Execute function on click.
    def update(self, x, y, clicked):
        self.mouse_hover = self.x < x < self.x + self.width and self.y < y < self.y + self.height
        if self.mouse_hover and Mouse.press:
            self.function(self.color)


    # Draw button on screen.
    def draw(self, canvas):
        canvas[self.y:self.y+self.height, self.x:self.x+self.width] = self.color

class Current_Color:
    def __init__(self, x, y, width, height):
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.mouse_hover = False
        self.color = (255,255,255)
    # Execute function on click.
    def update(self, x, y, clicked):
        self.color = Mouse.color


    # Draw Element on screen.
    def draw(self, canvas):
        canvas[self.y:self.y+self.height, self.x:self.x+self.width] = self.color
        write_text(canvas, "Color", self.x , self.y + self.height + 10 , 0.4, 2)
"""
A menu Object to hold clickable objects
"""
class Menu_bar:
    def __init__(self,x,y, width, height):
        self.x, self.y = x, y
        self.width, self.height = width, height

    def draw(self, canvas):
        canvas[self.y:self.y+self.height, self.x:self.x+self.width] = (100,100,100)

    def update(self,x,y,clicked):
        if(self.width != cv2.WINDOW_NORMAL):
            self.width = cv2.WINDOW_NORMAL