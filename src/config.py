"""Global configuration and paths for DSA benchmark experiment."""

from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Dataset Sizes
SIZE_TEST = 100_000             # 1 Lakh - Fast sanity tests
SIZE_MEDIUM = 10_000_000        # 1 Crore - Quick benchmarking
SIZE_1_BILLION = 1_000_000_000   # 100 Crore / 1 Billion integers

# Buffer chunk size for streaming disk I/O (avoids Out-Of-Memory)
CHUNK_SIZE = 1_000_000

# File Paths
PATH_SORTED = DATA_DIR / "sorted.txt"
PATH_UNSORTED_REP = DATA_DIR / "unsorted_repetition.txt"
PATH_UNSORTED_NO_REP = DATA_DIR / "unsorted_no_repetition.txt"
