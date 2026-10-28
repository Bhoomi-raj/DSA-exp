"""Data generation WITHOUT using the `random` library.

Implements a 64-bit Linear Congruential Generator (LCG) and modular coprime permutation
from first principles. Completely independent of Python's standard `random` module.
"""

from pathlib import Path


class CustomPRNG:
    """A 64-bit Linear Congruential Generator (LCG).

    Uses Donald Knuth's MMIX constants:
        a = 6364136223846793005
        c = 1442695040888963407
        m = 2^64
    """

    MASK_64 = 0xFFFFFFFFFFFFFFFF

    def __init__(self, seed: int = 123456789):
        # Ensure non-zero seed within 64-bit range
        self.state = (seed & self.MASK_64) or 1

    def next_uint64(self) -> int:
        """Returns the next pseudo-random 64-bit unsigned integer."""
        self.state = (self.state * 6364136223846793005 + 1442695040888963407) & self.MASK_64
        return self.state

    def randint(self, low: int, high: int) -> int:
        """Returns a pseudo-random integer in the range [low, high]."""
        if high <= low:
            return low
        span = (high - low) + 1
        return low + (self.next_uint64() % span)


def custom_gcd(a: int, b: int) -> int:
    """Euclidean algorithm to find greatest common divisor from scratch."""
    while b != 0:
        a, b = b, a % b
    return a


def generate_sorted_custom(
    output_path: Path,
    total_count: int,
    chunk_size: int = 1_000_000,
    seed: int = 123456789,
) -> None:
    """Generates a sorted integer dataset using a custom PRNG."""
    prng = CustomPRNG(seed)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    current_val = prng.randint(1, 10)
    written = 0

    with open(output_path, "w", buffering=32 * 1024 * 1024, encoding="ascii") as f:
        while written < total_count:
            batch_count = min(chunk_size, total_count - written)
            chunk = []
            for _ in range(batch_count):
                chunk.append(str(current_val))
                # Add positive pseudo-random delta (1 to 5)
                current_val += prng.randint(1, 5)

            f.write("\n".join(chunk) + "\n")
            written += batch_count
            print(f"[without_random] Sorted: {written:,} / {total_count:,} ({(written / total_count) * 100:.1f}%)", end="\r")

    print(f"\n[without_random] Finished sorted file -> {output_path}")


def generate_unsorted_repetition_custom(
    output_path: Path,
    total_count: int,
    chunk_size: int = 1_000_000,
    min_val: int = 1,
    max_val: int = 10_000_000,
    seed: int = 123456789,
) -> None:
    """Generates an unsorted dataset with duplicates using custom PRNG."""
    prng = CustomPRNG(seed)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    written = 0
    with open(output_path, "w", buffering=32 * 1024 * 1024, encoding="ascii") as f:
        while written < total_count:
            batch_count = min(chunk_size, total_count - written)
            chunk = [str(prng.randint(min_val, max_val)) for _ in range(batch_count)]
            f.write("\n".join(chunk) + "\n")
            written += batch_count
            print(f"[without_random] Unsorted (with rep): {written:,} / {total_count:,} ({(written / total_count) * 100:.1f}%)", end="\r")

    print(f"\n[without_random] Finished unsorted (with repetition) file -> {output_path}")


def generate_unsorted_no_repetition_custom(
    output_path: Path,
    total_count: int,
    chunk_size: int = 1_000_000,
    seed: int = 123456789,
) -> None:
    """Generates an unsorted dataset where every number from 1 to total_count is unique.

    Uses a full-period modular affine bijection:
        val = ((a * i + c) % total_count) + 1
    without importing math or random libraries.
    """
    prng = CustomPRNG(seed)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Find a coprime multiplier 'a' using our custom PRNG and custom GCD
    while True:
        candidate = prng.randint(3, total_count - 1)
        if custom_gcd(candidate, total_count) == 1:
            a = candidate
            break

    c = prng.randint(1, total_count - 1)

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
            print(f"[without_random] Unsorted (no rep): {written:,} / {total_count:,} ({(written / total_count) * 100:.1f}%)", end="\r")

    print(f"\n[without_random] Finished unsorted (without repetition) file -> {output_path}")
