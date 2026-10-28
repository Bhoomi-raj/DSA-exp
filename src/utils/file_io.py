"""File utility functions for loading datasets efficiently."""

from pathlib import Path
from typing import Generator, List


def stream_integers(file_path: Path) -> Generator[int, None, None]:
    """Streams integers from a text file one line at a time to minimize memory usage."""
    with open(file_path, "r", encoding="ascii") as f:
        for line in f:
            stripped = line.strip()
            if stripped:
                yield int(stripped)


def load_sample_integers(file_path: Path, max_count: int = 1_000_000) -> List[int]:
    """Loads a bounded sample of integers into memory for quick benchmarking.

    Note: 1 billion integers in Python takes ~36 GB RAM, so loading a subset
    (e.g. 10 million) is recommended for memory-constrained machines.
    """
    sample = []
    with open(file_path, "r", encoding="ascii") as f:
        for line in f:
            stripped = line.strip()
            if stripped:
                sample.append(int(stripped))
                if len(sample) >= max_count:
                    break
    return sample
