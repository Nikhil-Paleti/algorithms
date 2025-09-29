
# 📘 Two-Pointers with a Fixed Index (3‑Sum Pattern & Triangle Counting)

A practical cheat sheet for problems that reduce an O(n³) triplet search to **O(n²)** by:
1) **Sorting** the array,  
2) **Fixing one index** in an outer loop,  
3) Running **two pointers** for the remaining two indices.

---

## 🧭 When to Use This Pattern
Use it when all of the following hold:
- You’re dealing with **triplets** (or k=4 with two fixed indices).  
- The array can be **sorted** without breaking correctness.  
- The predicate is **monotonic** under index movement (e.g., sum increases when right pointer moves right, decreases when left pointer moves left).

**Typical tasks:** 3Sum, 3Sum Closest, 4Sum (fix two, two pointers), **Valid Triangle Number**.

---

## 🔧 Core Template (Fix One, Sweep Two)

```python
nums.sort()
n = len(nums)
for fixed in range(n - 2):              # choose which index you fix
    left, right = fixed + 1, n - 1
    while left < right:
        # evaluate condition involving nums[fixed], nums[left], nums[right]
        if condition_is_small:
            left += 1                    # grow the value
        elif condition_is_large:
            right -= 1                   # shrink the value
        else:
            # handle hit
            # then move past duplicates on both sides:
            valL, valR = nums[left], nums[right]
            while left < right and nums[left] == valL: left += 1
            while left < right and nums[right] == valR: right -= 1
```

**Why it’s fast:** each inner scan moves pointers monotonically and never revisits pairs → **O(n)** per outer index → **O(n²)** total, after an initial **O(n log n)** sort.

---

## 🔹 3Sum (LeetCode 15) — Fix the **Smallest** (`i`) ✅

**Goal:** find unique triplets summing to 0.

**Template:**
```python
def threeSum(nums):
    nums.sort()
    n = len(nums)
    ans = []
    for i in range(n - 2):
        if i > 0 and nums[i] == nums[i - 1]:   # skip duplicate i
            continue
        if nums[i] > 0:                         # smallest > 0 → no sum 0 possible
            break
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
                while l < r and nums[l] == lv: l += 1
                while l < r and nums[r] == rv: r -= 1
    return ans
```
**Why fixing `i` is nice:** skipping duplicate `i` is safe and avoids missing solutions; duplicate handling sits cleanly at one place.

---

## 🔹 Valid Triangle Number (LeetCode 611)

A triangle is valid if `a + b > c` for sides `(a ≤ b ≤ c)`. After sorting, we need to count `(i, j, k)` with `i < j < k` such that:
```
nums[i] + nums[j] > nums[k]
```

### Option A — Fix the **Largest** (`k`) ✅ (most intuitive)
```python
def triangleNumber(nums):
    nums.sort()
    n = len(nums)
    ans = 0
    for k in range(2, n):
        i, j = 0, k - 1
        while i < j:
            if nums[i] + nums[j] > nums[k]:
                ans += (j - i)      # all i..j-1 with this j work
                j -= 1
            else:
                i += 1
    return ans
```
**Intuition:** with `k` fixed, if `nums[i] + nums[j] > nums[k]`, then increasing `i` only increases the sum, so all pairs `(i..j-1, j)` are valid at once.

### Option B — Fix the **Smallest** (`i`) (symmetric pattern)
```python
def triangleNumber(nums):
    nums.sort()
    n = len(nums)
    ans = 0
    for i in range(n - 2):
        if nums[i] == 0:            # zero can't start a valid triangle
            continue
        k = i + 2
        for j in range(i + 1, n - 1):
            while k < n and nums[i] + nums[j] > nums[k]:
                k += 1
            ans += max(0, k - j - 1)    # all (j+1 .. k-1) valid with this (i, j)
    return ans
```
**Intuition:** for fixed `i`, as `j` increases, the maximal feasible `k` never moves backward → one forward-moving `k` pointer amortizes to **O(n)**.

**Both options:** **O(n²)** time, **O(1)** extra space (ignoring sort).

---

## 🧩 Recognizing Monotonic Moves
- **Sum too small?** move the pointer that **increases** the value (usually `left++`).  
- **Sum too large?** move the pointer that **decreases** the value (usually `right--`).  
- **Hit?** record, then **skip duplicates on both sides** to move to the next distinct pair.

---

## 🧪 Quick Examples

### Triangle Count on `[2,2,3,4]`
- **Fix k:** yields 3 triangles: `(2,2,3)`, `(2,3,4)` (twice with different indices).  
- **Fix i:** same count using the `j` loop and forward `k` pointer.

### 3Sum on `[-2,0,1,1,2]`
- Fix `i`: gets `[-2,0,2]` and `[-2,1,1]`.  
- Avoid global `set` by skipping duplicates at `i`, and locally at `l/r` after hits.

---

## ⚙️ Complexity Cheats
- Sorting: **O(n log n)**.  
- Outer loop × inner two-pointer scan: **O(n²)** total.  
- Space: **O(1)** extra (unless using a `set` to dedupe results explicitly).

---

## 🗺️ Decision Guide
- **Need unique triplets (like 3Sum)?** Fix **`i`** (smallest) and skip dups.  
- **Counting combinations with inequality boundary (like triangles)?** Fix **`k`** (largest) or **`i`** with a forward `k`.  
- **Condition monotonic after sorting?** Two-pointers is your friend.  
- When in doubt, **sort, fix one, and check the monotonic move**.

---

## 📝 Bonus: Bisect Variant (Slower but OK)
For counting tasks, you can sometimes replace the inner pointer by a **binary search** (e.g., find first `k` where `nums[k] >= nums[i]+nums[j]`).  
- Time: **O(n² log n)**.  
- Simpler to code if you’re very comfortable with `bisect`, but two-pointers is optimal.

---
