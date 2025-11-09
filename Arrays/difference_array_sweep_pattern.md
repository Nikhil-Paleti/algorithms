# 🧮 Difference Array / Sweep Line Pattern

## 🧩 Overview

This is one of the most powerful and common **prefix-sum–based patterns** used to efficiently handle **range updates** or **interval coverage counting**.

Instead of explicitly iterating through every index of an interval, you **record start and end events**, and then compute a running prefix sum to recover the actual values or coverage counts.

---

## ⚙️ Core Idea

When you want to add a value `v` to every element in range `[L, R]`:

```python
diff[L]   += v
diff[R+1] -= v
```

Then, after processing all intervals:
```python
prefix_sum = 0
for i in range(n):
    prefix_sum += diff[i]
    actual[i] = prefix_sum
```

This converts *range updates* → *two-point events* → *O(n)* prefix reconstruction.

---

## 💡 Identification Clues

You’re likely looking at a **difference array / sweep line** problem when:

| Symptom | Explanation |
|----------|--------------|
| You’re repeatedly updating or counting over ranges `[L, R]` | Each query modifies many elements → need aggregated updates |
| You only care about final or aggregate results, not intermediate states | You can apply updates lazily and resolve with prefix sums |
| You want to know “how many intervals cover each point” | Same structure: `+1` on start, `-1` on end+1`, then sweep |
| You’re asked for max overlap, total coverage, or union length | Classic sweep-line cases |
| The constraints are large (e.g., 1e5+ intervals or operations) | Direct simulation is too slow; prefix trick saves time |

---

## 🧠 Intuition

Think of this like **marking entry and exit points on a number line**:

```
Interval [L, R]
   +1 at L   (enter)
   -1 at R+1 (exit)
```

When you “walk” from left → right and maintain a running sum,
that sum tells you **how many intervals currently cover** that point.

---

## 🧩 Typical Use Cases

| Category | Examples |
|-----------|-----------|
| Range updates / accumulations | Add `k` to `[L, R]`, then query array |
| Interval overlaps | How many intervals cover each point |
| Flight bookings / events timeline | LC 1109 – Corporate Flight Bookings |
| Skyline / meeting rooms | Start/end events → track active count |
| Histogram or prefix computations | Range sums, light bulbs, heat maps |

---

## 📘 Example 1 — Interval Coverage Counting

```python
from collections import defaultdict

nums = [3, 8]
k = 2
# Each element defines interval [x - k, x + k]
events = defaultdict(int)
for x in nums:
    L, R1 = x - k, x + k + 1
    events[L] += 1
    events[R1] -= 1

active = 0
for point in sorted(events):
    active += events[point]
    print(f"At {point}: {active} active intervals")
```

Output:
```
At 1: 1
At 6: 0
At 6: 1
At 11: 0
```

---

## 📘 Example 2 — LeetCode Problems

| Problem | Type | Pattern Use |
|----------|------|-------------|
| **LC 1109 – Corporate Flight Bookings** | Range addition | Apply +v/-v, prefix at end |
| **LC 370 – Range Addition** | Classic | Same diff array idea |
| **LC 253 – Meeting Rooms II** | Sweep line | Start +1, end -1, track max active |
| **LC 3347 – Max Frequency After Operations II** | Interval coverage | +1 at L, −1 at R+1, prefix to count coverage |
| **LC 218 – The Skyline Problem** | 2D sweep line | Sort events, maintain active set |

---

## ⚡️ Key Complexity Benefits

| Operation | Naive | Difference Array / Sweep |
|------------|--------|--------------------------|
| Range update | O(n) per update | O(1) per update |
| Range query after updates | O(n) | O(n) once via prefix |
| Memory | O(n) | O(n) |
| Common use | large intervals, offline computations | ✅ ideal |

---

## 🧩 Mental Model

> “Mark when something **starts**, mark when it **ends**,  
> and let the **prefix sum** tell you how many are active.”

---

## 🧱 Summary

| Concept | Keyword |
|----------|----------|
| Add events only at boundaries | +1 / -1 |
| Reconstruct final state | prefix sum |
| Prevent double counting | exclusive end (R+1) |
| Generalization | Sweep line, range diff array, interval compression |

---

**In short:**  
> “Two marks + prefix sum = efficient range updates.”  
>  
> — The difference array / sweep-line pattern
