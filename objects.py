from drawing import draw_line, write_text
from numpy import full, uint8
from file_handler import open_file, save_file


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
    def __init__(self, x, y, width, height, text, function):
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.mouse_hover = False
        self.text = text
        self.function = function

    # Execute function on click.
    def update(self, x, y, clicked):
        self.mouse_hover = self.x < x < self.x + self.width and self.y < y < self.y + self.height

        if self.mouse_hover and Mouse.press:
            self.function()

    # Draw button on screen.
    def draw(self, canvas):
        canvas[self.y:self.y+self.height, self.x:self.x+self.width] = (250, 250, 250) if self.mouse_hover else (225, 225, 225)
        write_text(canvas, self.text, self.x, self.y + 24, 1, 2)