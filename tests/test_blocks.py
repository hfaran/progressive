from __future__ import division

from progressive.blocks import bar, indent, percentage, title


def test__indent():
    block = indent.Indent(length=4, character=" ")
    assert block.len == 4
    assert block.view == "    "


def test__percentage():
    block = percentage.Percentage(1/2)
    assert block.view == " 50%"
    assert block.len == 4


def test__fraction():
    block = percentage.Fraction(1, 2)
    assert block.view == "1/2"
    assert block.len == 3


def test__title():
    _ = "I am title"
    block = title.Title(_)
    assert block.len == 10
    assert block.view == _


def test__title__custom_length():
    _ = "I am title"
    block = title.Title(_, 9)
    assert block.len == 9
    assert block.view == _


def test_bar():
    pass
