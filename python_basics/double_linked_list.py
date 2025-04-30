# Тесты в конце

from typing import Optional, Any


class Node:
    def __init__(self, value):
        self.value: Any = value
        self.prev_v: Optional[Node, None] = None
        self.next_v: Optional[Node, None] = None

    def __str__(self):
        return str(self.value)


class DoubleLinkedList:
    """
    This is Double Linked List

    DoubleLinkedList(*args)

    Methods:
        append(value): Adds value at the end.
        prepend(value): Adds value at the beginning.
        insert(value, index): Inserts value using index.
        delete(value): Deletes value.
        find(value): Searches value, returns index.
    """
    def __init__(self, *args):
        self.start: Optional[Node, None] = None

        if args:
            for arg in args:
                self.append(arg)

    def append(self, value):
        new_node = Node(value)

        if not self.start:
            self.start = new_node

        else:
            curr_node: Node = self.start
            while curr_node.next_v:
                curr_node = curr_node.next_v

            curr_node.next_v = new_node
            new_node.prev_v = curr_node

    def prepend(self, value):
        new_node = Node(value)

        if not self.start:
            self.start = new_node

        else:
            self.start.prev_v = new_node
            new_node.next_v = self.start
            self.start = new_node

    def insert(self, value, index):
        new_node = Node(value)

        if index == 0:
            new_node.next_v = self.start
            if self.start:
                self.start.prev_v = new_node
            self.start = new_node
            return

        else:
            curr_node: Node = self.start
            if curr_node is None:
                raise IndexError("Index out of range")

            for _ in range(index - 1):

                if curr_node is None:
                    raise IndexError("Index out of range")

                curr_node = curr_node.next_v

            new_node.next_v = curr_node.next_v
            new_node.prev_v = curr_node

            if curr_node.next_v:
                curr_node.next_v.prev_v = new_node

            curr_node.next_v = new_node

    def delete(self, value):

        if not self.start:
            raise IndexError("List is empty")

        else:
            curr_node: Node = self.start
            while curr_node.next_v:

                if curr_node.value == value:
                    if curr_node.prev_v:
                        curr_node.prev_v.next_v = curr_node.next_v
                    else:
                        self.start = curr_node.next_v

                    if curr_node.next_v:
                        curr_node.next_v.prev_v = curr_node.prev_v

                    del curr_node
                    return

                curr_node = curr_node.next_v

    def find(self, value):
        if not self.start:
            raise IndexError("List is empty")

        else:
            index_count = -1
            curr_node: Node = self.start
            while curr_node:
                index_count += 1

                if curr_node.value == value:
                    return index_count
                curr_node = curr_node.next_v

            return -1

    def __str__(self):
        curr_node: Node = self.start
        result_str = ""
        while curr_node:
            result_str += f"{str(curr_node)}, "
            curr_node = curr_node.next_v

        return result_str

    def __repr__(self):
        return "DoubleLinkedList(*args)"

    def __len__(self):
        curr_node: Node = self.start
        result_str = ""
        while curr_node:
            result_str += f"{str(curr_node)}"
            curr_node = curr_node.next_v

        return len(result_str)

    def __iter__(self):
        self.curr_node = self.start
        return self

    def __next__(self):

        if self.curr_node is None:
            raise StopIteration

        value = self.curr_node.value
        self.curr_node = self.curr_node.next_v
        return value


# Simple tests:
import unittest


class TestDoubleLinkedList(unittest.TestCase):
    def setUp(self):
        self.dll = DoubleLinkedList()

    def test_append(self):
        self.dll.append(1)
        self.dll.append(2)
        self.dll.append(3)

        self.assertEqual(str(self.dll), "1, 2, 3, ")

    def test_prepend(self):
        self.dll.prepend(1)
        self.dll.prepend(2)

        self.assertEqual(str(self.dll), "2, 1, ")

    def test_insert(self):
        self.dll.append(1)
        self.dll.append(3)
        self.dll.insert(2, 1)

        self.assertEqual(str(self.dll), "1, 2, 3, ")

    def test_delete(self):
        self.dll.append(1)
        self.dll.append(2)
        self.dll.append(3)

        self.dll.delete(2)
        self.assertEqual(str(self.dll), "1, 3, ")

    def test_find(self):
        self.dll.append(1)
        self.dll.append(2)
        self.dll.append(3)

        self.assertEqual(self.dll.find(2), 1)
        self.assertEqual(self.dll.find(3), 2)
        self.assertEqual(self.dll.find(4), -1)

        empty_list = DoubleLinkedList()
        with self.assertRaises(IndexError):
            empty_list.find(1)

    def test_len(self):
        self.dll.append(1)
        self.dll.append(2)
        self.dll.append(3)

        self.assertEqual(len(self.dll), 3)

    def test_iter(self):
        self.dll.append(1)
        self.dll.append(2)
        self.dll.append(3)

        values = [value for value in self.dll]
        self.assertEqual(values, [1, 2, 3])

    def test_create_list_with_args(self):
        new_dll = DoubleLinkedList(1, 2, 3)
        self.assertEqual(str(new_dll), "1, 2, 3, ")


if __name__ == "__main__":
    unittest.main()
