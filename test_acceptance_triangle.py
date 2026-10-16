import unittest

from triangle import classify_triangle


class TestCustomerAcceptance(unittest.TestCase):
    """Acceptance test written from the customer's triangle requirements.

    Story: a customer enters three side lengths and expects the classifier
    to return the category their requirements list for those sides.
    """

    def test_customer_sees_correct_classification_for_each_requirement(self):
        # (sides, expected result, requirement it covers)
        scenarios = [
            ((0, 3, 4), "Invalid", "any side <= 0 is invalid"),
            ((-2, 3, 4), "Invalid", "any side <= 0 is invalid"),
            ((1, 2, 3), "Invalid", "sum of two sides equal to the third is invalid"),
            ((1, 2, 10), "Invalid", "triangle inequality failure is invalid"),
            ((5, 5, 5), "Equilateral", "all sides equal"),
            ((5, 5, 7), "Isosceles", "exactly two sides equal"),
            ((2, 3, 4), "Scalene", "all sides different"),
            ((3, 4, 5), "Right Scalene", "Pythagorean theorem gives a Right prefix"),
            ((5, 5, 5 * 2 ** 0.5), "Right Isosceles", "right isosceles uses the Right prefix"),
        ]

        for sides, expected, requirement in scenarios:
            with self.subTest(sides=sides, requirement=requirement):
                self.assertEqual(classify_triangle(*sides), expected)


if __name__ == "__main__":
    unittest.main()
