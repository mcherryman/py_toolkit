
# -*- coding: utf-8 -*-
"""
Suppress unit tests
"""
import sys
import unittest

# Append the current and parent directories to path so we can always find the module we want to test
map(lambda p : sys.path.append(p), [".", ".."])

# noinspection PyUnresolvedReferences,PyUnresolvedReferences
import suppress

class SuppressTest(unittest.TestCase):

    def test_01_suppressing_an_error_should_prevent_it_throwing(self):
        """Suppressing an error type should prevent it being raised"""
        with suppress.suppress(IOError):
            with open('blahblah'):
                raise Exception("FAIL: Somehow opened blahblah, why on earth does it exist!")

    def test_02_supressing_mulitple_errors_should_prevent_any_of_them_throwing(self):
        """Suppressing multiple error types should prevent them being raised"""
        with suppress.suppress(IOError, KeyError):
            with open('blahblah'):
                raise Exception("FAIL: Somehow opened blahblah, why on earth does it exist!")
            d = {}
            print(d['Bad key'])
            raise Exception("FAIL: Bad key exists....")

    def test_03_mulitple_suppressions_should_be_chainable_in_a_context(self):
        """Multiple supressions should be chainable in a with context"""
        with suppress.suppress(IOError), suppress.suppress(KeyError):
            with open('blahblah'):
                raise Exception("FAIL: Somehow opened blahblah, why on earth does it exist!")
            d = {}
            print(d['Bad key'])
            raise Exception("FAIL: Bad key exists....")

    def test_04_suppressing_an_error_should_not_suppress_an_error_of_another_type(self):
        """Suppressing an error of type A should not prevent an error of type B being raised"""
        def test_func():
            with suppress.suppress(KeyError):
                raise Exception("This is not a key error")
        with self.assertRaises(Exception):
            test_func()

if __name__ == "__main__":
    unittest.main(verbosity=5)