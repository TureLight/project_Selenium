# coding=utf-8

"""
Author: zhangzheng
Description: Change The Style Of Console Print Message
Version: 0.0.1
LastUpdateDate:  2019-8-27
UpadteURL: 
LOG: 
    1. Support To Change The Color of Console Print Message
"""
import ctypes

STD_INPUT_HANDLE = -10
STD_OUTPUT_HANDLE = -11
STD_ERROR_HANDLE = -12

FOREGROUND_BLUE = 0x01  # text color contains blue.
FOREGROUND_GREEN = 0x02  # text color contains green.
FOREGROUND_RED = 0x04  # text color contains red.
FOREGROUND_WHITE = FOREGROUND_BLUE | FOREGROUND_GREEN | FOREGROUND_RED
FOREGROUND_YELLOW = FOREGROUND_RED | FOREGROUND_GREEN
FOREGROUND_INTENSITY = 0x08  # text color is intensified.

BACKGROUND_BLUE = 0x10  # background color contains blue.
BACKGROUND_GREEN = 0x20  # background color contains green.
BACKGROUND_RED = 0x40  # background color contains red.
BACKGROUND_INTENSITY = 0x80  # background color is intensified.


class Color:
    '''
        for information on Windows APIs.
        https://docs.microsoft.com/en-us/windows/console/console-screen-buffers#character-attributes
    '''
    std_out_handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)

    @classmethod
    def set_color(cls, color: int, handle=std_out_handle):
        bool = ctypes.windll.kernel32.SetConsoleTextAttribute(handle, color)
        return bool

    @classmethod
    def white_foreground_black_background(cls):
        cls.set_color(color=FOREGROUND_WHITE)

    @classmethod
    def white_bright_foreground_black_background(cls):
        cls.set_color(color=FOREGROUND_WHITE | FOREGROUND_INTENSITY)

    @classmethod
    def yellow_foreground_black_background(cls):
        cls.set_color(color=FOREGROUND_YELLOW)

    @classmethod
    def red_foreground_black_background(cls):
        cls.set_color(color=FOREGROUND_RED)

    @classmethod
    def red_bright_foreground_black_background(cls):
        cls.set_color(color=FOREGROUND_RED | FOREGROUND_INTENSITY)