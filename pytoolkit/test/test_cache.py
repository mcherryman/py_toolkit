# -*- coding: utf-8 -*-
"""
Cache unit tests
"""
import sys
import time
import unittest

# Append the current and parent directories to path so we can always find the module we want to test
map(lambda p : sys.path.append(p), [".", ".."])
# noinspection PyUnresolvedReferences,PyUnresolvedReferences
import cache

class CacheTest(unittest.TestCase):

    EXPIRY_TIME = 2.0
    PRUNE_INTERVAL = 10.0

    def get_test_cache(self, extend_on_read):
        class TestCache(cache.Cache):
            def __init__(self):
                super(TestCache, self).__init__(expiry_time_secs=CacheTest.EXPIRY_TIME,
                                                refresh_expiry_on_read=extend_on_read,
                                                prune_interval=CacheTest.PRUNE_INTERVAL)
                self.miss_counter = 0

            def on_miss(self, key):
                self.miss_counter += 1
                return key
        return TestCache()

    def test_01_cache_miss_should_invoke_onmiss(self):
        """A cache miss should invoke on_miss"""
        cache = self.get_test_cache(False)
        self.assertEquals(cache.miss_counter, 0)
        cache.lookup("key_1")
        self.assertEqual(cache.miss_counter, 1)

    def test_02_cache_hit_should_not_invoke_onmiss(self):
        """A cache hit should not invoke on_miss"""
        cache = self.get_test_cache(False)
        self.assertEquals(cache.miss_counter, 0)
        cache.lookup("key_1")
        self.assertEqual(cache.miss_counter, 1)
        cache.lookup("key_1")
        self.assertEqual(cache.miss_counter, 1)

    def test_03_cache_entry_should_expire_after_expiry_time(self):
        """A cache entry should expire after the expiry time"""
        cache = self.get_test_cache(False)
        self.assertEquals(cache.miss_counter, 0)
        cache.lookup("key_1")
        self.assertEqual(cache.miss_counter, 1)
        time.sleep(CacheTest.EXPIRY_TIME+1)
        cache.lookup("key_1")
        self.assertEqual(cache.miss_counter, 2)

    def test_04_cache_entry_should_not_expire_if_refresh_expiry_on_read_specified(self):
        """A cache entry should extend it's expiry time if refresh on read is enabled"""
        cache = self.get_test_cache(True)
        self.assertEquals(cache.miss_counter, 0)
        cache.lookup("key_1")
        self.assertEqual(cache.miss_counter, 1)
        time.sleep(CacheTest.EXPIRY_TIME/2.0)
        cache.lookup("key_1")
        self.assertEqual(cache.miss_counter, 1)
        time.sleep(CacheTest.EXPIRY_TIME / 2.0)
        cache.lookup("key_1")
        self.assertEqual(cache.miss_counter, 1)
        time.sleep(CacheTest.EXPIRY_TIME)
        cache.lookup("key_1")
        self.assertEqual(cache.miss_counter, 2)

    def test_05_cache_entry_should_be_removed_after_pruning_if_not_read(self):
        """A cache entry should be removed by the pruning thread if it is expired"""
        cache = self.get_test_cache(False)
        self.assertEquals(cache.miss_counter, 0)
        cache.lookup("key_1")
        self.assertEqual(len(cache), 1)
        time.sleep(CacheTest.PRUNE_INTERVAL+1)
        self.assertEqual(len(cache), 0)

    def test_06_cache_entry_should_not_be_removed_after_pruning_if_not_expired(self):
        """A cache entry should not be removed by the pruning thread if it is not expired"""
        cache = self.get_test_cache(False)
        self.assertEquals(cache.miss_counter, 0)
        time.sleep(CacheTest.PRUNE_INTERVAL-1)
        cache.lookup("key_1")
        self.assertEqual(len(cache), 1)
        time.sleep(1)
        self.assertEqual(len(cache), 1)

    def test_07_cache_entry_should_be_removed_if_dropped(self):
        """Cache entries should be removed if dropped."""
        cache = self.get_test_cache(False)
        self.assertEquals(cache.miss_counter, 0)
        cache.lookup("key_1")
        cache.lookup("key_2")
        self.assertEqual(len(cache), 2)
        cache.drop("key_1")
        self.assertEqual(len(cache), 1)
        cache.drop("key_2")
        self.assertEqual(len(cache), 0)

    def test_08_dropping_a_missing_key_should_not_raise(self):
        """Dropping a missing key should not raise an exception"""
        cache = self.get_test_cache(False)
        cache.drop("key_1")


if __name__ == "__main__":
    unittest.main(verbosity=5)