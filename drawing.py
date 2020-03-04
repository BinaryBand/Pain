from cv2 import line, putText, FONT_HERSHEY_SIMPLEX


"""
Draw text to the screen.
"""
def write_text(frame, text, x, y, size=1, color=(0, 0, 0)):
    font = FONT_HERSHEY_SIMPLEX
    lineType = 2
    putText(frame, text, (x, y), font, size, color, lineType)


"""
Draw a line.
"""
def draw_line(frame, x1, y1, x2, y2, thickness=1, color=(0, 0, 0)):
    line(frame, (x1, y1), (x2, y2), color, thickness)