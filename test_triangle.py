import math

import pytest

from triangle import classify_triangle, is_valid_triangle

# Part 2 skeleton. Each test below is a stub that FAILS on purpose until
# its body is written (with Copilot autocomplete, reviewed against the spec
# table). Do not leave a stub unfilled when you commit.


# --- is_valid_triangle ---------------------------------------------------

def test_valid_triangles_are_valid():
    # Spec: sides > 0 and triangle inequality holds -> True.
    assert is_valid_triangle(3, 4, 5)

def test_side_zero_or_negative_is_invalid():
    # Spec row 1: any side <= 0 -> invalid.
    assert not is_valid_triangle(0, 1, 1)


def test_is_valid_rejects_triangle_inequality_failure():
    # Spec row 1: triangle inequality fails -> invalid.
    assert not is_valid_triangle(1, 1, 3)


# --- classify_triangle: one test per row of the spec table ---------------

def test_any_side_zero_or_negative_is_invalid():
    # Spec row 1: "Invalid" when any side <= 0.
    assert classify_triangle(0, 1, 1) == "Invalid"


def test_triangle_inequality_failure_is_invalid():
    # Spec row 1: "Invalid" when triangle inequality fails.
    assert classify_triangle(1, 1, 3) == "Invalid"



def test_all_sides_equal_is_equilateral():
    # Spec row 2: all sides equal -> "Equilateral".
    assert classify_triangle(2, 2, 2) == "Equilateral"


def test_exactly_two_sides_equal_is_isosceles():
    # Spec row 3: exactly two sides equal -> "Isosceles".
    assert classify_triangle(2, 2, 3) == "Isosceles"


def test_all_sides_different_is_scalene():
    # Spec row 4: all sides different -> "Scalene".
    # Edited: (3, 4, 5) is a right triangle, so it returns "Right Scalene".
    # (2, 3, 4) has all sides different and no right angle.
    assert classify_triangle(2, 3, 4) == "Scalene"


def test_pythagorean_triple_is_right_scalene():
    # Spec row 5: Pythagorean theorem -> "Right " prefix, e.g. "Right Scalene".
    assert classify_triangle(3, 4, 5) == "Right Scalene"


def test_right_triangle_with_non_integer_sides():
    # Spec row 5, tolerance required: legs 5 and 5, hypotenuse 5*sqrt(2).
    # A suggestion that uses == here is wrong by the spec; reject or edit it.
    assert classify_triangle(5, 5, 5 * math.sqrt(2)) == "Right Isosceles"


def test_right_isosceles_with_unit_legs():
    # Spec row 5 with a tolerance-sensitive non-integer hypotenuse.
    assert classify_triangle(1, 1, math.sqrt(2)) == "Right Isosceles"


def test_right_check_does_not_depend_on_side_order():
    # Spec row 5: hypotenuse may be listed first, middle, or last.
    assert classify_triangle(5 * math.sqrt(2), 5, 5) == "Right Isosceles"


# --- boundaries ----------------------------------------------------------

def test_degenerate_sum_equal_to_third_side_is_invalid():
    # Spec row 1 boundary: 1 + 2 == 3 -> "Invalid".
    assert classify_triangle(1, 2, 3) == "Invalid"


def test_degenerate_is_invalid_in_any_position():
    # Spec row 1 boundary, with the degenerate side in each position.
    assert classify_triangle(1, 3, 2) == "Invalid"


def test_just_under_degenerate_is_valid():
    # Spec boundary: 1 + 2 > 2.999 -> valid (Scalene).
    assert classify_triangle(1, 2, 2.999) == "Scalene"


# --- equilateral is never right ------------------------------------------

def test_equilateral_is_never_labelled_right():
    # Spec: an equilateral triangle is never "Right ...".
    assert classify_triangle(1, 1, 1) == "Equilateral"


# --- tolerance -----------------------------------------------------------

def test_near_right_outside_tolerance_is_not_right():
    # Spec row 5: a clearly-not-right triangle must not get the prefix.
    assert classify_triangle(3, 4, 5.001) == "Scalene"
