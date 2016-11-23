#!/usr/bin/env python2
import os
import sys
import copy
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), '../'))

from drpython import board
from drpython.board import Board
from drpython.block import Color
from drpython.exceptions import *
from drpython.utils import Pos


class BoardTest(unittest.TestCase):
    def setUp(self):
        self.board = Board()

    def assertPosEqual(self, a, b):
        self.assertTrue(a == b)

    def test_init_board_size(self):
        self.assertEqual(len(self.board._board), board.HEIGHT)

        for row in self.board._board:
            self.assertEqual(len(row), board.WIDTH)

    def test_init_brick_none(self):
        self.assertIsNone(self.board._brick)

    def test_spawn_brick_position(self):
        self.board.spawn_brick()

        self.assertEqual(len(self.board.brick.blocks), 2)

        block_a, block_b = self.board.brick.blocks

        self.assertPosEqual(block_a.pos, board.SPAWN_POS)
        self.assertPosEqual(block_b.pos, board.SPAWN_POS + Pos(1, 0))

    def test_spawn_brick_occupied(self):
        self.board.spawn_brick()

        with self.assertRaises(PositionOccupied):
            self.board.spawn_brick()

    def test_block(self):
        block = self.board.block(0, 0)

        self.assertIsNotNone(block)
        self.assertPosEqual(block.pos, Pos(0, 0))

        # Should return the same instance
        block_2 = self.board.block(0, 0)
        self.assertIs(block, block_2)

        with self.assertRaises(BottomReached):
            _ = self.board.block(0, board.HEIGHT + 1)

        with self.assertRaises(OutOfBoard):
            _ = self.board.block(999, 0)

        with self.assertRaises(OutOfBoard):
            _ = self.board.block(-1, 0)

    def test_move_brick_invalid(self):
        self.board.spawn_brick()

        with self.assertRaises(InvalidParameter):
            self.board.move_brick('up')

    def test_move_brick_down(self):
        self.board.spawn_brick()

        brick = self.board.brick
        blocks = copy.deepcopy(brick.blocks)

        self.board.move_brick('down')

        for i in range(0, 2):
            self.assertPosEqual(brick.blocks[i].pos, blocks[i].pos + Pos(0, 1))
            self.assertEqual(brick.blocks[i].color, blocks[i].color)

    def test_move_brick_left(self):
        self.board.spawn_brick()

        brick = self.board.brick
        blocks = copy.deepcopy(brick.blocks)

        self.board.move_brick('left')

        for i in range(0, 2):
            self.assertEqual(brick.blocks[i].x, blocks[i].x - 1)
            self.assertEqual(brick.blocks[i].y, blocks[i].y)
            self.assertEqual(brick.blocks[i].color, blocks[i].color)

    def test_move_brick_right(self):
        self.board.spawn_brick()

        brick = self.board.brick
        blocks = copy.deepcopy(brick.blocks)

        self.board.move_brick('right')

        colors = [o.color for o in blocks]
        for i in range(0, 2):
            self.assertEqual(brick.blocks[i].x, blocks[i].x + 1)
            self.assertEqual(brick.blocks[i].y, blocks[i].y)
            self.assertEqual(brick.blocks[i].color, colors[i])

    def test_rotate_brick_to_vertical(self):
        self.board.spawn_brick()
        # Ensure there is enough space
        self.board.move_brick('down')

        origin = self.board.brick.blocks
        colors = [o.color for o in origin]

        self.board.rotate_brick()
        brick = self.board.brick

        self.assertFalse(brick.is_horizontal())
        self.assertPosEqual(brick.blocks[0].pos, origin[0].pos)
        self.assertPosEqual(brick.blocks[1].pos, origin[1].pos + Pos(-1, -1))

        for i in range(0, 2):
            self.assertEqual(brick.blocks[i].color, colors[i])

    def test_rotate_brick_to_vertical_obstacle(self):
        self.board.spawn_brick()

        origin = self.board.brick.blocks
        colors = [o.color for o in origin]

        self.board.rotate_brick()
        brick = self.board.brick

        self.assertFalse(brick.is_horizontal())
        self.assertPosEqual(brick.blocks[0].pos, origin[0].pos + Pos(0, 1))
        self.assertPosEqual(brick.blocks[1].pos, origin[1].pos + Pos(-1, 0))

        for i in range(0, 2):
            self.assertEqual(brick.blocks[i].color, colors[i])

    def test_rotate_brick_to_horizontal(self):
        self.board.spawn_brick()
        # Ensure there is enough space
        self.board.move_brick('down')
        # Set up origin vertical position
        self.board.rotate_brick()

        origin = self.board.brick.blocks
        colors = [o.color for o in origin]
        colors.reverse()

        self.board.rotate_brick()
        brick = self.board.brick

        self.assertTrue(brick.is_horizontal())
        self.assertPosEqual(brick.blocks[0].pos, origin[1].pos + Pos(0, 1))
        self.assertPosEqual(brick.blocks[1].pos, origin[0].pos + Pos(1, 0))

        for i in range(0, 2):
            self.assertEqual(brick.blocks[i].color, colors[i])

    def test_rotate_brick_to_horizontal_obstacle(self):
        self.board.spawn_brick()
        # Ensure there is enough space
        self.board.move_brick('down')
        # Set up origin vertical position
        self.board.rotate_brick()

        # Place obstacle
        b = self.board.brick.blocks[0]
        self.board.block(b.x + 1, b.y).set_color(Color.RED)

        origin = self.board.brick.blocks
        colors = [o.color for o in origin]
        colors.reverse()

        self.board.rotate_brick()
        brick = self.board.brick

        self.assertTrue(brick.is_horizontal())
        self.assertPosEqual(brick.blocks[0].pos, origin[1].pos + Pos(-1, 1))
        self.assertPosEqual(brick.blocks[1].pos, origin[0].pos)

        for i in range(0, 2):
            self.assertEqual(brick.blocks[i].color, colors[i])

    def test_get_falling_blocks(self):
        blocks = self.board.get_falling_blocks()
        self.assertListEqual(blocks, [])

        self.board.block(0, 0).set_falling(True)
        blocks = self.board.get_falling_blocks()
        self.assertListEqual(blocks, [self.board.block(0, 0)])


if __name__ == '__main__':
    unittest.main()
