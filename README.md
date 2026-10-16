# Triangle Classifier

## Project Description

This project is a triangle classifier written in Python for my Software Engineering assignment. The program takes three side lengths and checks whether they form a valid triangle. If the triangle is valid, it determines whether it is equilateral, isosceles, or scalene. It also checks whether the triangle has a right angle.

The purpose of this project is to practice Python programming, unit testing, boundary testing, and reviewing AI-generated suggestions.

## Files in the Project

- `triangle.py`: Contains the functions used to validate and classify triangles.
- `test_triangle.py`: Contains unit tests for triangle classification and boundary cases (28 test cases).
- `test_acceptance.py`: Contains an acceptance test based on the customer's requirements (1 test case).
- `requirements.txt`: Contains the pytest dependency (`pytest==9.1.1`).
- `README.md`: Explains the project, testing process, and AI usage.

## How to Run the Tests

Install pytest:

```bash
python3 -m pip install -r requirements.txt
```

Run the tests:

```bash
python3 -m pytest -v
```

## Test Results

All 29 tests pass: 28 unit tests in `test_triangle.py` and 1 acceptance test in `test_acceptance.py`. The tests were run locally with pytest 9.1.1.

## Equivalence Classes and Boundary Cases

I identified different types of inputs to check whether the program correctly classifies triangles and handles invalid values.

| Equivalence Class | Example | Expected Result |
|---|---|---|
| Zero side length | `(0, 3, 3)` | Invalid |
| Negative side length | `(-1, 2, 2)` | Invalid |
| Triangle inequality fails | `(1, 2, 10)` | Invalid |
| Degenerate triangle | `(1, 2, 3)`, `(3, 1, 2)`, `(1, 3, 2)` | Invalid |
| Nearly degenerate valid triangle | `(1, 2, 2.999)` | Scalene |
| Equilateral triangle | `(5, 5, 5)`, `(0.001, 0.001, 0.001)` | Equilateral |
| Isosceles triangle | `(5, 5, 7)` | Isosceles |
| Scalene triangle | `(2, 3, 4)` | Scalene |
| Right scalene triangle | `(3, 4, 5)`, `(5, 3, 4)`, `(13, 5, 12)` | Right Scalene |
| Right isosceles, non-integer sides | `(5, 5, 5√2)`, `(1, 1, √2)` | Right Isosceles |
| Near-right, outside tolerance | `(3, 4, 5.001)` | Scalene |

## Boundary Testing

One important boundary is when the sum of two sides equals the third side. For example, sides 1, 2, and 3 cannot form a valid triangle because 1 + 2 = 3. The test checks this in every position the degenerate side can take.

I also tested zero and negative side lengths, because a triangle must have three positive sides. The nearly degenerate case `(1, 2, 2.999)` checks that a very flat but valid triangle is still classified correctly.

## Triangle Classification

The program uses two functions.

**`is_valid_triangle()`** checks whether the side lengths are positive and satisfy the triangle inequality. If they don't form a valid triangle, it returns `False`.

**`classify_triangle()`** identifies the triangle type:

- **Equilateral:** all three sides are equal.
- **Isosceles:** exactly two sides are equal.
- **Scalene:** all three sides are different.
- **Right Isosceles / Right Scalene:** the Pythagorean check passes, with the `"Right "` prefix.
- **Invalid:** the sides do not form a triangle.

The right-angle check sorts the sides and compares the two shorter sides' squares with the longest side's square using `math.isclose` with a relative tolerance of `1e-9`, not `==`.

## Why an Equilateral Triangle Cannot Be a Right Triangle

In a right triangle, the Pythagorean theorem requires `a² + b² = c²`, where `c` is the hypotenuse. An equilateral triangle has `a = b = c`, so the condition becomes `a² + a² = a²`, which reduces to `a² = 0`. That is impossible for a side with positive length. The code returns `"Equilateral"` for these inputs and never adds the `"Right "` prefix.

## Claude Review Log

For this assignment, I used Claude (an AI assistant) to draft the tests and to review them. I checked each one against the spec table, not against what the code returned.

| Test | Claude-Suggested? | Decision | Explanation |
|---|---|---|---|
| `test_right_triangle_with_non_integer_sides` | Yes | Kept | Uses `5 * math.sqrt(2)`. I checked it by mutation: replacing the tolerance in `triangle.py` with exact `==` makes this test and `test_right_isosceles_with_unit_legs` fail. |
| `test_is_valid_rejects_triangle_inequality_failure` (duplicate name) | Yes | Edited | Two tests in the file had the same name, so pytest would silently run only one. A duplicate-name check caught it. I renamed the `is_valid_triangle` test. |
| Spot check `(0.1 + 0.2, 0.4, 0.5)` | Yes | Edited | Claude's first expectation was `Invalid`. That was wrong: 0.3 + 0.4 > 0.5, so it is valid, and 0.09 + 0.16 = 0.25, so it is exactly right. I corrected the expectation to `Right Scalene`. |
| `test_equilateral_is_never_labelled_right` | Yes | Kept | Checks that equilateral triangles of several sizes, including 0.001, return `"Equilateral"` and never a right-angle label. |
| `test_just_under_degenerate_is_valid` | Yes | Kept | Checks the boundary just inside the degenerate case: `(1, 2, 2.999)` is valid. |

## Acceptance Criteria (Stained-Glass Studio)

The customer requirement: customers enter three side lengths and are told the shape and whether it is buildable. Invalid input must show a message instead of crashing. Right-angle pieces must be flagged, because they need reinforced corners. The answer must be correct every time.

- **AC1: Invalid is reported, never raised.** For every integer triple from -1 to 20 that is not a valid triangle, `classify_triangle` returns `"Invalid"` and raises no exception.
- **AC2: Zero mismatches on valid triangles.** For every integer triple from 1 to 20 that is a valid triangle, the shape and right-angle flag match an exact integer-arithmetic reference (`a² + b² == c²`, with no floats). The number of mismatches must be 0.
- **AC3: Non-integer right angles are flagged.** `(5, 5, 5√2)` and `(1, 1, √2)` return `"Right Isosceles"`. `(3, 4, 5.001)` does not return a `"Right "` result.

## Acceptance Testing

`test_acceptance.py` contains one test that calls `classify_triangle()` end to end and checks AC1, AC2, and AC3. The reference used for AC2 is written with exact integer arithmetic so it doesn't depend on the tolerance being tested.

**Known gap:** AC1 covers numeric input only. Non-numeric values such as `"a"` or `None` currently raise `TypeError` instead of returning `"Invalid"`. This needs a decision before the studio can use free-text input.

## AI-Use Disclosure

- **Tool:** Claude (Anthropic), via Claude Code.
- **Used for:** drafting `triangle.py`, the unit tests, the acceptance test and its criteria, and this README.
- **Verified by:** running `pytest` (28 unit tests and 1 acceptance test, all passing); a duplicate-test-name check; a mutation test that swaps the tolerance for exact `==`; checking the acceptance reference logic by hand against the spec table; and probing non-numeric inputs to find the `TypeError` gap.
- No other AI tool was used.

## Conclusion

This project helped me understand how triangle classification works and why software testing matters. I learned how to identify valid and invalid triangles, check boundary cases, and test different kinds of inputs. I also learned that AI-drafted tests can contain mistakes, such as a wrong expected value and a duplicated test name, so every test has to be checked against the spec, not accepted automatically.
