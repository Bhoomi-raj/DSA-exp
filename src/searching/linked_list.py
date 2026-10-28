
class Node:
    def __init__(self, data: int):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def append(self, value: int) -> None:
        node = Node(value)

        if self.head is None:
            self.head = node
        else:
            self.tail.next = node

        self.tail = node
        self.size += 1

    @classmethod
    def from_iterable(cls, values):
        result = cls()
        for value in values:
            result.append(value)
        return result

    def linear_search(self, target: int) -> int | None:
        current = self.head
        index = 0

        while current is not None:
            if current.data == target:
                return index
            current = current.next
            index += 1

        return None
