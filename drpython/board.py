"""Game board class."""

import random

import pygame
import drpython.block
import drpython.brick
from drpython.exception import InvalidParameter
from drpython.block import Block
from drpython.block import Color
from drpython.brick import Brick
from drpython.colors import *

WIDTH = 8
HEIGHT = 16

WIDTH_PIXELS = WIDTH * drpython.block.WIDTH
HEIGHT_PIXELS = HEIGHT * drpython.block.HEIGHT

SPAWN_POINT = (3, 0)

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
        # TODO check if the spot is empty

        colors = (
            random.randint(1,3),
            random.randint(1,3),
        )

        blocks = (
            self._board[SPAWN_POINT[1]][SPAWN_POINT[0]],
            self._board[SPAWN_POINT[1]][SPAWN_POINT[0]+1],
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

        new_a = self.board[a.y+y][a.x+x]
        new_b = self.board[b.y+y][b.x+x]

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
                self._render_block(self._display, self._board[h][w])

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

    @property
    def board(self):
        return self._board

    @property
    def brick(self):
        return self._brick

    @property
    def display(self):
        return self._display
