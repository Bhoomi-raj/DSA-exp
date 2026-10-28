
import csv
import random
import time
from pathlib import Path

from src.searching.algorithms import linear_search, binary_search
from src.searching.linked_list import LinkedList

SAMPLE_SIZE = 100_000
TRIALS = 5


def measure(function, target):
    timings = []
    result = None

    for _ in range(TRIALS):
        start = time.perf_counter()
        result = function(target)
        timings.append((time.perf_counter() - start) * 1000)

    return result, sum(timings) / len(timings)


def benchmark_case(name, numbers, is_sorted=False):
    linked = LinkedList.from_iterable(numbers)

    algorithms = {
        "Array Linear": lambda x: linear_search(numbers, x),
        "Linked List Linear": linked.linear_search,
    }

    if is_sorted:
        algorithms["Array Binary"] = (
            lambda x: binary_search(numbers, x)
        )

    targets = [
        ("present", numbers[len(numbers) // 2]),
        ("absent", max(numbers) + 1),
    ]

    rows = []

    for target_type, target in targets:
        for algorithm_name, function in algorithms.items():
            result, avg_ms = measure(function, target)

            print(
                f"{name} | {algorithm_name} | "
                f"{target_type} | {avg_ms:.4f} ms"
            )

            rows.append({
                "case": name,
                "algorithm": algorithm_name,
                "target_type": target_type,
                "target": target,
                "elements": len(numbers),
                "found": result is not None,
                "average_ms": round(avg_ms, 6),
                "trials": TRIALS,
            })

    return rows


def main():
    rng = random.Random(42)
    n = SAMPLE_SIZE

    repeated = [rng.randint(1, n // 2) for _ in range(n)]
    unique = list(range(1, n + 1))
    rng.shuffle(unique)
    sorted_numbers = sorted(repeated)

    cases = [
        ("Sorted", sorted_numbers, True),
        ("Unsorted with repetition", repeated, False),
        ("Unsorted without repetition", unique, False),
    ]

    results = []

    for name, numbers, is_sorted in cases:
        results.extend(benchmark_case(name, numbers, is_sorted))

    output = Path("searching_results.csv")

    with output.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

    print(f"\nResults saved to: {output.resolve()}")


if __name__ == "__main__":
    main()
