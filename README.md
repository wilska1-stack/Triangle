# Triangle Classifier

Classifies a triangle from its three side lengths, for a stained-glass studio. Invalid sides return `"Invalid"`. Right-angle pieces get a `"Right "` prefix so they can be reinforced.

## Files

- `triangle.py` — `is_valid_triangle(a, b, c) -> bool` and `classify_triangle(a, b, c) -> str`
- `test_triangle.py` — unit tests (pytest)
- `test_acceptance.py` — acceptance test built from the studio's requirements
- `requirements.txt` — pins `pytest==9.1.1`

## How to run the tests

```bash
pip install -r requirements.txt
python3 -m pytest -v
```

## Behaviour

- `is_valid_triangle`: `False` if any side is `<= 0` or the triangle inequality fails. The inequality is strict, so the degenerate case (two sides summing to the third) is invalid.
- `classify_triangle` returns one of `"Invalid"`, `"Equilateral"`, `"Isosceles"`, `"Scalene"`, or the last three with a `"Right "` prefix (e.g. `"Right Scalene"`). The Pythagorean check uses a relative tolerance of `1e-9` instead of `==`, so floating-point sides such as `5 * sqrt(2)` are still recognised as right.

## Why an equilateral triangle can never be right

In a right triangle the Pythagorean theorem requires `a² + b² = c²`, where `c` is the hypotenuse, the longest side. An equilateral triangle has `a = b = c`, so the condition becomes `a² + a² = a²`, which reduces to `a² = 0`. That is impossible for a side with positive length, so no equilateral triangle is right-angled. The code returns `"Equilateral"` for these inputs and never adds the prefix.

## Equivalence classes and boundaries

| Class | Example | Result |
|---|---|---|
| Side ≤ 0 (zero or negative) | `(0, 3, 3)`, `(-1, 2, 2)` | `Invalid` |
| Triangle inequality fails | `(1, 2, 10)` | `Invalid` |
| Degenerate (sum equals third side) | `(1, 2, 3)`, `(3, 1, 2)` | `Invalid` |
| Just valid, very flat | `(1, 2, 2.999)` | `Scalene` |
| All sides equal | `(5, 5, 5)` | `Equilateral` |
| Exactly two sides equal | `(5, 5, 7)` | `Isosceles` |
| All sides different | `(2, 3, 4)` | `Scalene` |
| Right, integer sides | `(3, 4, 5)` | `Right Scalene` |
| Right, non-integer sides | `(5, 5, 5√2)`, `(1, 1, √2)` | `Right Isosceles` |
| Near right, outside tolerance | `(3, 4, 5.001)` | `Scalene` |

Boundaries tested: side = 0, the degenerate sum (`a + b = c`), and just inside it: `(1, 2, 2.999)` is valid because `1 + 2 > 2.999`.

## Claude Review Log

Every test in `test_triangle.py` and `test_acceptance.py` was drafted by Claude (an AI assistant). The entries below record the review checks that were actually run.

| Test | Claude-suggested? | Kept / edited / rejected | Why |
|---|---|---|---|
| `test_right_triangle_with_non_integer_sides` | Yes (drafted by Claude) | Kept | Uses `5 * math.sqrt(2)`, which is not exact in floats. Checked by mutation: replacing the tolerance in `triangle.py` with `x*x + y*y == z*z` makes this test and `test_right_isosceles_with_unit_legs` fail, so it catches the `==` mistake. |
| `test_triangle_inequality_failure` (duplicate name) | Yes (drafted by Claude) | Edited | Two tests in the file shared one name, so pytest would silently run only one. Caught with a duplicate-name check (`grep ... \| sort \| uniq -d`). Renamed the `is_valid_triangle` test to `test_is_valid_rejects_triangle_inequality_failure`. |
| Spot check `(0.1+0.2, 0.4, 0.5)` | Yes (drafted by Claude) | Edited | Expected `Invalid`. Wrong: 0.3 + 0.4 > 0.5, so it is valid, and 0.09 + 0.16 = 0.25, so it is exactly right. Corrected the expectation to `Right Scalene`. |

## Acceptance criteria (studio)

The studio's requirement: customers enter three side lengths and are told the shape and whether it is buildable. Invalid input must show a message instead of crashing. Right-angle pieces must be flagged. The answer must be correct every time.

- **AC1 — invalid is reported, never raised.** For every integer triple from -1 to 20 that is not a valid triangle, `classify_triangle` returns `"Invalid"` and raises no exception.
- **AC2 — zero mismatches on valid triangles.** For every integer triple from 1 to 20 that is a valid triangle, the shape and right-angle flag match an exact integer-arithmetic reference (`a² + b² == c²`, no floats). The number of mismatches must be 0.
- **AC3 — non-integer right angles are flagged.** `(5, 5, 5√2)` and `(1, 1, √2)` return `"Right Isosceles"`. `(3, 4, 5.001)` does not return a `"Right "` result.

**Scope limit:** AC1 covers numeric input. Non-numeric input (for example `"a"` or `None`) currently raises `TypeError` — see Known gaps.

## Known gaps

- Non-numeric side values (`"a"`, `None`) raise `TypeError` instead of returning `"Invalid"`. This is not covered by the acceptance criteria above and needs a decision before the studio can use free-text input.

## AI-use disclosure

- **Tool:** Claude (Anthropic), via Claude Code.
- **Used for:** drafting `triangle.py`, the unit tests, the acceptance test and criteria, and this README.
- **Verified by:** running `pytest` (28 unit tests, 1 acceptance test, all passing); a duplicate-test-name check; a mutation test that swaps the tolerance for exact `==`; checking the acceptance reference logic by hand against the spec table; probing non-numeric inputs to find the `TypeError` gap.
- No other AI tool was used.
