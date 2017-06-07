# -*- coding: utf-8 -*-

"""
AtomicInt unit tests
"""

import sys
import math
import unittest

# Append the current and parent directories to path so we can always find the module we want to test
map(lambda p: sys.path.append(p), [".", ".."])

# noinspection PyUnresolvedReferences,PyUnresolvedReferences
import atomic


class AtomicIntTest(unittest.TestCase):
    def test_01_incrementing_should_increase_value_by_one(self):
        """ Incrementing should increase value by one"""
        a = atomic.AtomicInt()
        self.assertEquals(a.value, 0)
        atomic.increment(a)
        self.assertEquals(a.value, 1)
        atomic.increment(a)
        atomic.increment(a)
        self.assertEquals(a.value, 3)

    def test_02_decrementing_should_decrease_value_by_one(self):
        """ Decrementing should decrease value by one """
        a = atomic.AtomicInt()
        self.assertEquals(a.value, 0)
        atomic.decrement(a)
        self.assertEquals(a.value, -1)
        atomic.decrement(a)
        atomic.decrement(a)
        self.assertEquals(a.value, -3)

    def test_03_incrmenting_a_non_atomic_int_asserts(self):
        """ Incrementing a type other than AtomicInt should raise an AssertionError """
        with self.assertRaises(AssertionError):
            atomic.increment(0)

    def test_04_decrementing_a_non_atomic_int_asserts(self):
        """ Decrementing a type other than AtomicInt should raise an AssertionError """
        with self.assertRaises(AssertionError):
            atomic.decrement(0)

    def test_05_initialising_an_atomic_int_should_have_the_correct_value(self):
        a = atomic.AtomicInt(5)
        self.assertEquals(a.value, 5)

    def test_06_adding_an_integer_should_calculate_correctly(self):
        """ Adding an integer value should perform addition """
        a = atomic.AtomicInt(5)
        self.assertEquals(a.value, 5)
        a += 5
        self.assertEquals(a.value, 10)
        b = atomic.AtomicInt(3)
        self.assertEquals(b.value, 3)
        c = b + 7l
        self.assertIsInstance(c, atomic.AtomicInt)
        self.assertEquals(c, 10)

    def test_07_adding_two_atomic_ints_should_calculate_correctly(self):
        """ Adding an AtomicInt should perform addition """
        a = atomic.AtomicInt(5)
        b = atomic.AtomicInt(5)
        c = a + b
        self.assertIsInstance(c, atomic.AtomicInt)
        self.assertEquals(c, 10)
        self.assertEquals(5 + c, 15)
        self.assertEquals(5l + c, 15)

    def test_08_subtracting_an_integer_should_calculate_correctly(self):
        """ Subtracting an integer value should perform subtraction """
        a = atomic.AtomicInt(5)
        self.assertEquals(a.value, 5)
        a -= 5
        self.assertEquals(a.value, 0)
        b = atomic.AtomicInt(7)
        self.assertEquals(b.value, 7)
        c = b - 3l
        self.assertIsInstance(c, atomic.AtomicInt)
        self.assertEquals(c, 4)
        self.assertEquals(5 - c, 1)
        self.assertEquals(5l - c, 1)

    def test_09_subtracting_two_atomic_ints_should_calculate_correctly(self):
        """ Subtracting an integer value should perform subtraction """
        a = atomic.AtomicInt(5)
        b = atomic.AtomicInt(5)
        c = a * b
        self.assertIsInstance(c, atomic.AtomicInt)
        self.assertEquals(c, 25)

    def test_10_multiplying_an_integer_should_calculate_correctly(self):
        """ Multiplying an integer value should perform multiplication """
        a = atomic.AtomicInt(5)
        self.assertEquals(a.value, 5)
        a *= 5
        self.assertEquals(a.value, 25)
        b = atomic.AtomicInt(7)
        self.assertEquals(b.value, 7)
        c = b * 3l
        self.assertIsInstance(c, atomic.AtomicInt)
        self.assertEquals(c, 21)
        self.assertEquals(5 * c, 105)
        self.assertEquals(5l * c, 105)

    def test_11_multiplying_two_atomic_ints_should_calculate_correctly(self):
        """ Multiplying an integer value should perform multiplication """
        a = atomic.AtomicInt(5)
        b = atomic.AtomicInt(5)
        c = a * b
        self.assertIsInstance(c, atomic.AtomicInt)
        self.assertEquals(c, 25)

    def test_12_dividing_an_integer_should_calculate_correctly(self):
        """ Dividing an integer value should perform integer division """
        a = atomic.AtomicInt(5)
        self.assertEquals(a.value, 5)
        a /= 5
        self.assertEquals(a.value, 1)
        b = atomic.AtomicInt(7)
        self.assertEquals(b.value, 7)
        c = b / 3l
        self.assertIsInstance(c, atomic.AtomicInt)
        self.assertEquals(c, 2)
        self.assertEquals(6 / c, 3)
        self.assertEquals(6l / c, 3)

    def test_13_dividing_two_atomic_ints_should_calculate_correctly(self):
        """ Dividing an integer value should perform integer division """
        a = atomic.AtomicInt(5)
        b = atomic.AtomicInt(5)
        c = a / b
        self.assertIsInstance(c, atomic.AtomicInt)
        self.assertEquals(c, 1)

    def test_14_modulo_can_be_performed_with_an_atomic_int(self):
        """ Modulo should perform correctly with an AtomicInt """
        a = atomic.AtomicInt(5)
        self.assertEquals(a % 4, 1)
        self.assertEquals(6 % a, 1)

    def test_15_abs_should_work_with_an_atomic_int(self):
        """ Abs should work with an atomic int """
        a = atomic.AtomicInt(-5)
        self.assertEquals(abs(a), 5)
        self.assertIsInstance(abs(a), atomic.AtomicInt)

    def test_16_pow_should_work_with_an_atomic_int(self):
        """ Pow should work with an atomic int """
        a = atomic.AtomicInt(5)
        self.assertEquals(pow(a, 2), 25)
        self.assertIsInstance(pow(a, 2), atomic.AtomicInt)
        self.assertEquals(a ** 2, 25)
        a **= 2
        self.assertEquals(a, 25)

    def test_17_atomic_int_should_convert_to_other_numeric_types(self):
        """ AtomicInt can be converted to other numeric types"""
        a = atomic.AtomicInt(0)
        self.assertIsInstance(int(a), int)
        self.assertIsInstance(long(a), long)
        self.assertIsInstance(float(a), float)
        self.assertIsInstance(complex(a), complex)

    def test_18_atomic_int_is_convertible_to_hex_and_oct(self):
        """ AtomicInt can be converted to oct and hex"""
        a = atomic.AtomicInt(255)
        self.assertEquals(hex(a), hex(255))
        self.assertEquals(oct(a), oct(255))

    def test_19_logical_operators_should_work_with_atomic_ints(self):
        """ Comparison operators work on AtomicInts """
        a = atomic.AtomicInt(5)
        b = atomic.AtomicInt(10)
        c = atomic.AtomicInt(10)
        self.assertTrue(a < b)
        self.assertTrue(5 < b)
        self.assertTrue(a < 10)
        self.assertTrue(b > a)
        self.assertTrue(10 > a)
        self.assertTrue(b > 5)
        self.assertTrue(b <= c)
        self.assertTrue(b >= c)
        self.assertTrue(b == c)
        self.assertTrue(10 == c)
        self.assertTrue(c == 10)
        self.assertTrue(a != c)
        self.assertTrue(5 != c)
        self.assertTrue(c != 5)
        self.assertTrue(c is c)
        self.assertTrue(c is not b)


    def test_20_binary_operators_should_work_with_atomic_ints(self):
        """ Bitwise operators work on AtomicInts """
        a = atomic.AtomicInt(2)
        b = atomic.AtomicInt(1)
        self.assertEquals(a & b, 0)
        self.assertEquals(a & 0, 0)
        self.assertEquals(0 & a, 0)
        self.assertEquals(a & a, a)

        self.assertEquals(a | b, 3)
        self.assertEquals(a | 1, 3)
        self.assertEquals(1 | a, 3)
        self.assertEquals(a | a, a)

        c = atomic.AtomicInt(3)
        self.assertEquals(a ^ c, 1)
        self.assertEquals(c ^ 2, 1)
        self.assertEquals(2 ^ c, 1)
        self.assertEquals(c ^ c, 0)

        self.assertEquals(~a, -3)

        d = atomic.AtomicInt(1)
        self.assertEquals(d, 1)
        self.assertEquals(d << 1, 2)
        d <<= 1
        self.assertEquals(d, 2)

        self.assertEquals(d >> 1, 1)
        d >>= 1
        self.assertEquals(d, 1)

    def test_21_numeric_operations_should_work_with_atomic_int(self):
        """ Numeric operations should work on AtomicInts """
        a = atomic.AtomicInt(10)
        b = atomic.AtomicInt(5)
        self.assertEquals(math.ceil(a), 10.0)
        self.assertEquals(math.floor(a), 10.0)
        self.assertEquals(-a, -10)
        self.assertEquals(divmod(a, a), (1, 0))
        self.assertEquals(divmod(a, b), (2, 0))
        self.assertEquals(divmod(a, 5), (2, 0))
        self.assertEquals(divmod(10, b), (2, 0))

    def test_22_atomic_int_should_raise_when_operated_on_with_non_integer_type(self):
        """ AtomicInt should raise when operated on with non integer type """
        a = atomic.AtomicInt(3)
        with self.assertRaises(TypeError):
            a += 2.0
        with self.assertRaises(TypeError):
            a -= 2.0
        with self.assertRaises(TypeError):
            a *= 2.0
        with self.assertRaises(TypeError):
            a /= 2.0
        with self.assertRaises(TypeError):
            a %= 2.0
        with self.assertRaises(TypeError):
            print(pow(a, 2.5))
        with self.assertRaises(TypeError):
            print(divmod(a, 2.5))

if __name__ == "__main__":
    unittest.main(verbosity=5)
