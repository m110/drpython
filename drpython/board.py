"""Game board class."""

import random

import pygame
import drpython.block
import drpython.brick
from drpython.exceptions import *
from drpython.block import Block
from drpython.block import Color
from drpython.brick import Brick
from drpython.colors import *
from drpython.utils import Pos

WIDTH = 8
HEIGHT = 16

WIDTH_PIXELS = WIDTH * drpython.block.WIDTH
HEIGHT_PIXELS = HEIGHT * drpython.block.HEIGHT

SPAWN_POS = Pos(x=3, y=0)

class Board(object):

    def __init__(self):
        self._display = pygame.Surface((WIDTH_PIXELS, HEIGHT_PIXELS))
        # Init board with clear blocks
        self._board = []
        for h in range(0, HEIGHT):
            self._board.append([])
            for w in range(0, WIDTH):
                self._board[h].append(Block(w, h))

        self._brick = None

    def spawn_brick(self):
        blocks = (
            self.block(SPAWN_POS.x, SPAWN_POS.y),
            self.block(SPAWN_POS.x + 1, SPAWN_POS.y),
        )

        for block in blocks:
            if not block.is_clear():
                # TODO catch this somewhere and end game
                raise PositionOccupied("Block is not clear at spawn point")

        colors = (
            random.randint(1,3),
            random.randint(1,3),
        )

        for i in (0,1):
            blocks[i].set_color(colors[i])

        self._brick = Brick(blocks)

    def move_brick(self, direction):
        a, b = self.brick.blocks

        if direction == 'down':
            y = 1
            x = 0
        elif direction == 'left':
            y = 0
            x = -1
        elif direction == 'right':
            y = 0
            x = 1
        else:
            raise InvalidParameter("Unknown direction: {}".format(direction))

        try:
            new_a = self.block(a.x+x, a.y+y)
            new_b = self.block(b.x+x, b.y+y)
        except OutOfBoard:
            return

        if (new_a != b and not new_a.is_clear()) or \
           (new_b != a and not new_b.is_clear()):
            raise PositionOccupied("Position is occupied by colored block")

        a_color = a.color
        b_color = b.color

        a.clear()
        b.clear()

        new_a.set_color(a_color)
        new_b.set_color(b_color)

        self.brick.set_blocks(new_a, new_b)

    def render(self):
        self.display.fill(BLACK)

        for h in range(0, HEIGHT):
            for w in range(0, WIDTH):
                self._render_block(self._display, self.block(w, h))

        return self.display

    def _render_block(self, display, block):
        if block.color == Color.CLEAR:
            return
        elif block.color == Color.RED:
            color = RED
        elif block.color == Color.BLUE:
            color = BLUE
        elif block.color == Color.YELLOW:
            color = YELLOW
        else:
            raise InvalidParameter("Block has invalid color: {}".format(block.color))

        display.fill(color,
            (block.x_pixels,
            block.y_pixels,
            drpython.block.WIDTH,
            drpython.block.HEIGHT))

    def block(self, x, y):
        if y >= 0 and len(self._board)-1 >= y:
            if x >= 0 and len(self._board[y])-1 >= x:
                return self._board[y][x]

        raise OutOfBoard("Position ({}, {}) not on board".format(x, y))

    @property
    def brick(self):
        return self._brick

    @property
    def display(self):
        return self._display
