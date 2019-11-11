# coding=utf-8

import win32gui
from PIL import ImageGrab
from multiprocessing import Pool

def screenshot(filepath):
    HWND = win32gui.GetForegroundWindow()
    # Returns the rectangle for a window in screen coordinates
    # (left, top, right, bottom) = GetWindowRect(hwnd)
    bbox = win32gui.GetWindowRect(HWND)
    img = ImageGrab.grab(bbox=bbox)
    img.save(filepath)


if __name__ == "__main__":
    pass