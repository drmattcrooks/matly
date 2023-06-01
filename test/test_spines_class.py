from unittest.mock import Mock

from matly.spines_class import SpineClass

COLOR = Mock()
LABEL = Mock()
IS_VISIBLE = Mock()


def test_spine_class_attributes_defaults():
    spine = SpineClass(LABEL, IS_VISIBLE, COLOR)
    assert 'spine_type' in dir(spine)
    assert 'edgecolor' in dir(spine)
    assert 'visible' in dir(spine)
    assert spine.spine_type == LABEL
    assert spine.edgecolor == COLOR
    assert spine.visible == IS_VISIBLE


def test_set_visible():
    spine = SpineClass(LABEL, IS_VISIBLE, COLOR)
    spine.set_visible(IS_VISIBLE)
    assert spine.visible == IS_VISIBLE


def test_get_visible():
    spine = SpineClass(LABEL, IS_VISIBLE, COLOR)
    spine.is_visible = IS_VISIBLE
    assert spine.get_visible() == spine.visible


def test_set_color():
    spine = SpineClass(LABEL, IS_VISIBLE, COLOR)
    spine.set_color(COLOR)
    assert spine.edgecolor == COLOR


def test_get_color():
    spine = SpineClass(LABEL, IS_VISIBLE, COLOR)
    spine.edgecolor = COLOR
    assert spine.get_color() == spine.edgecolor


def test_set_edgecolor():
    spine = SpineClass(LABEL, IS_VISIBLE, COLOR)
    spine.set_edgecolor(COLOR)
    assert spine.edgecolor == COLOR


def test_get_edgecolor():
    spine = SpineClass(LABEL, IS_VISIBLE, COLOR)
    spine.edgecolor = COLOR
    assert spine.get_edgecolor() == spine.edgecolor