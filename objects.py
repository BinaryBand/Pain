from drawing import draw_line, write_text
from numpy import full, uint8, array, zeros, uint8, append
from file_handler import open_file, save_file
import cv2
import numpy as np


def resize(image, new_width, new_height):
    new_canvas = full((new_height, new_width, 3), (255, 255, 255), dtype=uint8)
    old_height, old_width, _ = image.shape
    new_canvas[:old_height,:old_width] = image
    return new_canvas


"""
Previous mouse position.
"""
class Mouse:
    x, y = None, None
    click = False
    press = False
    release = False
    color = (0, 0, 0)
    cursor_size = 1


"""
Drawing element.
"""
class Canvas:
    def __init__(self, x, y, width, height):
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.canvas = full((height, width, 3), (255, 255, 255), dtype=uint8)
        self.history = []
        self.first = full((height, width, 3), (255, 255, 255), dtype=uint8)
        self.current = self.canvas

        self.resize_x, self.resize_y = False, False
        self.hover_x, self.hover_y = False, False

    # Detect mouse clicks and allow user to draw
    def update(self, x, y, clicked):
        self.hover_x = self.width + self.x - 5 < Mouse.x < self.width + self.x + 5 if Mouse.x else False
        self.hover_y = self.height + self.y - 5 < Mouse.y < self.height + self.y + 5 if Mouse.y else False

        if Mouse.press or Mouse.release:
            if self.hover_x: self.resize_x = Mouse.click
            if self.hover_y: self.resize_y = Mouse.click

        if self.resize_x or self.resize_y:
            if self.resize_x: self.width = max(1, Mouse.x - self.x)     # Resize canvas width
            if self.resize_y: self.height = max(1, Mouse.y - self.y)    # Resize canvas height
        else:
            if Mouse.press:
                self.history.append(self.canvas)
                if 30 < len(self.history):
                    self.history.pop(0)
                    self.first = self.history[0]
            if clicked:
                draw_line(self.canvas, Mouse.x - self.x, Mouse.y - self.y, x - self.x, y - self.y, Mouse.cursor_size, Mouse.color)

        canvas_height, canvas_width, _ = self.canvas.shape
        self.canvas = resize(self.canvas, max(self.width, canvas_width), max(self.height, canvas_height))


    # Draw this object on screen
    def draw(self, canvas):
        # Draw border
        canvas[self.y - 1: self.y + self.height + (3 if self.hover_y else 1), self.x - 1: self.x + self.width + (3 if self.hover_x else 1)] = (0, 0, 0)
        
        # Draw image
        canvas[self.y:self.y+self.height, self.x:self.x+self.width] = self.canvas[:self.height,:self.width]

    # Fill canvas with white
    def clear(self):
        self.canvas[:,:] = (255, 255, 255)

    # Save image to local storage
    def export(self):
        save_file(self.canvas[:self.height,:self.width])

    def load(self):
        new_image = open_file()
        height, width, _ = new_image.shape
        self.height, self.width = height, width
        self.canvas = new_image
        self.first = new_image

    def undo(self):
        prev = None
        if len(self.history) != 0:
            prev = self.history[-1]
            self.history.pop(-1)
        else:
            prev = np.copy(self.first)
        
        # Undo, resize if necessary
        new_height, new_width, _ = self.canvas.shape
        self.width, self.height = new_width, new_height
        self.resize_x, self.resize_y, self.hover_x, self.hover_y = False, False, False, False
        self.canvas = resize(prev, new_width, new_height)


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

        if self.mouse_hover and Mouse.release:
            self.function()

    # Draw button on screen.
    def draw(self, canvas):
        canvas[self.y - 1:self.y+self.height + 1, self.x - 1:self.x+self.width + 1] = [100,100,100]
        canvas[self.y:self.y+self.height, self.x:self.x+self.width] = (200, 200, 200) if self.mouse_hover else (250, 250, 250)
        write_text(canvas, self.text, self.x + int((self.width // len(self.text)) - 1.6 * len(self.text)), self.y  + int(1.5 * (self.height // 2)) , self.text_size, 1)

class ColorButton:
    def __init__(self, x, y, width, height,color, function):
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.mouse_hover = False
        self.color = color
        self.function = function

    # Execute function on click.
    def update(self, x, y, clicked):
        self.mouse_hover = self.x < x < self.x + self.width and self.y < y < self.y + self.height
        if self.mouse_hover and Mouse.release:
            self.function(self.color)

    # Draw button on screen.
    def draw(self, canvas):
        canvas[self.y - 1:self.y+self.height + 1, self.x - 1:self.x+self.width + 1] = [100,100,100]
        canvas[self.y:self.y+self.height, self.x:self.x+self.width] = self.color 


class CurrentColor:
    def __init__(self, x, y, width, height):
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.mouse_hover = False
        self.color = (0, 0, 0)

    # Execute function on click.
    def update(self, x, y, clicked):
        self.color = Mouse.color

    # Draw Element on screen.
    def draw(self, canvas):
        canvas[self.y - 1:self.y+self.height + 1, self.x - 1:self.x+self.width + 1] = [100,100,100]
        canvas[self.y:self.y+self.height, self.x:self.x+self.width] = self.color 
        write_text(canvas, "Color", self.x , self.y + self.height + 10 , 0.5, 1)


"""
DropDown Menu
A menu that drops down with options when clicked on
"""
class DropDown:
    def __init__(self,x,y,width,height,item_list,function, text_size , canvas):
        self.x, self.y = x, y
        self.canvas = canvas
        self.width, self.height = width,height
        self.item_list = item_list
        self.function = function
        self.current_item = item_list[0]
        self.clicked = False
        self.mouse_hover = False
        self.mouse_select = False
        self.text_size = text_size

    def draw(self, canvas):
        # Draw the container and text
        canvas[self.y:self.y+self.height, self.x:self.x+self.width] = (230, 230, 230) if self.mouse_hover else (250, 250, 250)
        write_text(canvas, self.current_item, self.x , self.y + self.height // 2  + 4, self.text_size, 1)
        
        # Draw the container and dropdown arrow
        # Don't display drop down when not clicked
        canvas[self.y - 1:self.y+self.height + 1, self.x - 1:self.x+self.width + 1] = [100,100,100]
        canvas[self.y:self.y+self.height, self.x:self.x+self.width] = (230, 230, 230) if self.mouse_hover else (250, 250, 250)
        write_text(canvas, self.current_item, self.x , self.y + self.height // 2  + 4, self.text_size, 1)
        
        # Draw dropdown arrow
        canvas[self.y - 1:self.y+self.height + 1, self.x + self.width - 1:self.x + self.width + 21] = [100,100,100]
        canvas[self.y:self.y+self.height, self.x + self.width:self.x + self.width + 20] = (210, 210, 210) if self.mouse_hover else (180, 180, 180)
        write_text(canvas, "V",self.x + self.width + 6,self.y + self.height // 2  + 5, self.text_size, 2)
        
        # Display dropdown menu when button is clicked
        if self.clicked is True:
            canvas[self.y - 1:self.y+self.height + 1, self.x - 1:self.x+self.width + 1] = [100,100,100]
            canvas[self.y + self.height :self.y + (self.height * (len(self.item_list) + 1)),self.x:self.x + self.width] = (200,200,200)
            
            # Write out the options in the dropdown menu
            for index, items in enumerate(self.item_list):
                write_text(canvas, items, self.x + 4, self.y + ((index + 2) * self.height) - self.height//2  + 4, self.text_size, 1)

            #get the area for the dropdown menu.
            self.mouse_select = self.x < Mouse.x < self.x + self.width and self.y < Mouse.y < self.y + (self.height * (len(self.item_list) + 1))

            #if the mouse is clicked in the dropdown menu. execute the function
            if self.mouse_select and Mouse.release:
                index = ((Mouse.y - (self.y + self.height))//self.height)
                self.function(index)

                #set the picked item in the list to current_item
                self.current_item = self.item_list[index]
                self.clicked = False

                #remove the drop down menu
                canvas[self.y:self.y + (self.height * (len(self.item_list) + 1)),self.x:self.x + self.width] = (220,210,210)

            #if the mouse clicks outside the dropdown menu don't do anything and remove the dropdown
            elif not self.mouse_select and Mouse.release:
                self.clicked = False
                #remove the dropdown menu
                canvas[self.y:self.y + (self.height * (len(self.item_list) + 1)),self.x:self.x + self.width] = (220,210,210)

    def update(self,x,y,clicked):
        self.mouse_hover = self.x < x < self.x + self.width + 20 and self.y < y < self.y + self.height
        if self.mouse_hover and Mouse.release:
            self.clicked = True

# a dropdown menu that allows edits to the canvas
class CanvasDropDown:
    def __init__(self,x,y,width,height,item_list,function, text_size ,c_history, c_draw, cx, cy, c_width,c_height, c_first, c_current):
        # information about dropdown menu
        self.x, self.y = x, y
        self.width, self.height = width,height
        self.item_list = item_list
        self.function = function
        self.current_item = item_list[0]
        self.clicked = False
        self.mouse_hover = False
        self.mouse_select = False
        self.text_size = text_size

        # information about the draw area
        self.cx = cx
        self.cy = cy
        self.c_history = c_history
        self.c_draw = c_draw
        self.c_width = c_width
        self.c_height = c_height
        self.c_first = c_first
        self.c_current = c_current

    def draw(self, canvas):

        # Don't display drop down when not clicked
        canvas[self.y - 1:self.y+self.height + 1, self.x - 1:self.x+self.width + 1] = [100,100,100]
        canvas[self.y:self.y+self.height, self.x:self.x+self.width] = (230, 230, 230) if self.mouse_hover else (250, 250, 250)
        
        # Draw dropdown arrow
        canvas[self.y - 1:self.y+self.height + 1, self.x + self.width - 1:self.x + self.width + 21] = [100,100,100]
        canvas[self.y:self.y+self.height, self.x + self.width:self.x + self.width + 20] = (210, 210, 210) if self.mouse_hover else (180, 180, 180)
        write_text(canvas, "V",self.x + self.width + 6,self.y + self.height // 2  + 5, self.text_size, 2)

        # Display dropdown menu when button is clicked
        if self.clicked is True:
            canvas[self.y - 1:self.y+self.height + 1, self.x - 1:self.x+self.width + 1] = [100,100,100]
            canvas[self.y + self.height :self.y + (self.height * (len(self.item_list) + 1)),self.x:self.x + self.width] = (200,200,200)
            
            for index, items in enumerate(self.item_list):
                # write out the options in the dropdown menu
                write_text(canvas, items, self.x + 4, self.y + ((index + 2) * self.height) - self.height//2  + 4, self.text_size, 1)

            #get the area for the dropdown menu.
            self.mouse_select = self.x < Mouse.x < self.x + self.width and self.y < Mouse.y < self.y + (self.height * (len(self.item_list) + 1))

            #if the mouse is clicked in the dropdown menu. execute the function
            if self.mouse_select and Mouse.release:
                index = ((Mouse.y - (self.y + self.height))//self.height)
                
               #remove the drop down menu
                canvas[self.y:self.y + (self.height * (len(self.item_list) + 1)),self.x:self.x + self.width] = (220,210,210)

                #includes canvas in the update
                if len(self.c_history) > 0:
                    draw_area = self.c_history[-1]
                else:
                    draw_area = self.c_first

                check = self.function(index,draw_area)
                self.c_history.append(array(check))
                self.c_current = check

                #set the picked item in the list to current_item
                self.current_item = self.item_list[index]
                self.clicked = False

            #if the mouse clicks outside the dropdown menu don't do anything and remove the dropdown
            elif not self.mouse_select and Mouse.release:
                self.clicked = False
                #remove the dropdown menu
                canvas[self.y:self.y + (self.height * (len(self.item_list) + 1)),self.x:self.x + self.width] = (220,210,210)

    def update(self,x,y,clicked):
        self.mouse_hover = self.x < x < self.x + self.width + 20 and self.y < y < self.y + self.height
        if self.mouse_hover and Mouse.release:
            self.clicked = True    

class Label:
    def __init__(self,x,y, text_size, text):
        self.x, self.y = x, y
        self.text = text
        self.clicked = False
        self.mouse_hover = False
        self.mouse_select = False
        self.text_size = text_size

    def draw(self, canvas):
        # Don't display drop down when not clicked
        write_text(canvas, self.text, self.x , self.y + 10, self.text_size, 1)

    def update(self,x,y,clicked):
        pass

"""
Menu_bar
A menu Object to hold clickable objects
"""
class MenuBar:
    def __init__(self,canvas, width):
        self.x, self.y = 0, 0
        self.width, self.height = width, 70

    def draw(self, canvas):
        canvas[self.y: self.y + self.height, self.x: self.x + self.width] = (220,210,210)

    def update(self, x, y, clicked):
        pass
