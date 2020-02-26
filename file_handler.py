from cv2 import imread, imwrite
import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfile


def get_file_location():
    tk.Tk().withdraw()
    return askopenfilename()


def set_file_location():
    return asksaveasfile(mode="w", defaultextension=".png").name


def open_file():
    location = get_file_location()

    if location is not None:
        return imread(location)


def save_file(image):
    location = set_file_location()

    print(location)

    if location is not None:
        imwrite(location, image)
