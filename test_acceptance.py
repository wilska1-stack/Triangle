"""Acceptance test for the stained-glass studio.

Customer requirement: customers enter three side lengths and are told the
shape and whether it is buildable. Invalid input shows a message instead of
crashing. Right-angle pieces are flagged, since they need reinforced corners.
The answer must be correct every time, because a wrong answer ruins a pane.

Acceptance criteria (each is a measurable condition):

  AC1. For every integer side triple with a side <= 0 or a failed triangle
       inequality, classify_triangle returns "Invalid" and raises nothing.
       Checked over every integer triple from -1 to 20 (9,261 triples).

  AC2. For every integer side triple from 1 to 20 that is a valid triangle,
       the result matches an exact integer-arithmetic reference on both the
       shape (Equilateral / Isosceles / Scalene) and the right-angle flag
       (a^2 + b^2 == c^2 exactly). Zero mismatches allowed.

  AC3. A right-angle piece with non-integer sides is flagged "Right ...".
       Legs 5 and 5 with hypotenuse 5*sqrt(2) and legs 1 and 1 with
       hypotenuse sqrt(2) must both be flagged. A piece that is off the
       right angle by more than the tolerance (3, 4, 5.001) must not be.
"""

import math
from itertools import product

from triangle import classify_triangle


def reference(a, b, c):
    """Exact integer reference for AC1 and AC2. Independent of the float tolerance."""
    if min(a, b, c) <= 0 or a + b <= c or a + c <= b or b + c <= a:
        return "Invalid"
    if a == b == c:
        return "Equilateral"
    x, y, z = sorted((a, b, c))
    shape = "Isosceles" if len({a, b, c}) < 3 else "Scalene"
    if x * x + y * y == z * z:
        return f"Right {shape}"
    return shape


def test_studio_acceptance_criteria():
    # AC1: invalid input is reported as "Invalid" and never raises.
    for a, b, c in product(range(-1, 21), repeat=3):
        if reference(a, b, c) != "Invalid":
            continue
        result = classify_triangle(a, b, c)
        assert result == "Invalid", f"AC1 failed for {(a, b, c)}: got {result!r}"

    # AC2: every valid integer triple matches the exact reference, zero mismatches.
    mismatches = []
    for a, b, c in product(range(1, 21), repeat=3):
        expected = reference(a, b, c)
        if expected == "Invalid":
            continue
        got = classify_triangle(a, b, c)
        if got != expected:
            mismatches.append(((a, b, c), expected, got))
    assert not mismatches, f"AC2 mismatches (first 5): {mismatches[:5]}"

    # AC3: right-angle pieces with non-integer sides are flagged.
    assert classify_triangle(5, 5, 5 * math.sqrt(2)) == "Right Isosceles"
    assert classify_triangle(1, 1, math.sqrt(2)) == "Right Isosceles"
    # AC3: a piece well outside the tolerance is not flagged as right.
    assert classify_triangle(3, 4, 5.001) == "Scalene"
