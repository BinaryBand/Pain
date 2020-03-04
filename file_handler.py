from cv2 import imread, imwrite
import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfile
import threading


"""
Open a window to ask user where the file should be saved.
"""
def get_file_location():
    tk.Tk().withdraw()
    return askopenfilename()


"""
Open an image file from specified location.
"""
def open_file(_):
    location = get_file_location()

    if location is not None:
        return imread(location)


"""
Save a file to a specific location.
"""
def save_file(image):
    location = get_file_location()
    
    if location is not None:
        imwrite(f"{location}.png", image)
