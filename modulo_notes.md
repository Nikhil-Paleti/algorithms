# Modulo & Division Quick Notes

## 1. Next index in circular array
```python
next = (i + 1) % n
```
- Moves to next slot  
- Wraps to `0` when `i = n-1`

## 2. Previous index in circular array
```python
prev = (i - 1 + n) % n
```
- Moves to previous slot  
- Wraps to `n-1` when `i = 0`

## 3. Number of chunks (ceil division)
```python
chunks = (num + size - 1) // size
```
- Splits `num` items into groups of `size`  
- Example: `num=10, size=3 → 4 chunks`

---

👉 **Mental model**  
- **Modulo** = “wrap around in a circle”  
- **`(num + size - 1) // size`** = ceiling division (rounding up)  
