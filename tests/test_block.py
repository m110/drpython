#!/usr/bin/env python2
import os
import sys
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), '../'))

from drpython.block import Block, Color
from drpython.exceptions import InvalidOperation, InvalidParameter


class BlockTest(unittest.TestCase):

    def test_init(self):
        block = Block(1, 2)

        self.assertEqual(block.color, Color.CLEAR)
        self.assertEqual(block.x, 1)
        self.assertEqual(block.y, 2)
        self.assertTrue(block.is_clear())

        block = Block(0, 0, Color.RED)
        self.assertEqual(block.color, Color.RED)
        self.assertFalse(block.is_clear())

    def test_set_color(self):
        block = Block(0, 0)
        self.assertEqual(block.color, Color.CLEAR)
        self.assertTrue(block.is_clear())

        block.set_color(Color.RED)
        self.assertEqual(block.color, Color.RED)
        self.assertFalse(block.is_clear())

    def test_clear(self):
        block = Block(0, 0, Color.RED)
        self.assertEqual(block.color, Color.RED)
        self.assertFalse(block.is_clear())

        block.clear()
        self.assertEqual(block.color, Color.CLEAR)
        self.assertTrue(block.is_clear())

    def test_raise_exception_on_clear_if_no_color(self):
        block = Block(0, 0)

        with self.assertRaises(InvalidOperation):
            block.clear()

    def test_raise_exception_on_set_color_if_not_clear(self):
        block = Block(0, 0, Color.RED)

        with self.assertRaises(InvalidOperation):
            block.set_color(Color.BLUE)

    def test_raise_exception_on_set_color_if_invalid_color(self):
        block = Block(0, 0)

        with self.assertRaises(InvalidParameter):
            block.set_color(99999)

    def test_set_falling(self):
        block = Block(0, 0)
        self.assertFalse(block.is_falling())

        block.set_falling(True)
        self.assertTrue(block.is_falling())

        block.set_falling(False)
        self.assertFalse(block.is_falling())

    def test_set_falling_raises_exception_on_double_set(self):
        block = Block(0, 0)

        with self.assertRaises(InvalidOperation):
            block.set_falling(False)

        block.set_falling(True)
        with self.assertRaises(InvalidOperation):
            block.set_falling(True)


if __name__ == '__main__':
    unittest.main()
