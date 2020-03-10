from cv2 import line, putText, FONT_HERSHEY_COMPLEX_SMALL


"""
Draw text to the screen.
"""
def write_text(frame, text, x, y, size=1, weight=1, color=(0, 0, 0)):
    font = FONT_HERSHEY_COMPLEX_SMALL
    putText(frame, text, (x, y), font, size, color, weight)


"""
Draw a line.
"""
def draw_line(frame, x1, y1, x2, y2, thickness=1, color=(0, 0, 0)):
    line(frame, (x1, y1), (x2, y2), color, thickness)
