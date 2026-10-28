"""Performance timing utilities."""

import time
from contextlib import contextmanager
from typing import Generator

@contextmanager
def measure_time(task_name: str = "Operation") -> Generator[None, None, None]:
    """Context manager to measure and print execution time with high precision."""
    start_time = time.perf_counter()
    try:
        yield
    finally:
        elapsed = time.perf_counter() - start_time
        print(f"[Timer] {task_name} completed in {elapsed:.4f} seconds ({elapsed / 60:.2f} mins)")
