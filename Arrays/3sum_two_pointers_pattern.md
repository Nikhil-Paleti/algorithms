
# 📘 3Sum Pattern – Fixing `i` vs Fixing `k` (Which to Choose?)

This note extends your two‑pointers + outer loop pattern with **when to fix the smallest (`i`) vs the largest (`k`) element**, why one is often safer, and ready‑to‑paste templates.

---

## 🔹 TL;DR – Which should I fix?

- **Prefer fixing `i` (the smallest)** in interviews.  
  - Duplicate handling is clean (skip duplicate `i`s).
  - Guarantees no missed triplets when you skip duplicates correctly.
  - Most editorial/standard solutions use this.

- **Fixing `k` (the largest)** is also valid **but trickier**.  
  - You must be careful with duplicate `k`s; skipping the wrong way can miss valid triplets (e.g., `[-2,1,1]`).  
  - If you keep all `k`s, you need careful duplicate skip on `i`/`j`, or dedupe with a `set`.

---

## 🔹 Why fixing `i` is safer

After sorting:
- Fixing `i` (smallest) → search for a pair `(l, r)` so that `nums[i] + nums[l] + nums[r] == 0`.
- Skipping duplicate `i`s is **safe**: once you processed a specific `nums[i]`, repeating the same value will only produce triplets you already found.
- After finding a valid triplet, skipping duplicates on both `l` and `r` advances to the next distinct pair—no missed solutions.

**Common pitfall avoided:** When fixing `k`, if you skip duplicate `k`s naively, you can miss triplets where the two equal numbers are the middle ones (e.g., `[-2,1,1]`).

---

## 🔹 When might fixing `k` be okay?

- If your counting logic benefits from treating the **largest element as a boundary** (e.g., **Valid Triangle Number**).  
- If you dedupe with a **`set`** (simple but extra memory), or you’re very careful to **not** skip necessary duplicate `k`s (and instead skip duplicates on `i`/`j` after recording a hit).

---

## 🔹 Templates

### ✅ Standard (Recommended): Fix `i` (smallest) + two pointers
```python
def threeSum(nums):
    nums.sort()
    n = len(nums)
    ans = []
    for i in range(n - 2):
        if i > 0 and nums[i] == nums[i - 1]:
            continue              # skip duplicate i
        if nums[i] > 0:
            break                 # no triplet can sum to 0 beyond this point
        l, r = i + 1, n - 1
        while l < r:
            s = nums[i] + nums[l] + nums[r]
            if s < 0:
                l += 1
            elif s > 0:
                r -= 1
            else:
                ans.append([nums[i], nums[l], nums[r]])
                lv, rv = nums[l], nums[r]
                while l < r and nums[l] == lv: l += 1   # skip dups on left
                while l < r and nums[r] == rv: r -= 1   # skip dups on right
    return ans
```
- **Time**: O(n²), **Space**: O(1) extra (ignoring output & sort).

---

### ✅ Alternative: Fix `k` (largest) + two pointers
**Option A (no set, careful duplicate handling):**
```python
def threeSum(nums):
    nums.sort()
    n = len(nums)
    ans = []
    for k in range(2, n):
        i, j = 0, k - 1
        while i < j:
            s = nums[i] + nums[j] + nums[k]
            if s < 0:
                i += 1
            elif s > 0:
                j -= 1
            else:
                ans.append([nums[i], nums[j], nums[k]])
                vi, vj = nums[i], nums[j]
                while i < j and nums[i] == vi: i += 1   # skip dups on i
                while i < j and nums[j] == vj: j -= 1   # skip dups on j
    return ans
```
- Do **not** skip duplicate `k` up front (can miss valid triplets).  
- Rely on skipping duplicates for `i` and `j` after each hit.

**Option B (simplest logic using a set):**
```python
def threeSum(nums):
    nums.sort()
    n = len(nums)
    seen = set()
    for k in range(2, n):
        i, j = 0, k - 1
        while i < j:
            s = nums[i] + nums[j] + nums[k]
            if s < 0:
                i += 1
            elif s > 0:
                j -= 1
            else:
                seen.add((nums[i], nums[j], nums[k]))
                vi, vj = nums[i], nums[j]
                while i < j and nums[i] == vi: i += 1
                while i < j and nums[j] == vj: j -= 1
    return [list(t) for t in seen]
```
- **Easiest** to reason about; uses extra space for dedupe.

---

## 🔹 Example where fixing `k` and skipping duplicate `k` fails

`nums = [-2, 0, 1, 1, 2]`  
- Triplets: `[-2, 0, 2]`, `[-2, 1, 1]`.
- If you `continue` when `nums[k] == nums[k-1]`, you may **skip k=3 (the second 1)** and miss `[-2,1,1]`.

**Fix:** Either don’t skip duplicate `k`, or dedupe results via set, or use the standard **fix `i`** approach.

---

## 🔹 Decision checklist

- **Triplets?** Sort the array.  
- **Need unique triplets?**  
  - Prefer **fix `i`**; skip duplicates of `i`, then skip duplicates of `l` and `r` after hits.  
  - If you must fix `k`, either avoid skipping duplicate `k` or dedupe with a `set`.
- **Counting combinations instead of listing them?**  
  - Fixing the **boundary** (often the largest) can be more natural, e.g., Valid Triangle Number.

---

## 🔹 Complexity (both styles)
- Sorting: O(n log n)  
- Two pointers per outer index: O(n)  
- Outer loop over ~n indices → **O(n²)** total  
- Space: O(1) extra (except for the optional `set` approach)

---

## 🔹 Intuition refresher (why two pointers work)
- Sorting gives a **monotonic** structure.  
- With one index fixed, the condition `sum < 0` or `sum > 0` tells you **which pointer to move** to get closer to the target.  
- When `sum == 0`, record and **skip duplicates** on both sides to move to the next new pair.

---

## 🔹 Quick references
- **3Sum (unique triplets)** → fix `i`.  
- **3Sum Closest** → fix `i`, track best diff.  
- **Valid Triangle Number** → fix `k` (largest), count `j - i` when condition holds.  
- **4Sum** → fix two indices (`i`, `j`), then two pointers on the inner pair.

