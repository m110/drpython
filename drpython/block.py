from drpython.exceptions import *
from drpython.utils import Pos

WIDTH = 20
HEIGHT = 14


class Color(object):
    CLEAR = 0
    BLUE = 1
    RED = 2
    YELLOW = 3


class Block(object):

    def __init__(self, x, y, color=None):
        self._x = x
        self._y = y
        self._color = Color.CLEAR
        self._falling = False
        if color:
            self.set_color(color)

    def set_color(self, color):
        if self._color != Color.CLEAR:
            raise InvalidOperation("Trying to set color on colored block")

        if color != Color.BLUE and color != Color.RED and color != Color.YELLOW:
            raise InvalidParameter("Invalid color value: {}".format(color))

        self._color = color

    def clear(self):
        if self._color == Color.CLEAR:
            raise InvalidOperation("Trying to clear block without color")

        self._color = Color.CLEAR

    def set_falling(self, falling):
        falling = bool(falling)

        if falling == self._falling:
            raise InvalidOperation("Falling already set to {}".format(falling))

        self._falling = falling

    def __repr__(self):
        return 'Block ({}, {}) color: {} falling: {}'.format(self.x, self.y, self.color, self._falling)

    def is_clear(self):
        return self.color == Color.CLEAR

    def is_falling(self):
        return self._falling

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def x_pixels(self):
        return self.x * WIDTH

    @property
    def y_pixels(self):
        return self.y * HEIGHT

    @property
    def pos(self):
        return Pos(self.x, self.y)

    @property
    def color(self):
        return self._color
