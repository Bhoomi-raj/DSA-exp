
def linear_search(arr: list[int], target: int) -> int | None:
    for index, value in enumerate(arr):
        if value == target:
            return index
    return None


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
