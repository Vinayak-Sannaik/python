import unittest
from lfu_cache import LFUCache


class TestLFUCache(unittest.TestCase):

    def test_put_get(self):
        cache = LFUCache(2)

        cache.put(1, "A")
        cache.put(2, "B")

        self.assertEqual(cache.get(1), "A")
        self.assertEqual(cache.get(2), "B")

    def test_frequency_eviction(self):
        cache = LFUCache(2)

        cache.put(1, "A")
        cache.put(2, "B")

        cache.get(1)
        cache.get(1)

        cache.put(3, "C")

        self.assertEqual(cache.get(1), "A")
        self.assertIsNone(cache.get(2))
        self.assertEqual(cache.get(3), "C")

    def test_update_existing(self):
        cache = LFUCache(2)

        cache.put(1, "A")
        cache.put(1, "AA")

        self.assertEqual(cache.get(1), "AA")

    def test_invalidate(self):
        cache = LFUCache(2)

        cache.put(1, "A")
        cache.put(2, "B")

        cache.invalidate(1)

        self.assertIsNone(cache.get(1))
        self.assertEqual(cache.get(2), "B")

    def test_capacity_one(self):
        cache = LFUCache(1)

        cache.put(1, "A")
        cache.put(2, "B")

        self.assertIsNone(cache.get(1))
        self.assertEqual(cache.get(2), "B")

    def test_multiple_frequency_changes(self):
        cache = LFUCache(3)

        cache.put(1, "A")
        cache.put(2, "B")
        cache.put(3, "C")

        cache.get(1)
        cache.get(1)

        cache.get(2)

        cache.put(4, "D")

        self.assertIsNone(cache.get(3))
        self.assertEqual(cache.get(1), "A")
        self.assertEqual(cache.get(2), "B")
        self.assertEqual(cache.get(4), "D")

    def test_get_missing_key(self):
        cache = LFUCache(2)

        self.assertIsNone(cache.get(100))

    def test_invalid_capacity(self):
        with self.assertRaises(ValueError):
            LFUCache(0)


if __name__ == "__main__":
    unittest.main()