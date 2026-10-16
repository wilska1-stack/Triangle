# Triangle Classifier

`triangle.py` provides two functions:

- `is_valid_triangle(a, b, c) -> bool`: `False` if any side is `<= 0` or if the triangle inequality fails. The inequality is strict, so the degenerate case (two sides summing to the third) is invalid.
- `classify_triangle(a, b, c) -> str`: returns `"Invalid"`, `"Equilateral"`, `"Isosceles"`, or `"Scalene"`. Right triangles get a `"Right "` prefix, e.g. `"Right Scalene"`. The Pythagorean check uses a relative tolerance (`1e-9`) instead of `==` to absorb floating-point error.

## Why an equilateral triangle can never be right

In a right triangle the Pythagorean theorem requires `a² + b² = c²`, where `c` is the hypotenuse, the longest side. An equilateral triangle has `a = b = c`, so the condition becomes `a² + a² = a²`, which reduces to `a² = 0`. That is impossible for a side with positive length, so no equilateral triangle is right-angled.

## Example

```python
from triangle import classify_triangle

classify_triangle(3, 4, 5)  # "Right Scalene"
classify_triangle(5, 5, 5)  # "Equilateral"
classify_triangle(1, 2, 3)  # "Invalid" (degenerate)
```
