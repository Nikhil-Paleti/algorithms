
# 📘 Notes on Binary Search & Bisect (Left & Right)

## 🔹 Intuition

### Binary Search
- **Goal**: Find an element in a sorted array efficiently.  
- Works by repeatedly dividing the search space in half.  
- Time complexity: **O(log n)**.  
- If the array is sorted, binary search is the go-to method.  

---

### Bisect (Binary Search Variants)
- Sometimes we don’t just need to check **if an element exists**; we want to know:
  - **Where should we insert** a number in a sorted array?  
  - Do we insert it **before** existing duplicates (`bisect_left`) or **after** (`bisect_right`)?  

- This is useful for problems like:
  - Finding the **lower bound** (first index where element ≥ target).  
  - Finding the **upper bound** (first index where element > target).  
  - Maintaining a **sorted list** after insertions.  

---

## 🔹 Python Implementations

### 1. `binary_search`
```python
def binary_search(a, x):
    """Return index of x if found, else -1."""
    lo, hi = 0, len(a) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if a[mid] == x:
            return mid
        elif a[mid] < x:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1
```

---

### 2. `bisect_left`
```python
def bisect_left(a, x, lo=0, hi=None):
    """Return leftmost insertion index for x in sorted list a."""
    if hi is None:
        hi = len(a)
    while lo < hi:
        mid = (lo + hi) // 2
        if a[mid] < x:
            lo = mid + 1
        else:
            hi = mid
    return lo
```

---

### 3. `bisect_right`
```python
def bisect_right(a, x, lo=0, hi=None):
    """Return rightmost insertion index for x in sorted list a."""
    if hi is None:
        hi = len(a)
    while lo < hi:
        mid = (lo + hi) // 2
        if a[mid] <= x:
            lo = mid + 1
        else:
            hi = mid
    return lo
```

---

## 🔹 Edge Case Behavior

### `bisect_left(nums, target)` can return:
- `0` if target is smaller than all elements.  
- `len(nums)` if target is larger than all elements.  
- The index of the **first element ≥ target** if target falls inside.  

### `bisect_right(nums, target) - 1` can return:
- `-1` if target is smaller than all elements.  
- `len(nums) - 1` if target is larger than all elements.  
- The index of the **predecessor (largest < target)** if target isn’t present but falls inside.  

This is why the typical check for range queries is:

```python
left  = bisect_left(nums, target)
right = bisect_right(nums, target) - 1

if left <= right and left < len(nums) and nums[left] == target:
    return [left, right]
return [-1, -1]
```

---

## 🔹 Example Usage

```python
arr = [1, 2, 4, 4, 5, 7]

# --- Binary search ---
print(binary_search(arr, 5))  # 4 (index of 5)
print(binary_search(arr, 3))  # -1 (not found)

# --- Bisect left/right ---
print(bisect_left(arr, 4))    # 2 (insert before first 4)
print(bisect_right(arr, 4))   # 4 (insert after last 4)

print(bisect_left(arr, 3))    # 2 (index to insert 3)
print(bisect_right(arr, 3))   # 2 (same as left since 3 not present)
```

---

## 🔹 Example Problems

### Problem 1: Search in Rotated Sorted Array
- Use **binary search** with conditions to decide which half to explore.  

---

### Problem 2: First & Last Position of Element in Sorted Array
- Use **bisect_left** to find the first index.  
- Use **bisect_right - 1** to find the last index.  

```python
def search_range(nums, target):
    left = bisect_left(nums, target)
    right = bisect_right(nums, target) - 1
    if left <= right and left < len(nums) and nums[left] == target:
        return [left, right]
    return [-1, -1]
```

---

### Problem 3: Count Occurrences
- Occurrences of `x` = `bisect_right(a, x) - bisect_left(a, x)`.  

---

### Problem 4: Maintain Sorted List
- To insert `x` in order:  
  - Use `i = bisect_left(a, x)`  
  - Then `a.insert(i, x)`  

---

## 🔹 Key Takeaways
- **Binary Search** → find element, O(log n).  
- **Bisect Left** → lower bound (first ≥ target).  
- **Bisect Right** → upper bound (first > target).  
- Edge cases matter: `bisect_left` can equal `len(nums)`, `bisect_right-1` can be `-1`.  
- Very useful in **range queries**, **counting elements**, and **sorted insertions**.  
