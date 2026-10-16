import unittest

from triangle import classify_triangle, is_valid_triangle


class TestIsValidTriangle(unittest.TestCase):
    def test_valid_triangle(self):
        self.assertTrue(is_valid_triangle(3, 4, 5))

    def test_equilateral_is_valid(self):
        self.assertTrue(is_valid_triangle(2, 2, 2))

    def test_zero_side_is_invalid(self):
        self.assertFalse(is_valid_triangle(0, 3, 3))

    def test_negative_side_is_invalid(self):
        self.assertFalse(is_valid_triangle(-1, 2, 2))

    def test_triangle_inequality_fails(self):
        self.assertFalse(is_valid_triangle(1, 2, 5))

    def test_degenerate_sum_equals_third_side_is_invalid(self):
        self.assertFalse(is_valid_triangle(1, 2, 3))

    def test_degenerate_in_any_position(self):
        self.assertFalse(is_valid_triangle(3, 1, 2))
        self.assertFalse(is_valid_triangle(1, 3, 2))


class TestClassifyTriangle(unittest.TestCase):
    def test_invalid_triangles(self):
        self.assertEqual(classify_triangle(1, 2, 3), "Invalid")
        self.assertEqual(classify_triangle(0, 3, 3), "Invalid")
        self.assertEqual(classify_triangle(-1, 2, 2), "Invalid")
        self.assertEqual(classify_triangle(1, 2, 10), "Invalid")

    def test_equilateral(self):
        self.assertEqual(classify_triangle(5, 5, 5), "Equilateral")

    def test_isosceles_all_positions(self):
        self.assertEqual(classify_triangle(5, 5, 7), "Isosceles")
        self.assertEqual(classify_triangle(5, 7, 5), "Isosceles")
        self.assertEqual(classify_triangle(7, 5, 5), "Isosceles")

    def test_scalene(self):
        self.assertEqual(classify_triangle(2, 3, 4), "Scalene")

    def test_right_scalene(self):
        self.assertEqual(classify_triangle(3, 4, 5), "Right Scalene")
        self.assertEqual(classify_triangle(5, 12, 13), "Right Scalene")

    def test_right_scalene_hypotenuse_not_last(self):
        self.assertEqual(classify_triangle(5, 3, 4), "Right Scalene")
        self.assertEqual(classify_triangle(13, 5, 12), "Right Scalene")

    def test_right_isosceles(self):
        self.assertEqual(classify_triangle(1, 1, 2 ** 0.5), "Right Isosceles")

    def test_isosceles_not_right(self):
        self.assertEqual(classify_triangle(5, 5, 7), "Isosceles")

    def test_equilateral_is_never_right(self):
        for side in (1, 2, 5, 100, 0.001):
            self.assertEqual(classify_triangle(side, side, side), "Equilateral")

    def test_right_check_uses_tolerance(self):
        # 0.3 + 0.4 vs 0.5 is a right triangle, but 0.1 + 0.2 is not exactly 0.3 in floats
        self.assertEqual(classify_triangle(0.1 + 0.2, 0.4, 0.5), "Right Scalene")

    def test_near_right_outside_tolerance_is_not_right(self):
        self.assertEqual(classify_triangle(3, 4, 5.001), "Scalene")


if __name__ == "__main__":
    unittest.main()
