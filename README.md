# DSA Experiment: 100 Crore (1 Billion) Integers Analysis

A comprehensive performance analysis study comparing searching and insertion operations across massive integer datasets (up to 1,000,000,000 integers).

---

## 📋 Problem Statement

1. **Generation**:
   - Generate **100 crore (1 billion)** integers and store them in text files.
   - Support both:
     - **Sorted array**
     - **Unsorted array with repetition**
     - **Unsorted array without repetition**
   - Provide two independent generation pipelines:
     - **With standard `random` library**
     - **Without `random` library** (pure custom PRNG from first principles).
2. **Searching Operations** (Assigned to Teammate 2):
   - Search in a sorted array.
   - Search in an unsorted array with repetition.
   - Search in an unsorted array without repetition.
3. **Insertion Operations** (Assigned to Teammate 3):
   - Insert an element at the beginning of an array.
   - Insert an element at the end of an array.
   - Insert an element at any specified position in an array.
4. **Benchmarking & Analysis**:
   - Analyze and compare the execution times of all operations using high-precision timers.

---

## 👥 Team Work Distribution

| Member | Module Directory | Responsibility | Status |
| :--- | :--- | :--- | :--- |
| **Member 1 (You)** | `src/generation/` | Dataset generation (Sorted, Unsorted with repetition, Unsorted without repetition) with and without Python's `random` library; file I/O optimization; timing infrastructure. | **Complete** ✅ |
| **Member 2** | `src/searching/` | Searching algorithms (Binary Search, Linear Search first/all) and execution time benchmarks. | *Pending Teammate* ⏳ |
| **Member 3** | `src/insertion/` | Insertion algorithms (beginning, end, arbitrary index) and execution time benchmarks. | *Pending Teammate* ⏳ |

---

## 📁 Repository & Folder Architecture

```text
DSA-exp/
├── data/                               # Directory for generated .txt dataset files (git-ignored)
│   ├── .gitkeep
│   ├── sorted.txt                      # 1 Billion sorted integers
│   ├── unsorted_repetition.txt         # 1 Billion unsorted integers (with duplicates)
│   └── unsorted_no_repetition.txt      # 1 Billion unsorted integers (100% unique)
│
├── src/
│   ├── __init__.py                     # Package initializer
│   ├── config.py                       # Global paths, buffer sizes, and dataset presets
│   │
│   ├── generation/                     # ⭐ MEMBER 1: DATASET GENERATION
│   │   ├── __init__.py                 # Exports generation functions
│   │   ├── with_random.py              # Generation using Python's built-in `random` module
│   │   ├── without_random.py           # Generation WITHOUT `random` (Custom 64-bit LCG & Coprime bijection)
│   │   └── run_generator.py            # Unified CLI runner with progress reporting
│   │
│   ├── searching/                      # 📂 MEMBER 2: SEARCHING OPERATIONS
│   │   └── .gitkeep                    # Reserved workspace for Member 2
│   │
│   ├── insertion/                      # 📂 MEMBER 3: INSERTION OPERATIONS
│   │   └── .gitkeep                    # Reserved workspace for Member 3
│   │
│   └── utils/                          # Shared Utilities
│       ├── __init__.py
│       ├── timer.py                    # High-precision execution timer context manager
│       └── file_io.py                  # Streaming line-by-line file reader for large datasets
│
├── .gitignore                          # Excludes large data files (>30 GB) and caches
└── README.md                           # Comprehensive documentation
```

---

## 🔬 Technical Design: Generation Module

### 1. Memory Challenge & $O(1)$ RAM Streaming Solution
* **The Problem**: Storing 1,000,000,000 integers in a Python list requires **~36 GB of RAM** ($28\text{ bytes per int} + 8\text{ bytes per pointer}$). Standard machines will instantly crash with `MemoryError`.
* **The Solution**: All generators stream data directly to disk in **buffered chunks** (default: `1,000,000` numbers per flush).
* **RAM Footprint**: Under **50 MB**, regardless of whether you generate 100 thousand or 1 billion integers.

### 2. Method 1: Generation WITH Python's `random` Library (`with_random.py`)
- **Sorted Array**: Starts at an initial base integer and accumulates a random positive delta ($+1$ to $+5$) at each step, ensuring strictly non-decreasing order.
- **Unsorted with Repetition**: Randomly samples numbers from a bounded range (`[1, 10,000,000]`), naturally creating duplicate values across $10^9$ elements.
- **Unsorted without Repetition**: Uses a **modular affine permutation generator**:
  $$f(i) = ((a \cdot i + c) \pmod N) + 1$$
  where $a$ is chosen randomly such that $\gcd(a, N) = 1$, and $c \in [1, N-1]$.
  By number theory, this creates a **bijective map** of $\{0, \dots, N-1\}$. Every single integer from $1$ to $N$ appears **exactly once** in pseudo-random order without maintaining a 36 GB hash set or array in memory.

### 3. Method 2: Generation WITHOUT `random` Library (`without_random.py`)
Built completely from first principles with **zero external or standard math/random library imports**:
- **Custom 64-bit Linear Congruential Generator (LCG)**:
  Uses Donald Knuth's MMIX constants:
  $$X_{n+1} = (a \cdot X_n + c) \pmod{2^{64}}$$
  - Multiplier $a = 6364136223846793005$
  - Increment $c = 1442695040888963407$
  - Modulus $m = 2^{64}$ (handled via `& 0xFFFFFFFFFFFFFFFF`)
