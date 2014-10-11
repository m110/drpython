#!/usr/bin/env python2

import copy
import unittest
from drpython import board
from drpython.board import Board
from drpython.block import Color
from drpython.exceptions import *

class BoardTest(unittest.TestCase):
    def setUp(self):
        self.board = Board()

    def test_init_board_size(self):
        self.assertEquals(len(self.board._board), board.HEIGHT)

        for row in self.board._board:
            self.assertEquals(len(row), board.WIDTH)

    def test_init_brick_none(self):
        self.assertIsNone(self.board._brick)

    def test_spawn_brick_position(self):
        self.board.spawn_brick()

        self.assertEqual(len(self.board.brick.blocks), 2)

        block_a, block_b = self.board.brick.blocks

        self.assertEquals(block_a.x, board.SPAWN_POS.x)
        self.assertEquals(block_a.y, board.SPAWN_POS.y)

        self.assertEquals(block_b.x, board.SPAWN_POS.x + 1)
        self.assertEquals(block_b.y, board.SPAWN_POS.y)

    def test_spawn_brick_occupied(self):
        self.board.spawn_brick()

        with self.assertRaises(PositionOccupied):
            self.board.spawn_brick()

    def test_block(self):
        block = self.board.block(0, 0)

        self.assertIsNotNone(block)
        self.assertEqual(block.x, 0)
        self.assertEqual(block.y, 0)

        # Should return the same instance
        block_2 = self.board.block(0, 0)
        self.assertIs(block, block_2)

        with self.assertRaises(OutOfBoard):
            _ = self.board.block(board.WIDTH + 1, board.HEIGHT + 1)

        with self.assertRaises(OutOfBoard):
            _ = self.board.block(-1, -1)

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
            self.assertEquals(brick.blocks[i].x, blocks[i].x)
            self.assertEquals(brick.blocks[i].y, blocks[i].y + 1)
            self.assertEquals(brick.blocks[i].color, blocks[i].color)

    def test_move_brick_left(self):
        self.board.spawn_brick()

        brick = self.board.brick
        blocks = copy.deepcopy(brick.blocks)

        self.board.move_brick('left')

        for i in range(0, 2):
            self.assertEquals(brick.blocks[i].x, blocks[i].x - 1)
            self.assertEquals(brick.blocks[i].y, blocks[i].y)
            self.assertEquals(brick.blocks[i].color, blocks[i].color)

    def test_move_brick_right(self):
        self.board.spawn_brick()

        brick = self.board.brick
        blocks = copy.deepcopy(brick.blocks)

        self.board.move_brick('right')

        for i in range(0, 2):
            self.assertEquals(brick.blocks[i].x, blocks[i].x + 1)
            self.assertEquals(brick.blocks[i].y, blocks[i].y)
            self.assertEquals(brick.blocks[i].color, blocks[i].color)

    def test_move_brick_collision(self):
        self.board.spawn_brick()

        blocks = self.board.brick.blocks

        for b in blocks:
            self.board.block(b.x, b.y + 1).set_color(Color.RED)

        with self.assertRaises(PositionOccupied):
            self.board.move_brick('down')

if __name__ == '__main__':
    unittest.main()
