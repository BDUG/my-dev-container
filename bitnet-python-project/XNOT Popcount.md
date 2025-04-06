
# 🔍 BitNets (XNOR + Popcount)

The term **BitNets (XNOR + Popcount)** describes a technique used in **binary neural networks** that is highly optimized in terms of **memory and computation** — making it ideal for **embedded systems, ARM NEON, FPGAs, or custom hardware**.

---

## 🧠 What is a BitNet?

A **BitNet** is a neural network where:

- The **weights** `W` are binary (`+1 / -1` or `1 / 0`)
- The **activations** `A` are binary as well

As a result, the **matrix multiplication** (the most computationally expensive operation in neural nets) can be replaced by simple **bitwise operations**.

---

## ⚙️ BitNet Principle: XNOR + Popcount

### 💡 Idea

Instead of expensive floating-point multiplications:

```text
z = A · W   (float: expensive)
```

→ Use:

```text
z = popcount(XNOR(A_bin, W_bin))
```

---

### 🧮 How does it work?

**Binary encoding:**

- `+1` → `1` (bit set)  
- `-1` → `0` (bit cleared)

**XNOR operation:**

- Bitwise comparison: `1 XNOR 1 = 1`, `0 XNOR 0 = 1`, otherwise `0`
- This yields `1` when the bits match (i.e., the multiplication is correct)

**Popcount:**

- Counts how many `1`-bits are present in the result
- This is equivalent to counting how many bit pairs matched
- → Result is **proportional to the dot product**

---

## 🔢 Example in Action

```text
A_bin = [1, 0, 1, 1]   → corresponds to [+1, -1, +1, +1]  
W_bin = [1, 1, 0, 1]   → corresponds to [+1, +1, -1, +1]

XNOR  = [1, 0, 0, 1]   → two matches  
Popcount = 2  
→ corresponds to a positive dot product score (2 out of 4 match)
```

---

## 🧩 Benefits

✅ **Speed**

- Instead of `n` float multiplications → only **1 XNOR** + **1 Popcount** over `n` bits  
- Enables up to **32× or 64× parallel processing** with `uint32_t` / `uint64_t`

✅ **Memory-efficient**

- 1 bit per weight instead of 32 bits → **32× smaller**

✅ **Optimizable via NEON / SIMD**

- Perfect for hardware with **ARM NEON**, **AVX2**, **SVE**, etc.

✅ **Simple to implement**

- Only a few bitwise operations needed (e.g., `vmvn`, `veor`, `vcnt` in NEON)

---

## ⚙️ Example Code (C with ARM NEON)

```c
#include <arm_neon.h>

int binary_dot(uint8x16_t a, uint8x16_t b) {
    uint8x16_t xnor = vmvnq_u8(veorq_u8(a, b));  // XNOR = ~(a ^ b)
    uint8x16_t pop = vcntq_u8(xnor);            // Popcount per byte
    uint16x8_t sum16 = vpaddlq_u8(pop);         // Pairwise add
    uint32x4_t sum32 = vpaddlq_u16(sum16);
    uint64x2_t sum64 = vpaddlq_u32(sum32);
    return vgetq_lane_u64(sum64, 0) + vgetq_lane_u64(sum64, 1);
}
```