- **Custom Euclidean GCD**:
  Computes the greatest common divisor from scratch to find coprime values for duplicate-free bijection:
  ```python
  def custom_gcd(a: int, b: int) -> int:
      while b != 0:
          a, b = b, a % b
      return a
  ```
- **Dataset implementations**:
  - Sorted: Monotonic LCG step increments.
  - Unsorted with repetition: LCG modulo range mapping.
  - Unsorted without repetition: Full-period modular affine bijection using custom GCD and LCG.

---

## ⏱️ Timing Infrastructure (`src/utils/timer.py`)

High-precision time profiling is implemented via Python's `time.perf_counter()`, which offers sub-microsecond resolution independent of system clock adjustments:

```python
from src.utils.timer import measure_time

with measure_time("100 Crore Integer Generation"):
    # Target operation here
    ...
```

---

## 🚀 How to Run the Generators

All commands are executed from the project root (`DSA-exp`):

### CLI Arguments
| Flag | Options | Default | Description |
| :--- | :--- | :--- | :--- |
| `--count` | Integer (e.g. `100000`, `10000000`, `1000000000`) | `100,000` | Number of integers to generate |
| `--method` | `with_random`, `without_random` | `with_random` | Generation engine to use |
| `--type` | `sorted`, `unsorted_rep`, `unsorted_no_rep`, `all` | `all` | Specific dataset or all datasets |
| `--chunk-size` | Integer | `1,000,000` | Batch size for buffered disk writes |

---

### Execution Examples

#### 1. Quick Test Run (1 Lakh = 100,000 integers)
Ideal for testing your code and logic in under a second:
```bash
# Using Python's random library
python src/generation/run_generator.py --count 100000 --method with_random

# Using Custom PRNG (without random library)
python src/generation/run_generator.py --count 100000 --method without_random
```

#### 2. Intermediate Scale (1 Crore = 10,000,000 integers)
Great for preliminary benchmarks before running the full billion:
```bash
python src/generation/run_generator.py --count 10000000 --method with_random
```

#### 3. Full Production Scale (100 Crore = 1,000,000,000 integers)
Generates all 3 datasets of 1 billion integers:
```bash
python src/generation/run_generator.py --count 1000000000 --method with_random
```

To generate only one specific dataset type at full scale:
```bash
# Only sorted
python src/generation/run_generator.py --count 1000000000 --type sorted

# Only unsorted with repetition
python src/generation/run_generator.py --count 1000000000 --type unsorted_rep

# Only unsorted without repetition
python src/generation/run_generator.py --count 1000000000 --type unsorted_no_rep
```

---

## 💾 Hardware & Disk Space Guidelines

> [!WARNING]
> **Disk Space Requirement for 1 Billion Integers**:
> - Each integer stored as ASCII text (e.g., 8–10 digits plus newline `\n`) takes roughly **9.5 to 11 GB per file**.
> - Generating all three full datasets requires **~30 GB to 33 GB of free disk space**.
> - Ensure your drive has sufficient free space before launching the full 100 crore generation.

---

## 🧪 Validation & Sanity Verification

You can verify that the generated data adheres strictly to specifications using this one-line Python check:

```bash
python -c "
with open('data/sorted.txt') as f:
    nums = [int(line) for _, line in zip(range(100000), f)]
    assert all(nums[i] <= nums[i+1] for i in range(len(nums)-1)), 'Sorted check failed'
print('Sorted check: PASSED')

with open('data/unsorted_repetition.txt') as f:
    nums = [int(line) for _, line in zip(range(100000), f)]
    print(f'Unsorted with repetition check: {len(nums)} numbers read, {len(set(nums))} unique values.')

with open('data/unsorted_no_repetition.txt') as f:
    nums = [int(line) for _, line in zip(range(100000), f)]
    assert len(nums) == len(set(nums)), 'Duplicates found!'
print('Unsorted without repetition check: PASSED (100% unique elements)')
"
```

---

## 🤝 Guide for Teammates

### For Member 2 (Searching):
* Place your searching scripts inside [`src/searching/`](file:///d:/Code/DSA-exp/src/searching).
* Use [`src/utils/file_io.py`](file:///d:/Code/DSA-exp/src/utils/file_io.py) (`load_sample_integers` or `stream_integers`) to read the datasets from `data/sorted.txt`, `data/unsorted_repetition.txt`, and `data/unsorted_no_repetition.txt`.
* Implement Binary Search for `sorted.txt` ($O(\log N)$) and Linear Search for unsorted datasets ($O(N)$).
* Benchmark and log the execution time differences.

### For Member 3 (Insertion):
* Place your insertion scripts inside [`src/insertion/`](file:///d:/Code/DSA-exp/src/insertion).
* Measure the execution times of:
  - Inserting at the beginning (shifts $N$ elements, $O(N)$).
  - Inserting at the end (amortized $O(1)$).
  - Inserting at a specified index $k$ (shifts $N - k$ elements, $O(N)$).
* Compare how execution time scales as $N$ grows.
