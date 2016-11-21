#!/usr/bin/env python2
import os
import sys
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), '../'))

from drpython.utils import Pos


class PosTest(unittest.TestCase):

    def test_pos_init(self):
        pos = Pos(1, 2)
        self.assertEqual(pos.x, 1)
        self.assertEqual(pos.y, 2)

        pos = Pos(x=42, y=100)
        self.assertEqual(pos.x, 42)
        self.assertEqual(pos.y, 100)

    def test_pos_equal(self):
        pos_a = Pos(100, 200)
        pos_b = Pos(100, 200)

        self.assertTrue(pos_a == pos_b)

        with self.assertRaises(TypeError):
            _ = pos_a == {}

    def test_pos_not_equal(self):
        pos_a = Pos(100, 200)
        pos_b = Pos(1, 2)

        self.assertFalse(pos_a == pos_b)

    def test_pos_equal_tuple(self):
        pos = Pos(100, 200)
        pos_tuple = (100, 200)
        pos_list = [100, 200]

        self.assertTrue(pos == pos_tuple)
        self.assertTrue(pos == pos_list)

    def test_pos_not_equal_tuple(self):
        pos = Pos(100, 200)
        pos_tuple = (1, 2)
        pos_list = [3, 4]

        self.assertFalse(pos == pos_tuple)
        self.assertFalse(pos == pos_list)

    def test_pos_add(self):
        pos_a = Pos(100, 200)
        pos_b = Pos(5, 10)

        pos = pos_a + pos_b
        self.assertEqual(pos.x, 105)
        self.assertEqual(pos.y, 210)

        pos = pos_b + pos_a
        self.assertEqual(pos.x, 105)
        self.assertEqual(pos.y, 210)

        pos = pos_a
        pos += pos_b
        self.assertEqual(pos.x, 105)
        self.assertEqual(pos.y, 210)


    def test_pos_tuple(self):
        pos_a = Pos(100, 200)
        pos_tuple = (5, 10)

        pos = pos_a + pos_tuple
        self.assertEqual(pos.x, 105)
        self.assertEqual(pos.y, 210)

        pos = pos_a
        pos += pos_tuple
        self.assertEqual(pos.x, 105)
        self.assertEqual(pos.y, 210)


if __name__ == '__main__':
    unittest.main()
