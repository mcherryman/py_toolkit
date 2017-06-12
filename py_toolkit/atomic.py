# -*- coding: utf-8 -*-

"""
Provide a simple implementation of an AtomicInt, supporting all operations of int but in a thread safe manner

https://docs.python.org/2.0/ref/numeric-types.html

    a = AtomicInt()
    a + 5
    5

    b = 5
    b + a
    10

    b + a.value
    10

Assignment is undetectable so;
 a = AtomicInt()
 type(a)
 <class 'AtomicInt'>

 a = 3
 type(a)
 <type 'int'>

is annoying but unavoidable behaviour

 a = AtomicInt()
 a.value = 3
 type(a)
 <class 'AtomicInt'>

is the correct form for this.
"""

import threading

class AtomicInt(object):
    def __init__(self, value=0):
        self._value = value
        self._lock = threading.RLock()

    def _check_and_return_other_value(self, b):
        if isinstance(b, AtomicInt):
            return self.value if self is b else b.value
        elif isinstance(b, (int, long)):
            return b
        else:
            raise TypeError("{0} is not an integer value".format(type(b)))

    @property
    def value(self):
        with self._lock:
            return self._value

    @value.setter
    def value(self, new_value):
        with self._lock:
            self._value = new_value

    def __repr__(self):
        return str(self)

    def __str__(self):
        with self._lock:
            return "{0}".format(self._value)

    def __unicode__(self):
        return self.__str__()

    def __add__(self, b):
        with self._lock:
            return AtomicInt(self._value + self._check_and_return_other_value(b))

    def __radd__(self, b):
        with self._lock:
            return AtomicInt(self._check_and_return_other_value(b) + self._value)

    def __iadd__(self, b):
        with self._lock:
            self._value += self._check_and_return_other_value(b)
            return self

    def __sub__(self, b):
        with self._lock:
            return AtomicInt(self._value - self._check_and_return_other_value(b))


    def __rsub__(self, b):
        with self._lock:
            return AtomicInt(self._check_and_return_other_value(b) - self._value)


    def __isub__(self, b):
        with self._lock:
            self._value -= self._check_and_return_other_value(b)
            return self

    def __mul__(self, b):
        with self._lock:
            return AtomicInt(self._value * self._check_and_return_other_value(b))

    def __rmul__(self, b):
        with self._lock:
            return AtomicInt(self._check_and_return_other_value(b) * self._value )

    def __imul__(self, b):
        with self._lock:
            self._value *= self._check_and_return_other_value(b)
            return self

    def __div__(self, b):
        with self._lock:
            return AtomicInt(self._value / self._check_and_return_other_value(b))

    def __rdiv__(self, b):
        with self._lock:
            return AtomicInt(self._check_and_return_other_value(b) / self._value)

    def __idiv__(self, b):
        with self._lock:
            self._value /= self._check_and_return_other_value(b)
            return self

    def __lt__(self, b):
        with self._lock:
            return self._value < self._check_and_return_other_value(b)

    def __le__(self, b):
        with self._lock:
            return self._value <= self._check_and_return_other_value(b)

    def __gt__(self, b):
        with self._lock:
            return self._value > self._check_and_return_other_value(b)

    def __ge__(self, b):
        with self._lock:
            return self._value >= self._check_and_return_other_value(b)

    def __eq__(self, b):
        with self._lock:
            return self._value == self._check_and_return_other_value(b)

    def __ne__(self, b):
        with self._lock:
            return self._value != self._check_and_return_other_value(b)

    def __floordiv__(self, b):
        with self._lock:
            return AtomicInt(self._value // self._check_and_return_other_value(b))

    def __ifloordiv__(self, b):
        with self._lock:
            self._value //= self._check_and_return_other_value(b)
            return self

    def __divmod__(self, b):
        with self._lock:
            return (self._value // self._check_and_return_other_value(b)), (self._value % self._check_and_return_other_value(b))

    def __rdivmod__(self, b):
        with self._lock:
            return (self._check_and_return_other_value(b) // self._value ), (self._check_and_return_other_value(b) % self._value)

    def __mod__(self, b):
        with self._lock:
            return AtomicInt(self._value % self._check_and_return_other_value(b))

    def __rmod__(self, b):
        with self._lock:
            return AtomicInt(self._check_and_return_other_value(b) % self._value)

    def __imod__(self, b):
        with self._lock:
            self._value %= self._check_and_return_other_value(b)
            return self

    def __pow__(self, b, modulo = None):
        with self._lock:
            return AtomicInt(pow(self._value, self._check_and_return_other_value(b), modulo))

    def __ipow__(self, b, modulo=None):
        with self._lock:
            self._value = pow(self._value, self._check_and_return_other_value(b), modulo)
            return self

    def __lshift__(self, b):
        with self._lock:
            return AtomicInt(self._value << self._check_and_return_other_value(b))

    def __ilshift__(self, b):
        with self._lock:
            self._value <<= self._check_and_return_other_value(b)
            return self

    def __rshift__(self, b):
        with self._lock:
            return AtomicInt(self._value >> self._check_and_return_other_value(b))

    def __irshift__(self, b):
        with self._lock:
            self._value >>= self._check_and_return_other_value(b)
            return self

    def __and__(self, b):
        with self._lock:
            return self._value & self._check_and_return_other_value(b)

    def __rand__(self, b):
        with self._lock:
            return self._check_and_return_other_value(b) & self._value

    def __iand__(self, b):
        with self._lock:
            self._value = int(self._value & self._check_and_return_other_value(b))
            return self

    def __xor__(self, b):
        with self._lock:
            return self._value ^ self._check_and_return_other_value(b)

    def __rxor__(self, b):
        with self._lock:
            return self._check_and_return_other_value(b) ^ self._value

    def __ixor__(self, b):
        with self._lock:
            self._value = int(self._value ^ self._check_and_return_other_value(b))
            return self

    def __or__(self, b):
        with self._lock:
            return self._value | self._check_and_return_other_value(b)

    def __ror__(self, b):
        with self._lock:
            return  self._check_and_return_other_value(b) | self._value

    def __ior__(self, b):
        with self._lock:
            self._value = int(self._value | self._check_and_return_other_value(b))
            return self

    def __neg__(self):
        with self._lock:
            return AtomicInt(-self._value)

    def __pos__(self):
        with self._lock:
            return AtomicInt(+self._value)

    def __abs__(self):
        with self._lock:
            return AtomicInt(abs(self._value))

    def __invert__(self):
        with self._lock:
            return AtomicInt(~self._value)

    def __complex__(self):
        with self._lock:
            return complex(self._value)

    def __int__(self):
        with self._lock:
            return int(self._value)

    def __long__(self):
        with self._lock:
            return long(self._value)

    def __float__(self):
        with self._lock:
            return float(self._value)

    def __oct__(self):
        with self._lock:
            return oct(self._value)

    def __hex__(self):
        with self._lock:
            return hex(self._value)

def increment(obj):
    assert (isinstance(obj, AtomicInt))
    obj += 1
    return obj.value

def decrement(obj):
    assert (isinstance(obj, AtomicInt))
    obj -= 1
    return obj.value
