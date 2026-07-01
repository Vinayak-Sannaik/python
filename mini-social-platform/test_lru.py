import unittest
from lru_cache import LRUCache

class TestLRUCache(unittest.TestCase):

    def test_put_and_get(self):
        cache = LRUCache(2)

        cache.put(1, "A")
        cache.put(2, "B")

        self.assertEqual(cache.get(1), "A")
        self.assertEqual(cache.get(2), "B")

    def test_eviction_order(self):
        cache = LRUCache(2)

        cache.put(1, "A")
        cache.put(2, "B")

        # Access key 1
        cache.get(1)

        # key 2 becomes LRU
        cache.put(3, "C")

        self.assertIsNone(cache.get(2))
        self.assertEqual(cache.get(1), "A")
        self.assertEqual(cache.get(3), "C")

    def test_update_existing_key(self):
        cache = LRUCache(2)

        cache.put(1, "A")
        cache.put(1, "AA")

        self.assertEqual(cache.get(1), "AA")

    def test_invalidate(self):
        cache = LRUCache(2)

        cache.put(1, "A")
        cache.put(2, "B")

        cache.invalidate(1)

        self.assertIsNone(cache.get(1))
        self.assertEqual(cache.get(2), "B")

    def test_multiple_evictions(self):
        cache = LRUCache(3)

        cache.put(1, "A")
        cache.put(2, "B")
        cache.put(3, "C")

        cache.get(1)
        cache.get(2)

        cache.put(4, "D")

        # 3 should be evicted
        self.assertIsNone(cache.get(3))

        cache.put(5, "E")

        # 1 should now be evicted
        self.assertIsNone(cache.get(1))

    def test_capacity_one(self):
        cache = LRUCache(1)

        cache.put(1, "A")
        cache.put(2, "B")

        self.assertIsNone(cache.get(1))
        self.assertEqual(cache.get(2), "B")

    def test_invalid_capacity(self):
        with self.assertRaises(ValueError):
            LRUCache(0)


if __name__ == "__main__":
    unittest.main()