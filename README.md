# DSA Experiment: 1 Billion (100 Crore) Integers Analysis

Benchmark study for searching and insertion operations on large datasets (up to 1,000,000,000 integers).

---

## 👥 Team Work Distribution

| Member | Module | Responsibilities | Status |
| :--- | :--- | :--- | :--- |
| **Member 1 (You)** | `src/generation/` | Generate 100 crore integers (Sorted, Unsorted with repetition, Unsorted without repetition) using `random` & custom PRNG without `random`. | **Complete** ✅ |
| **Member 2** | `src/searching/` | Implement and benchmark searching (Binary search on sorted, linear search on unsorted with/without repetition). | In Progress ⏳ |
| **Member 3** | `src/insertion/` | Implement and benchmark insertions (beginning, end, arbitrary position). | In Progress ⏳ |

---

## 📁 Project Directory Structure

```text
DSA-exp/
├── data/                               # Output text files for generated datasets (ignored by git)
│   ├── .gitkeep
│   ├── sorted.txt
│   ├── unsorted_repetition.txt
│   └── unsorted_no_repetition.txt
├── src/
│   ├── __init__.py
│   ├── config.py                       # Paths, chunk sizes, and size constants
│   ├── generation/                     # ⭐ MEMBER 1: DATA GENERATION
│   │   ├── __init__.py
│   │   ├── with_random.py              # Generation using Python's standard `random`
│   │   ├── without_random.py           # Generation without `random` (64-bit LCG & Coprime bijection)
│   │   └── run_generator.py            # CLI generator runner
│   ├── searching/                      # ⭐ MEMBER 2: SEARCHING OPERATIONS
│   │   └── .gitkeep
│   ├── insertion/                      # ⭐ MEMBER 3: INSERTION OPERATIONS
│   │   └── .gitkeep
│   └── utils/
│       ├── __init__.py
│       ├── timer.py                    # High-precision execution timer
│       └── file_io.py                  # Streaming file readers
├── .gitignore
└── README.md
```

---

## 🚀 How to Run the Generation Pipeline

All commands are executed from the project root (`DSA-exp`):

### 1. Fast Sanity Test (100,000 integers)
Generate all 3 files using Python's `random`:
```bash
python src/generation/run_generator.py --count 100000 --method with_random
```

Or using the custom PRNG (without `random`):
```bash
python src/generation/run_generator.py --count 100000 --method without_random
```

### 2. Intermediate Benchmark (1 Crore = 10,000,000 integers)
```bash
python src/generation/run_generator.py --count 10000000 --method with_random
```

### 3. Full Scale (100 Crore = 1,000,000,000 integers)
```bash
python src/generation/run_generator.py --count 1000000000 --method with_random
```

> [!WARNING]
> **Disk Space Notice for 1 Billion Integers**:
> 1 billion integers in text format requires approximately **9.5 to 11 GB of free disk space per file** (~30 GB for all three files). Ensure your drive has sufficient capacity.

---

## ⚙️ Technical Details (Generation Implementation)

1. **Memory Efficiency ($O(1)$ RAM)**:
   - Python cannot hold 1 billion numbers in RAM (~36 GB overhead).
   - All generators use **chunked streaming writes** (`1,000,000` numbers per batch) to keep memory footprint under **~50 MB**.

2. **Unsorted Without Repetition ($O(1)$ Memory Bijective Permutation)**:
   - Standard `random.sample(range(10**9))` or shuffling crashes with `MemoryError`.
   - We utilize a **modular affine permutation generator**:
     $$f(i) = (a \cdot i + c) \pmod N + 1$$
     where $\gcd(a, N) = 1$. This mathematically guarantees 100% unique numbers across all $10^9$ elements with zero memory overhead.

3. **Without `random` Library**:
   - Implements Donald Knuth's 64-bit Linear Congruential Generator (LCG) with multiplier $a = 6364136223846793005$ and increment $c = 1442695040888963407$.
   - Includes custom Euclidean GCD algorithm for the coprime bijection.
