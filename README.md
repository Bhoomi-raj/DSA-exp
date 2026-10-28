# DSA Experiment: 100 Crore (1 Billion) Integers Analysis

A comprehensive performance analysis study comparing generation, searching, and insertion operations across massive integer datasets (up to 1,000,000,000 integers).

---

## 📌 Table of Contents
1. [Academic Problem Statement](#-academic-problem-statement)
2. [Team Work Distribution](#-team-work-distribution)
3. [Repository & Folder Architecture](#-repository--folder-architecture)
4. [Theoretical Complexity Analysis](#-theoretical-complexity-analysis)
5. [Generation Technical Design & Code](#-generation-technical-design--code)
   - [Memory Challenge & $O(1)$ Streaming](#1-memory-challenge--o1-streaming-architecture)
   - [Method 1: With Python `random`](#2-method-1-using-pythons-random-library-with_randompy)
   - [Method 2: Without `random` (Custom PRNG)](#3-method-2-without-random-library-without_randompy)
6. [Timer & Benchmarking Infrastructure](#-timer--benchmarking-infrastructure)
7. [CLI Execution Guide & Examples](#-cli-execution-guide--examples)
8. [Hardware & Storage Requirements](#-hardware--storage-requirements)
9. [Sanity & Validation Checks](#-sanity--validation-checks)
10. [Guides & Starter Templates for Teammates](#-guides--starter-templates-for-teammates)
11. [Git Collaboration Workflow](#-git-collaboration-workflow-for-the-team)

---

## 📋 Academic Problem Statement

> **Question:**
> Write a Python program to generate 100 crore (1 billion) integers and store them in a text file. Perform the following operations on the generated data:
>
> **1. Searching Operations**
> - Search in a sorted array.
> - Search in an unsorted array with repetition.
> - Search in an unsorted array without repetition.
>
> **2. Insertion Operations**
> - Insert an element at the beginning of an array.
> - Insert an element at the end of an array.
> - Insert an element at any specified position in an array.
>
> Analyze and compare the execution times of the searching and insertion operations.

---

## 👥 Team Work Distribution

| Member | Module Directory | Responsibility | Status |
| :--- | :--- | :--- | :--- |
| **Member 1 (You)** | `src/generation/`<br>`src/utils/` | Dataset generation (Sorted, Unsorted with repetition, Unsorted without repetition) with and without Python's `random` library; file I/O optimization; timing infrastructure. | **Complete** ✅ |
| **Member 2** | `src/searching/` | Searching algorithms (Binary Search on sorted, Linear Search on unsorted with/without repetition) and benchmark execution times. | *Pending Teammate* ⏳ |
| **Member 3** | `src/insertion/` | Array insertion algorithms (beginning, end, arbitrary index) and benchmark execution times. | *Pending Teammate* ⏳ |

---

## 📁 Repository & Folder Architecture

```text
DSA-exp/
├── data/                               # Generated .txt dataset files (git-ignored)
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

## 📊 Theoretical Complexity Analysis

### 1. Generation Complexity
| Dataset Type | Time Complexity | Auxiliary Space Complexity | Method Description |
| :--- | :---: | :---: | :--- |
| **Sorted** | $O(N)$ | $O(1)$ | Streaming monotonic increments. |
| **Unsorted with Repetition** | $O(N)$ | $O(1)$ | Bounded pseudo-random range sampling. |
| **Unsorted without Repetition** | $O(N)$ | $O(1)$ | Full-period modular affine bijection $((a \cdot i + c) \pmod N) + 1$. |

### 2. Searching Operations Complexity (Teammate 2)
| Operation | Target Dataset | Algorithm | Best Case | Average Case | Worst Case | Space |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| Search in Sorted Array | `sorted.txt` | **Binary Search** | $O(1)$ | $O(\log N)$ | $O(\log N)$ | $O(1)$ |
| Search in Unsorted Array (with Repetition) | `unsorted_repetition.txt` | **Linear Search** | $O(1)$ | $O(N)$ | $O(N)$ | $O(1)$ |
| Search in Unsorted Array (without Repetition) | `unsorted_no_repetition.txt` | **Linear Search** | $O(1)$ | $O(N)$ | $O(N)$ | $O(1)$ |

### 3. Insertion Operations Complexity (Teammate 3)
| Operation | Implementation | Time Complexity | Reason |
| :--- | :---: | :---: | :--- |
| **Insert at Beginning** | `arr.insert(0, val)` | $O(N)$ | Must shift all $N$ existing elements right by 1 position. |
| **Insert at End** | `arr.append(val)` | $O(1)$ (amortized) | Elements appended to the tail of dynamic array. |
| **Insert at Index $k$** | `arr.insert(k, val)` | $O(N - k)$ | Must shift $(N - k)$ remaining elements right by 1 position. |

---

## 🔬 Generation Technical Design & Code

### 1. Memory Challenge & $O(1)$ Streaming Architecture
- **The Problem**: Storing 1,000,000,000 integers in a Python list requires **~36 GB of RAM** ($28\text{ bytes per int} + 8\text{ bytes per pointer}$). Standard machines will crash with `MemoryError`.
- **The Solution**: All generators stream data directly to disk in **buffered chunks** (`1,000,000` numbers per flush).
- **RAM Footprint**: Under **50 MB**, regardless of whether you generate 100 thousand or 1 billion integers.

---

### 2. Method 1: Using Python's `random` Library (`with_random.py`)

#### A. Sorted Generation
```python
current_val = random.randint(1, 10)
for _ in range(batch_count):
    chunk.append(str(current_val))
    current_val += random.randint(1, 5)  # Monotonic positive step
```

#### B. Unsorted with Repetition
```python
# Range [min_val, max_val] defaults to 10,000,000 so duplicates naturally occur
chunk = [str(random.randint(min_val, max_val)) for _ in range(batch_count)]
```

#### C. Unsorted without Repetition ($O(1)$ Memory Bijective Permutation)
```python
# Mathematically guaranteed complete bijection of {1, ..., N} with zero duplicates
# a is coprime to N: gcd(a, N) == 1
for i in range(written, written + batch_count):
    val = ((a * i + c) % total_count) + 1
    chunk.append(str(val))
```

---

### 3. Method 2: Without `random` Library (`without_random.py`)

Completely self-contained implementation with **zero external or standard math/random library imports**:

#### A. 64-bit Linear Congruential Generator (LCG)
Implemented using Donald Knuth's MMIX constants:
$$X_{n+1} = (a \cdot X_n + c) \pmod{2^{64}}$$
```python
class CustomPRNG:
    MASK_64 = 0xFFFFFFFFFFFFFFFF

    def __init__(self, seed: int = 123456789):
        self.state = (seed & self.MASK_64) or 1

    def next_uint64(self) -> int:
        self.state = (self.state * 6364136223846793005 + 1442695040888963407) & self.MASK_64
        return self.state

    def randint(self, low: int, high: int) -> int:
        if high <= low:
            return low
        return low + (self.next_uint64() % ((high - low) + 1))
```

#### B. Custom Euclidean GCD
```python
def custom_gcd(a: int, b: int) -> int:
    while b != 0:
        a, b = b, a % b
    return a
```

---

## ⏱️ Timer & Benchmarking Infrastructure

High-precision profiling is implemented in `src/utils/timer.py` using `time.perf_counter()` (sub-microsecond accuracy independent of system time adjustments):

```python
import time
from contextlib import contextmanager

@contextmanager
def measure_time(task_name: str = "Operation"):
    start_time = time.perf_counter()
    try:
        yield
    finally:
        elapsed = time.perf_counter() - start_time
        print(f"[Timer] {task_name} completed in {elapsed:.4f} seconds ({elapsed / 60:.2f} mins)")
```

---

## 🚀 CLI Execution Guide & Examples

All commands are run from the project root (`DSA-exp`):

### CLI Argument Reference
| Flag | Options | Default | Description |
| :--- | :--- | :--- | :--- |
| `--count` | Integer | `100,000` | Number of integers to generate |
| `--method` | `with_random`, `without_random` | `with_random` | Generator engine |
| `--type` | `sorted`, `unsorted_rep`, `unsorted_no_rep`, `all` | `all` | Specific dataset or all 3 |
| `--chunk-size` | Integer | `1,000,000` | Flush chunk size for disk I/O |

---

### Command Examples

#### 1. Quick Test Run (1 Lakh = 100,000 integers)
Runs in fractions of a second for quick development checks:
```bash
# Using Python's random library
python src/generation/run_generator.py --count 100000 --method with_random

# Using Custom PRNG (without random library)
python src/generation/run_generator.py --count 100000 --method without_random
```

#### 2. Intermediate Scale (1 Crore = 10,000,000 integers)
Ideal for benchmarking searching and insertion before full-scale tests:
```bash
python src/generation/run_generator.py --count 10000000 --method with_random
```

#### 3. Full Production Scale (100 Crore = 1,000,000,000 integers)
```bash
# Generate all three 1-billion integer files
python src/generation/run_generator.py --count 1000000000 --method with_random

# Or generate them individually as disk space allows:
python src/generation/run_generator.py --count 1000000000 --type sorted
python src/generation/run_generator.py --count 1000000000 --type unsorted_rep
python src/generation/run_generator.py --count 1000000000 --type unsorted_no_rep
```

---

## 💾 Hardware & Storage Requirements

> [!WARNING]
> **Disk Space Notice for 1 Billion Integers**:
> - Each integer stored as ASCII text (`8` to `10` digits plus newline `\n`) takes **~9.5 to 11 GB per file**.
> - Generating all three full datasets requires **~30 GB to 33 GB of free disk space**.
> - Ensure your target drive has adequate storage before running the full 100 crore generation.

---

## 🧪 Sanity & Validation Checks

Run this command from your terminal to verify data integrity:

```bash
python -c "
with open('data/sorted.txt') as f:
    nums = [int(line) for _, line in zip(range(100000), f)]
    assert all(nums[i] <= nums[i+1] for i in range(len(nums)-1)), 'Sorted check failed'
print('Sorted check: PASSED (Monotonically increasing)')

with open('data/unsorted_repetition.txt') as f:
    nums = [int(line) for _, line in zip(range(100000), f)]
    print(f'Unsorted with repetition check: {len(nums):,} numbers read, {len(set(nums)):,} unique values.')

with open('data/unsorted_no_repetition.txt') as f:
    nums = [int(line) for _, line in zip(range(100000), f)]
    assert len(nums) == len(set(nums)), 'Duplicates found in no_repetition file!'
print('Unsorted without repetition check: PASSED (100% unique elements)')
"
```

---

## 🤝 Guides & Starter Templates for Teammates

### Member 2: Searching Operations
Place your code in [`src/searching/`](src/searching).

#### Reading Data
```python
from src.utils.file_io import load_sample_integers
from src.config import PATH_SORTED, PATH_UNSORTED_REP, PATH_UNSORTED_NO_REP

# Loads a manageable sample (e.g. 1 million ints) to test algorithms in memory
sorted_arr = load_sample_integers(PATH_SORTED, max_count=1_000_000)
```

#### Algorithms to Implement:
1. **Binary Search**:
   ```python
   def binary_search(arr: list[int], target: int) -> int | None:
       low, high = 0, len(arr) - 1
       while low <= high:
           mid = (low + high) // 2
           if arr[mid] == target:
               return mid
           elif arr[mid] < target:
               low = mid + 1
           else:
               high = mid - 1
       return None
   ```
2. **Linear Search**:
   ```python
   def linear_search(arr: list[int], target: int) -> int | None:
       for idx, val in enumerate(arr):
           if val == target:
               return idx
       return None
   ```

---

### Member 3: Insertion Operations
Place your code in [`src/insertion/`](src/insertion).

#### Operations to Benchmark:
```python
# 1. Insert at Beginning (O(N) - shifts all elements)
arr.insert(0, new_val)

# 2. Insert at End (O(1) amortized append)
arr.append(new_val)

# 3. Insert at Specified Position k (O(N - k) - shifts trailing elements)
arr.insert(k, new_val)
```

Use `measure_time()` from [`src/utils/timer.py`](src/utils/timer.py) to measure execution times for each and create a comparative graph/table.

---

## 🐙 Git Collaboration Workflow for the Team

```bash
# 1. Pull the latest code from main
git pull origin main

# 2. Create your own feature branch
git checkout -b feature/searching    # For Member 2
git checkout -b feature/insertion    # For Member 3

# 3. Add your implementation in your respective folder
# Member 2 works in src/searching/
# Member 3 works in src/insertion/

# 4. Stage, commit, and push your branch
git add src/
git commit -m "Implement searching algorithms and benchmarks"
git push origin feature/searching

# 5. Open a Pull Request on GitHub to merge into main
```
