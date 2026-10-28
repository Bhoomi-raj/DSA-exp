"""Data generation using Python's built-in `random` module.

Optimized for memory-efficient streaming to handle up to 100 crore (1 billion) integers.
"""

import math
import random
from pathlib import Path
from typing import Optional


def generate_sorted_random(
    output_path: Path,
    total_count: int,
    chunk_size: int = 1_000_000,
    seed: Optional[int] = 42,
) -> None:
    """Generates a sorted sequence of integers with random positive steps.

    Uses O(1) auxiliary memory via chunked streaming writes.
    """
    if seed is not None:
        random.seed(seed)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    current_val = random.randint(1, 10)

    written = 0
    with open(output_path, "w", buffering=32 * 1024 * 1024, encoding="ascii") as f:
        while written < total_count:
            batch_count = min(chunk_size, total_count - written)
            chunk = []
            for _ in range(batch_count):
                chunk.append(str(current_val))
                # Add random delta (1 to 5) so numbers strictly or monotonically increase
                current_val += random.randint(1, 5)

            f.write("\n".join(chunk) + "\n")
            written += batch_count
            print(f"[with_random] Sorted: {written:,} / {total_count:,} ({(written / total_count) * 100:.1f}%)", end="\r")

    print(f"\n[with_random] Finished sorted file -> {output_path}")


def generate_unsorted_repetition_random(
    output_path: Path,
    total_count: int,
    chunk_size: int = 1_000_000,
    min_val: int = 1,
    max_val: int = 10_000_000,
    seed: Optional[int] = 42,
) -> None:
    """Generates an unsorted sequence with duplicate values allowed.

    Range [min_val, max_val] defaults to 10 million so repetitions naturally occur.
    """
    if seed is not None:
        random.seed(seed)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    randint = random.randint

    written = 0
    with open(output_path, "w", buffering=32 * 1024 * 1024, encoding="ascii") as f:
        while written < total_count:
            batch_count = min(chunk_size, total_count - written)
            chunk = [str(randint(min_val, max_val)) for _ in range(batch_count)]
            f.write("\n".join(chunk) + "\n")
            written += batch_count
            print(f"[with_random] Unsorted (with rep): {written:,} / {total_count:,} ({(written / total_count) * 100:.1f}%)", end="\r")

    print(f"\n[with_random] Finished unsorted (with repetition) file -> {output_path}")


def _find_random_coprime(n: int) -> int:
    """Finds a random integer 'a' such that gcd(a, n) == 1."""
    while True:
        candidate = random.randint(3, n - 1)
        if math.gcd(candidate, n) == 1:
            return candidate


def generate_unsorted_no_repetition_random(
    output_path: Path,
    total_count: int,
    chunk_size: int = 1_000_000,
    seed: Optional[int] = 42,
) -> None:
    """Generates an unsorted sequence where every integer from 1 to total_count appears exactly once.

    Uses a pseudo-random modular affine permutation:
        f(i) = (a * i + c) mod total_count + 1
    where gcd(a, total_count) == 1.
    This guarantees 100% uniqueness in O(1) memory, allowing 1 billion unique integers
    without running out of RAM (which would crash standard shuffle/set approaches).
    """
    if seed is not None:
        random.seed(seed)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Pick random coprime 'a' and offset 'c' using the random library
    a = _find_random_coprime(total_count)
    c = random.randint(1, total_count - 1)

    written = 0
    with open(output_path, "w", buffering=32 * 1024 * 1024, encoding="ascii") as f:
        while written < total_count:
            batch_count = min(chunk_size, total_count - written)
            chunk = []
            for i in range(written, written + batch_count):
                val = ((a * i + c) % total_count) + 1
                chunk.append(str(val))

            f.write("\n".join(chunk) + "\n")
            written += batch_count
            print(f"[with_random] Unsorted (no rep): {written:,} / {total_count:,} ({(written / total_count) * 100:.1f}%)", end="\r")

    print(f"\n[with_random] Finished unsorted (without repetition) file -> {output_path}")
