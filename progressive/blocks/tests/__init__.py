from __future__ import division

import unittest

from progressive.blocks import bar, indent, percentage, title


class TestBlocks(unittest.TestCase):

    def test__indent(self):
        block = indent.Indent(length=4, character=" ")
        self.assertEqual(block.len, 4)
        self.assertEqual(block.view, "     ")

    def test__percentage(self):
        block = percentage.Percentage(1/2)
        self.assertEqual(block.view, "50%")
        self.assertEqual(block.len, 3)

    def test__fraction(self):
        block = percentage.Fraction(1, 2)
        self.assertEqual(block.view, "1/2")
        self.assertEqual(block.len, 3)

    def test__title(self):
        _ = "I am title"
        block = title.Title(_)
        self.assertEqual(block.len, 10)
        self.assertEqual(block.view, _)

    def test__title__custom_length(self):
        _ = "I am title"
        block = title.Title(_, 9)
        self.assertEqual(block.len, 9)
        self.assertEqual(block.view, _)

    def test_bar(self):
        pass
