# ✅ Sentinel Pattern (Sentinel Sweep) in Coding Interviews

## 🧠 What Is the Sentinel Pattern?

The **Sentinel Pattern** (also called **Sentinel Sweep**) is a technique where we intentionally add an extra “dummy”/boundary value to the beginning or end of an array or structure.  
This helps **avoid edge-case checks**, making the solution cleaner and more elegant.

Instead of writing special logic for:

- First element
- Last element
- Empty input

…we **add an artificial boundary** and let the loop handle everything.

---

## 🎯 Why Use It?

✔ Eliminates ugly `if i == 0`, `if i == n-1`, or `if array is empty` checks  
✔ Unified logic in a single loop  
✔ Very useful in interval problems, stack problems, and parsing  
✔ Makes your code appear more mature and intentional during interviews

---

## 🛠 Core Template

```python
prev = lower_bound - 1

for curr in nums + [upper_bound + 1]:  # ← Sentinel added
    if curr - prev >= 2:
        record missing range [prev + 1, curr - 1]
    prev = curr
```

---

## 📌 Where Is This Used?

| Problem Category           | Use of Sentinel                               |
|----------------------------|-----------------------------------------------|
| Missing Ranges             | Add `upper + 1` to flush the last interval   |
| Merge Intervals            | Add `[-inf, -inf]` or `[inf, inf]`           |
| Histogram / Stack Problems | Add `0` height at the end to flush stack     |
| Linked Lists               | Add a dummy head node (`ListNode(-1)`)       |
| String Parsing             | Add extra `)` or `+` to force final compute  |
| Sliding Window / Prefix Sum| Add 0 or large limits to simplify edge cases |

---

## ✅ Example: LeetCode 163 — Missing Ranges

```python
class Solution:
    def findMissingRanges(self, nums, lower, upper):
        res = []
        prev = lower - 1

        for curr in nums + [upper + 1]:
            if curr - prev >= 2:
                res.append([prev + 1, curr - 1])
            prev = curr

        return res
```

---

## 🧩 Common Sentinel Variations

| Sentinel Type         | Example                                          |
|------------------------|--------------------------------------------------|
| Right sentinel         | `nums + [upper + 1]`                           |
| Left sentinel          | `[lower - 1] + nums`                           |
| Dummy linked list node | `dummy = ListNode(0, head)`                   |
| Stack sentinel         | Add 0 height to histogram bars                 |
| String parsing         | Append `')'`, `'+'`, or `' '` at end           |

---

## 📝 LeetCode Problems to Practice This Pattern

### ✅ **Directly Using Sentinel Boundary**

- 163. Missing Ranges  
- 228. Summary Ranges  
- 57. Insert Interval  
- 56. Merge Intervals  
- 252. Meeting Rooms  
- 986. Interval List Intersections

---

### ✅ **Using Dummy Nodes / Sentinel in Linked Lists**

- 21. Merge Two Sorted Lists  
- 83. Remove Duplicates from Sorted List  
- 82. Remove Duplicates II  
- 203. Remove Linked List Elements  
- 2. Add Two Numbers  

---

### ✅ **Using Sentinel in Stack Problems**

- 84. Largest Rectangle in Histogram  
- 42. Trapping Rain Water  
- 739. Daily Temperatures (optional sentinel use)  

---

### ✅ **Using Sentinel in String Parsing**

- 227. Basic Calculator II  
- 224. Basic Calculator  
- 20. Valid Parentheses  
- 394. Decode String  

---

## 🧠 How to Recognize When to Use It?

Look for these signs:
- “I need to handle the last remaining item…”
- “I’m writing a special condition just for the first/last element.”
- “My code has too many boundary checks.”
- “After the loop ends, I still need to append something manually.”

When that happens → **Think: _“Can I add a sentinel?”_**

---

## ✅ Summary Cheat Sheet

✔ **Sentinel = fake boundary value to simplify logic**  
✔ **Avoids first/last element edge-case checks**  
✔ **Common in interval, stack, string parsing, and linked list problems**  
✔ **Makes your code cleaner and interview-friendly**

---

Happy coding 🚀
