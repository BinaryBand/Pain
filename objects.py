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
    cursor_size = 1


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
            draw_line(self.canvas, Mouse.x - self.x, Mouse.y - self.y, x - self.x, y - self.y, Mouse.cursor_size, Mouse.color)

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
        canvas[self.y:self.y+self.height, self.x:self.x+self.width] = (200, 200, 200) if self.mouse_hover else (250, 250, 250)
        write_text(canvas, self.text, self.x + int((self.width // len(self.text)) - 1.6 * len(self.text)), self.y  + int(1.5 * (self.height // 2)) , self.text_size, 2)

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
DropDown Menu
A menu that drops down with options when clicked on
"""
class Drop_down:
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
        #don't display drop down when not clicked
        if self.clicked is False:
            canvas[self.y:self.y+self.height, self.x:self.x+self.width] = (230, 230, 230) if self.mouse_hover else (250, 250, 250)
            write_text(canvas, self.current_item, self.x , self.y + self.height // 2  + 4, self.text_size, 2)
            #draw dropdown arrow
            canvas[self.y:self.y+self.height, self.x + self.width:self.x + self.width + 20] = (210, 210, 210) if self.mouse_hover else (180, 180, 180)
            write_text(canvas, "V",self.x + self.width + 6,self.y + self.height // 2  + 5, self.text_size, 2)
        #display dropdown menu when button is clicked
        if self.clicked is True:
            offset = 1
            canvas[self.y + self.height :self.y + (self.height * (len(self.item_list) + 1)),self.x:self.x + self.width] = (200,200,200)
            for items in self.item_list:
                # write out the options in the dropdown menu
                write_text(canvas, items, self.x + 4, self.y + ((offset + 1) * self.height) - self.height//2  + 4, self.text_size, 2)
                offset += 1

            #get the area for the dropdown menu.
            self.mouse_select = self.x < self.M_x < self.x + self.width and self.y < self.M_y < self.y + (self.height * (len(self.item_list) + 1))

            #if the mouse is clicked in the dropdown menu. execute the function
            if self.mouse_select and Mouse.press:
                index = ((self.M_y - (self.y + self.height))//self.height)
                self.function(index)
                #set the picked item in the list to current_item
                self.current_item = self.item_list[index]
                self.clicked = False
                #remove the drop down menu
                canvas[self.y:self.y + (self.height * (len(self.item_list) + 1)),self.x:self.x + self.width] = (220,210,210)
            #if the mouse clicks outside the dropdown menu don't do anything and remove the dropdown
            elif not self.mouse_select and Mouse.press:
                self.clicked = False
                #remove the dropdown menu
                canvas[self.y:self.y + (self.height * (len(self.item_list) + 1)),self.x:self.x + self.width] = (220,210,210)

    def update(self,x,y,clicked):
        self.mouse_hover = self.x < x < self.x + self.width + 20 and self.y < y < self.y + self.height
        if self.mouse_hover and Mouse.press:
            self.clicked = True
        #current x and y coordinates of mouse
        self.M_x = x
        self.M_y = y
            #loop through items in list and create dropdown menu




"""
Menu_bar
A menu Object to hold clickable objects
"""
class Menu_bar:
    def __init__(self,canvas):
        self.x, self.y = 0, 0
        self.width, self.height = canvas.width, 70

    def draw(self, canvas):
        canvas[self.y:self.y+self.height, self.x:self.x+self.width] = (220,210,210)

    def update(self,x,y,clicked):
        if self.width != cv2.WINDOW_NORMAL:
            self.width = cv2.WINDOW_NORMAL
