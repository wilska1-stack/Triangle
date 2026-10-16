import math

import pytest

from triangle import classify_triangle, is_valid_triangle


# --- is_valid_triangle ---------------------------------------------------

@pytest.mark.parametrize("sides", [(3, 4, 5), (2, 2, 2), (5, 5, 7)])
def test_valid_triangles_are_valid(sides):
    assert is_valid_triangle(*sides)


@pytest.mark.parametrize("sides", [(0, 3, 3), (3, 0, 3), (3, 3, 0), (-1, 2, 2)])
def test_side_zero_or_negative_is_invalid(sides):
    assert not is_valid_triangle(*sides)


def test_is_valid_rejects_triangle_inequality_failure():
    assert not is_valid_triangle(1, 2, 10)


# --- classify_triangle: one test per row of the spec table ---------------

def test_any_side_zero_or_negative_is_invalid():
    assert classify_triangle(0, 3, 4) == "Invalid"
    assert classify_triangle(-2, 3, 4) == "Invalid"


def test_triangle_inequality_failure_is_invalid():
    assert classify_triangle(1, 2, 10) == "Invalid"


def test_all_sides_equal_is_equilateral():
    assert classify_triangle(5, 5, 5) == "Equilateral"


def test_exactly_two_sides_equal_is_isosceles():
    assert classify_triangle(5, 5, 7) == "Isosceles"


def test_all_sides_different_is_scalene():
    assert classify_triangle(2, 3, 4) == "Scalene"


def test_pythagorean_triple_is_right_scalene():
    assert classify_triangle(3, 4, 5) == "Right Scalene"


def test_right_triangle_with_non_integer_sides():
    # Legs 5 and 5, hypotenuse 5*sqrt(2). math.sqrt is not exact, so a
    # strict == check on the Pythagorean sum would wrongly say "Isosceles".
    assert classify_triangle(5, 5, 5 * math.sqrt(2)) == "Right Isosceles"


def test_right_isosceles_with_unit_legs():
    assert classify_triangle(1, 1, math.sqrt(2)) == "Right Isosceles"


def test_right_check_does_not_depend_on_side_order():
    assert classify_triangle(5, 3, 4) == "Right Scalene"
    assert classify_triangle(13, 5, 12) == "Right Scalene"


# --- boundaries ----------------------------------------------------------

def test_degenerate_sum_equal_to_third_side_is_invalid():
    # 1 + 2 == 3: flat line, not a triangle.
    assert classify_triangle(1, 2, 3) == "Invalid"


@pytest.mark.parametrize("sides", [(1, 2, 3), (3, 1, 2), (1, 3, 2)])
def test_degenerate_is_invalid_in_any_position(sides):
    assert classify_triangle(*sides) == "Invalid"


def test_just_under_degenerate_is_valid():
    # 1 + 2 = 3 is degenerate; 1 + 2 > 2.999 is a valid, very flat triangle.
    assert classify_triangle(1, 2, 2.999) == "Scalene"


# --- equilateral is never right ------------------------------------------

@pytest.mark.parametrize("side", [0.001, 1, 2, 5, 100])
def test_equilateral_is_never_labelled_right(side):
    assert classify_triangle(side, side, side) == "Equilateral"


# --- tolerance -----------------------------------------------------------

def test_near_right_outside_tolerance_is_not_right():
    assert classify_triangle(3, 4, 5.001) == "Scalene"
