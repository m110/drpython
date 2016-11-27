"""Game board class."""
import pygame
import random

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
            random.randint(1, 3),
            random.randint(1, 3),
        )

        for i in (0, 1):
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
        except (OutOfBoard, BottomReached):
            raise

        if (new_a != b and not new_a.is_clear()) or (new_b != a and not new_b.is_clear()):
            raise PositionOccupied("Collision occurred")

        a_color = a.color
        b_color = b.color

        a.clear()
        b.clear()

        new_a.set_color(a_color)
        new_b.set_color(b_color)

        self.brick.set_blocks(new_a, new_b)

    def rotate_brick(self):
        transform = (
            # vertical to horizontal
            ((Pos(1, 0), Pos(0, 1)),
             (Pos(0, 0), Pos(-1, 1))),
            # horizontal to vertical
            ((Pos(0, 0), Pos(-1, -1)),
             (Pos(0, 1), Pos(-1, 0)))
        )

        section = int(self.brick.is_horizontal())

        origin = self.brick.blocks

        for offset in transform[section]:
            try:
                i = not section
                j = not i
                new_blocks = (
                    self.block(origin[i].x + offset[i].x, origin[i].y + offset[i].y),
                    self.block(origin[j].x + offset[j].x, origin[j].y + offset[j].y),
                )

                # Don't overwrite blocks
                for b in new_blocks:
                    if not b.is_clear() and b.pos != origin[0].pos and b.pos != origin[1].pos:
                        raise InvalidOperation("New block is occupied")

                if self.brick.is_horizontal():
                    # standard colors
                    colors = (origin[0].color, origin[1].color)
                else:
                    # swap colors
                    colors = (origin[1].color, origin[0].color)

                for k in range(0, 2):
                    origin[k].clear()
                    new_blocks[k].set_color(colors[k])

                self.brick.set_blocks(*new_blocks)
            except (OutOfBoard, InvalidOperation):
                continue
            else:
                break

    def check_match(self, blocks):
        match = False

        for block in blocks:
            if block.is_clear():
                continue

            horizontal = set(self._get_matches_in_direction(block, 1, 0) + self._get_matches_in_direction(block, -1, 0))
            vertical = set(self._get_matches_in_direction(block, 0, 1) + self._get_matches_in_direction(block, 0, -1))

            for matches in (horizontal, vertical):
                if len(matches) >= 3:
                    match = True
                    for next_block in matches:
                        next_block.clear()
                    block.clear()

        return match

    def _get_matches_in_direction(self, block, x_dir, y_dir):
        matches = []

        x = block.x + x_dir
        y = block.y + y_dir

        while True:
            try:
                next_block = self.block(x, y)
            except (OutOfBoard, BottomReached):
                break

            if next_block.is_clear():
                break

            if block.color != next_block.color:
                break

            matches.append(next_block)

            x += x_dir
            y += y_dir

        return matches

    def check_blocks_in_air(self):
        changed = True

        # TODO second brick block should drop if the first block is cleared

        while changed:
            changed = False
            for x in range(0, WIDTH):
                for y in range(0, HEIGHT):
                    block = self.block(x, y)
                    block_changed = self._check_block_in_air(block)
                    if block_changed:
                        changed = True

    def _check_block_in_air(self, block):
        if block.is_clear() or block.is_falling():
            return False

        try:
            bottom_block = self.block(block.x, block.y+1)
        except BottomReached:
            return False

        right_block = None
        left_block = None

        try:
            right_block = self.block(block.x+1, block.y)
        except OutOfBoard:
            pass

        try:
            left_block = self.block(block.x-1, block.y)
        except OutOfBoard:
            pass

        if (bottom_block.is_clear() or bottom_block.is_falling()) and \
                (not right_block or right_block.is_clear()) and \
                (not left_block or left_block.is_clear()):
            block.set_falling(True)
            return True

        return False

    def get_falling_blocks(self):
        return [block for rows in reversed(self._board)
                for block in rows
                if block.is_falling()]

    def handle_falling_blocks(self):
        blocks = self.get_falling_blocks()

        if not blocks:
            return []

        blocks_at_bottom = []

        for block in blocks:
            try:
                bottom_block = self.block(block.x, block.y+1)
            except BottomReached:
                blocks_at_bottom.append(block)
                block.set_falling(False)
                continue

            if bottom_block.is_clear():
                bottom_block.set_color(block.color)
                bottom_block.set_falling(True)
                block.clear()
                block.set_falling(False)
            else:
                blocks_at_bottom.append(block)
                block.set_falling(False)

        return blocks_at_bottom

    def handle_collision(self):
        self.check_match(self._brick.blocks)

        while True:
            self.check_blocks_in_air()

            blocks = []
            while self.get_falling_blocks():
                blocks.extend(self.handle_falling_blocks())

            if not self.check_match(blocks):
                break

        self.spawn_brick()

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
        if x < 0 or y < 0:
            raise OutOfBoard("Trying to get block at negative position")

        if y <= len(self._board)-1:
            if x <= len(self._board[y])-1:
                return self._board[y][x]
            else:
                raise OutOfBoard("Position ({}, {}) not on board".format(x, y))
        else:
            raise BottomReached("Bottom reached by block")

    @property
    def brick(self):
        return self._brick

    @property
    def display(self):
        return self._display
