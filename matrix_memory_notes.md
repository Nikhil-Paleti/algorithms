# 📘 Notes on Matrix/Tensor Memory Size + Unit Conversions

---

## 🔹 1. Memory Size Formula
\[
\text{Memory (bytes)} = \text{Number of elements} \times \text{Bytes per element}
\]

- Elements = product of all dimensions  
- Bytes per element (common dtypes):
  - `float16` / `bfloat16` → 2 bytes  
  - `float32` → 4 bytes  
  - `float64` → 8 bytes  
  - `int8` → 1 byte  

---

## 🔹 2. Unit Conversions (Binary vs Decimal)

- **Binary (power of 2, common in OS / RAM reporting):**
  - 1 KB = 2^10 = 1024 bytes  
  - 1 MB = 1024 KB = 1024^2 = 1,048,576 bytes  
  - 1 GB = 1024 MB = 1024^3 ≈ 1.07 × 10^9 bytes  
  - 1 TB = 1024 GB = 1024^4 ≈ 1.10 × 10^12 bytes  

- **Decimal (power of 10, common in storage marketing like HDD/SSD):**
  - 1 KB = 1000 bytes  
  - 1 MB = 10^6 bytes  
  - 1 GB = 10^9 bytes  
  - 1 TB = 10^12 bytes  

⚠️ This is why your “1 TB hard drive” shows as ~931 GB in your OS.

---

## 🔹 3. Bits vs Bytes
- `b` (lowercase) = **bit** (0 or 1)  
- `B` (uppercase) = **byte** (8 bits)

Examples:  
- **MB** = megabyte = 10^6 bytes (storage) or 2^20 bytes (binary MB)  
- **Mb** = megabit = 10^6 bits = 125,000 bytes (~0.125 MB)  

👉 Internet speeds are usually in **megabits per second (Mbps)**, but file sizes are in **megabytes (MB)**.  
So a **100 Mbps** connection = ~**12.5 MB/s** download speed.

---

## 🔹 4. Example: m × n fp16 matrix
- Each element = 2 bytes  
- Memory = m × n × 2 bytes

Example:  
`1000 × 2000` fp16 matrix  
= 1000 × 2000 × 2 = 4,000,000 bytes  
≈ 3.81 MB (binary MB)

---

## 🔹 5. Reverse Calculation: Given memory budget
If you have `M` bytes RAM:

\[
\text{Max elements} = \frac{M}{\text{bytes per element}}
\]

- **1 GB RAM** (binary = 1024^3 bytes) = 1,073,741,824 bytes  
- For fp16 (2 bytes):  
  Max elements = 1,073,741,824 / 2 ≈ 536,870,912

---

## 🔹 6. Shapes you can fit (fp16, 1 GB RAM)
- **Arbitrary matrix (m × n):**  
  m × n ≤ 536,870,912

- **Square matrix:**  
  n^2 ≤ 536,870,912  
  ⇒ n ≤ √536,870,912 ≈ 23,170  
  → ~23k × 23k fits

- **Fix one dimension (say m = 1000):**  
  n ≤ 536,870,912 / 1000 ≈ 536,870

---

## 🔹 7. Generalization to Tensors
For shape (d1, d2, ..., dk):

\[
\text{Memory (bytes)} = (d1 × d2 × ... × dk) × \text{bytes per element}
\]

---

## 🔹 8. Quick Formulas
- Memory (MB) ≈  
  (num elements × bytes per element) / 1024^2

- Max elements =  
  RAM bytes / bytes per element

- Max square dim =  
  √(Max elements)

- Fix one dimension m:  
  n = Max elements / m

---

⚡ **Practical tip:** On GPUs, usable VRAM < total VRAM (reserve ~10–20% for overhead).
