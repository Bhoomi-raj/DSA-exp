"""Command-line runner to generate datasets for the DSA project.

Supports:
- Sorted integers
- Unsorted integers with repetition
- Unsorted integers without repetition
Both with Python's `random` module and with custom PRNG (without `random`).
"""

import argparse
import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.config import (
    PATH_SORTED,
    PATH_UNSORTED_REP,
    PATH_UNSORTED_NO_REP,
    CHUNK_SIZE,
    SIZE_1_BILLION,
    SIZE_MEDIUM,
    SIZE_TEST,
)
from src.utils.timer import measure_time
from src.generation.with_random import (
    generate_sorted_random,
    generate_unsorted_repetition_random,
    generate_unsorted_no_repetition_random,
)
from src.generation.without_random import (
    generate_sorted_custom,
    generate_unsorted_repetition_custom,
    generate_unsorted_no_repetition_custom,
)


def run():
    parser = argparse.ArgumentParser(description="Dataset Generator for 100 Crore (1 Billion) Integers")
    parser.add_argument(
        "--type",
        choices=["sorted", "unsorted_rep", "unsorted_no_rep", "all"],
        default="all",
        help="Type of integer dataset to generate (default: all)",
    )
    parser.add_argument(
        "--method",
        choices=["with_random", "without_random"],
        default="with_random",
        help="Use built-in random library or custom PRNG without random (default: with_random)",
    )
    parser.add_argument(
        "--count",
        type=int,
        default=SIZE_TEST,
        help=f"Number of integers to generate. E.g. {SIZE_TEST:,} (test), {SIZE_MEDIUM:,} (medium), {SIZE_1_BILLION:,} (100 crore / 1 billion). Default: {SIZE_TEST:,}",
    )
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=CHUNK_SIZE,
        help=f"Streaming chunk size to keep memory usage low (default: {CHUNK_SIZE:,})",
    )

    args = parser.parse_args()

    print("=" * 60)
    print("           DSA DATASET GENERATION PIPELINE")
    print("=" * 60)
    print(f" Target Count : {args.count:,} integers")
    print(f" Method       : {args.method}")
    print(f" Generation   : {args.type}")
    print(f" Chunk Size   : {args.chunk_size:,}")
    print("=" * 60)

    use_custom = args.method == "without_random"

    # 1. Sorted
    if args.type in ("sorted", "all"):
        print(f"\n[1/3] Generating Sorted Integers ({args.count:,})...")
        with measure_time("Sorted Generation"):
            if use_custom:
                generate_sorted_custom(PATH_SORTED, args.count, args.chunk_size)
            else:
                generate_sorted_random(PATH_SORTED, args.count, args.chunk_size)

    # 2. Unsorted with repetition
    if args.type in ("unsorted_rep", "all"):
        print(f"\n[2/3] Generating Unsorted with Repetition ({args.count:,})...")
        with measure_time("Unsorted with Repetition Generation"):
            if use_custom:
                generate_unsorted_repetition_custom(PATH_UNSORTED_REP, args.count, args.chunk_size)
            else:
                generate_unsorted_repetition_random(PATH_UNSORTED_REP, args.count, args.chunk_size)

    # 3. Unsorted without repetition
    if args.type in ("unsorted_no_rep", "all"):
        print(f"\n[3/3] Generating Unsorted without Repetition ({args.count:,})...")
        with measure_time("Unsorted without Repetition Generation"):
            if use_custom:
                generate_unsorted_no_repetition_custom(PATH_UNSORTED_NO_REP, args.count, args.chunk_size)
            else:
                generate_unsorted_no_repetition_random(PATH_UNSORTED_NO_REP, args.count, args.chunk_size)

    print("\n" + "=" * 60)
    print("Generation complete! Output files in:", PATH_SORTED.parent)
    print("=" * 60)


if __name__ == "__main__":
    run()
