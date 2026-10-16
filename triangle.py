"""Triangle classifier.

classify_triangle returns one of:
    "Invalid", "Equilateral", "Isosceles", "Scalene",
    or any of the last three prefixed with "Right " when the triangle is right-angled.
"""

import math

# Relative tolerance for the Pythagorean check, so floating-point error
# (e.g. sides like 0.1, 0.2, sqrt(0.05)) does not cause a false negative.
RIGHT_ANGLE_REL_TOL = 1e-9


def is_valid_triangle(a, b, c) -> bool:
    """Return True if a, b, c can form a non-degenerate triangle."""
    if a <= 0 or b <= 0 or c <= 0:
        return False
    # Strict inequality: a + b == c is degenerate (a flat line), so it is invalid.
    return a + b > c and a + c > b and b + c > a


def is_right_triangle(a, b, c) -> bool:
    """Return True if the sides satisfy a^2 + b^2 = c^2 within a tolerance.

    Assumes the sides form a valid triangle.
    """
    x, y, z = sorted((a, b, c))
    return math.isclose(x * x + y * y, z * z, rel_tol=RIGHT_ANGLE_REL_TOL)


def classify_triangle(a, b, c) -> str:
    """Classify a triangle by its sides, e.g. "Right Isosceles" or "Scalene"."""
    if not is_valid_triangle(a, b, c):
        return "Invalid"

    if a == b == c:
        # An equilateral triangle is never right-angled (a^2 + a^2 != a^2),
        # so no "Right " prefix is needed here.
        return "Equilateral"

    if a == b or b == c or a == c:
        kind = "Isosceles"
    else:
        kind = "Scalene"

    if is_right_triangle(a, b, c):
        return f"Right {kind}"
    return kind
