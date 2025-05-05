# Отдельный класс итератор

# class MyIterator:
#     def __init__(self, data):
#         self._data = data
#         self._bucket_index = 0
#         self._inner_index = 0
#
#     def __iter__(self):
#         return self
#
#     def __next__(self):
#         while self._bucket_index < len(self._data):
#             bucket = self._data[self._bucket_index]
#             if self._inner_index < len(bucket):
#                 key = bucket[self._inner_index][0]
#                 self._inner_index += 1
#                 return key
#             else:
#                 self._bucket_index += 1
#                 self._inner_index = 0
#         raise StopIteration


class MyDict:
    def __init__(self, size=4):
        self._size = size
        self._data = [[] for _ in range(self._size)]
        self._count = 0

    def create_hash(self, key):
        return hash(key) % self._size

    def re_size_data(self):
        self._size *= 2
        new_data = [[] for _ in range(self._size)]

        for bucket in self._data:
            for k, v in bucket:
                index = self.create_hash(k)
                new_data[index].append((k, v))

        self._data = new_data

    def __setitem__(self, key, value):
        index = self.create_hash(key)

        bucket = self._data[index]
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return

        bucket.append((key, value))
        self._count += 1

        if self._count > self._size // 2:
            self.re_size_data()

    def __getitem__(self, item):
        index = self.create_hash(item)

        bucket = self._data[index]

        if len(bucket) == 1:
            return bucket[0][1]

        for i, (k, v) in enumerate(bucket):
            if k == item:
                return v

    def __contains__(self, key):
        index = self.create_hash(key)
        bucket = self._data[index]

        for k, _ in bucket:
            if k == key:
                return True
        return False

    def __delitem__(self, key):
        index = self.create_hash(key)
        bucket = self._data[index]

        for i, (k, v) in enumerate(bucket):
            if k == key:
                del bucket[i]
                self._count -= 1
                return
        raise KeyError(f'Key {key} not found')

    def __len__(self):
        return self._count

    # def __iter__(self):
    #     """ Для варианте где итератор это отдельный класс """
    #     return MyIterator(self._data)

    def __iter__(self):
        return self.keys()

    def get(self, key, default=None):
        index = self.create_hash(key)

        bucket = self._data[index]

        if len(bucket) == 1:
            return bucket[0][1]

        for i, (k, v) in enumerate(bucket):
            if k == key:
                return v

        return default

    def keys(self):
        for bucket in self._data:
            for key, _ in bucket:
                yield key

    def values(self):
        for bucket in self._data:
            for _, values in bucket:
                yield values

    def items(self):
        for bucket in self._data:
            for pair in bucket:
                yield pair


import unittest


class TestDoubleLinkedList(unittest.TestCase):
    def setUp(self):
        self.d = MyDict()

    def test_set_item(self):
        self.d[1] = 1
        self.d["1"] = "1"
        self.assertEqual(len(self.d), 2)

    def test_get_item(self):
        self.d[1] = 1
        self.assertEqual(self.d[1], 1)

    def test_iter(self):
        self.d[1] = 1
        self.d["1"] = "1"

        dd = [k for k in self.d]
        self.assertIsInstance(dd, list)

    def test_contains(self):
        self.d[2] = 1
        self.assertIn(2, self.d)
        self.assertNotIn(3, self.d)

    def test_get(self):
        self.d[1] = 1
        res = self.d.get(2, default=None)
        self.assertEqual(res, None)

    def test_keys(self):
        self.d[1] = "one"
        self.d["1"] = "string one"

        dd = [k for k in self.d.keys()]
        self.assertEqual(set(dd), {1, "1"})

    def test_values(self):
        self.d[1] = "one"
        self.d["1"] = "string one"

        dd = [k for k in self.d.values()]
        self.assertEqual(set(dd), {"one", "string one"})

    def test_items(self):
        self.d[1] = "one"
        self.d["1"] = "string one"

        dd = [k for k in self.d.items()]
        self.assertEqual(set(dd), {(1, "one"), ("1", "string one")})


