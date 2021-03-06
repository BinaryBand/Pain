from cv2 import imread, imwrite, resize
from numpy import zeros, uint
import tkinter as tk
tk.Tk().withdraw()
from tkinter.filedialog import askopenfilename, asksaveasfile
import threading


"""
Open a window to ask user where the file should be saved.
"""
def get_file_location():
    return askopenfilename()


"""
Prompt the user for a file path.
"""
def set_file_location():
    return asksaveasfile(mode="w", defaultextension=".png").name


"""
Open an image file from specified location.
"""
def open_file():
    location = get_file_location()

    if location is not None:
        imported_image = imread(location)
        height, width, _ = imported_image.shape
        
        if height > 400 or width > 630:
            scale = min(400 / height, 630 / width)

        return resize(imported_image, None, fx=scale, fy=scale)


        height, width, _ = imported_image.shape
        return imported_image[:min(height, 400),:min(width, 630),:]


"""
Save a file to a specific location.
"""
def save_file(image):
    location = set_file_location()
    
    if location is not None:
        imwrite(location, image)
