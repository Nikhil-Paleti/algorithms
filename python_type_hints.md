# 📘 Python Type Hints Cheatsheet

## 🔹 Basic Types
- `int`, `float`, `str`, `bool`, `None`
- `Any` → allows any type (from `typing`)

---

## 🔹 Lists / Arrays
```python
nums: list[int] = [1, 2, 3]
words: list[str] = ["a", "b"]
```
✅ Older equivalent: `List[int]` from `typing`

---

## 🔹 Tuples
- Fixed length:
  ```python
  coord: tuple[int, int] = (3, 4)
  rgb: tuple[int, int, int] = (255, 128, 0)
  ```
- Variable length (all same type):
  ```python
  values: tuple[int, ...] = (1, 2, 3, 4, 5)
  ```
- Variable length, mixed `int | str`:
  ```python
  t: tuple[int | str, ...] = (1, "a", 2, "b", "c")
  ```

---

## 🔹 Dictionaries
```python
# Keys are strings, values are ints
ages: dict[str, int] = {"alice": 25, "bob": 30}

# Keys are ints, values are lists of ints
graph: dict[int, list[int]] = {1: [2, 3], 2: [4]}

# Keys are tuples, values are floats
coords: dict[tuple[int, int], float] = {(0,0): 1.5}
```
✅ Older equivalent: `Dict[str, int]`, `Dict[int, List[int]]`

---

## 🔹 Sets
```python
seen: set[int] = {1, 2, 3}
words: set[str] = {"hi", "bye"}
```
✅ Older: `Set[int]`

---

## 🔹 Queues / Deques
```python
from collections import deque
q: deque[int] = deque([1, 2, 3])
```

---

## 🔹 Optional Values
```python
from typing import Optional
name: Optional[str] = None  # could be str or None
```

---

## 🔹 Unions (multiple possible types)
```python
from typing import Union
value: Union[int, float] = 3.14
```
Python 3.10+ shorthand:
```python
value: int | float = 3.14
```

---

## 🔹 Callables (functions)
```python
from typing import Callable
# Function taking int, str → returns bool
func: Callable[[int, str], bool]
```

---

## 🔹 Iterables / Generators
```python
from typing import Iterable, Iterator

nums: Iterable[int]   # anything you can loop over
it: Iterator[str]     # an actual iterator
```

---

## 🔹 Nested structures (common in algorithms)
```python
# Adjacency list for weighted graph
graph: dict[int, list[tuple[int, int]]] = {
    0: [(1, 5), (2, 3)],
    1: [(2, 1)]
}
```

---

# 📝 Quick Reference Table

| Data Structure          | Type Hint Example                  |
|--------------------------|------------------------------------|
| List of ints            | `list[int]`                        |
| List of lists of ints   | `list[list[int]]`                  |
| Tuple (int, str)        | `tuple[int, str]`                  |
| Tuple variable length   | `tuple[int, ...]`                  |
| Tuple int/str variable  | `tuple[int | str, ...]`            |
| Dict str→int            | `dict[str, int]`                   |
| Dict int→list[int]      | `dict[int, list[int]]`             |
| Dict tuple→float        | `dict[tuple[int, int], float]`     |
| Set of ints             | `set[int]`                         |
| Queue of ints           | `deque[int]`                       |
| Optional string         | `str | None` or `Optional[str]`    |
| Union int/float         | `int | float` or `Union[int, float]` |
| Function type           | `Callable[[int, str], bool]`       |
