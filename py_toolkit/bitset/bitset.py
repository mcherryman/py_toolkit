#!/usr/bin/env python 

import itertools
import collections
import sys
if sys.version_info.major < 3:
    import StringIO as stringio
else:
    import stringio
    
BIT_CONST_STR = 'BIT_{0}'
BITMASK_VALUE_TYPE_ERROR = 'Expected int type, found {0} for {1}.'
BITMASK_VALUE_RANGE_ERROR = '{0} is not in the range 0-{1}.'
UNKNOWN_TYPE_ERROR = 'Type {0} has not been declared.'
DUPLICATE_FIELDS_ERROR = 'Fields contains duplicate entries: [{0}]'
DUPLICATE_BITSET_NAME_ERROR = "BitSet name '{0}' has been declared already"

class EmptyAttributeListError(Exception):
    def __init__(self):
        super(EmptyAttributeListError, self).__init__('Cannot declare a BitSet with no attributes')

class DuplicateAttributeError(Exception):
    def __init__(self, fields):
        super(DuplicateAttributeError, self).__init__(DUPLICATE_FIELDS_ERROR.format(', '.join(sorted([ item for (item, count,) in collections.Counter(fields).items() if count > 1 ]))))

class DuplicateTypeError(Exception):
    def __init__(self, typename):
        super(DuplicateTypeError, self).__init__(DUPLICATE_BITSET_NAME_ERROR.format(typename))

class TypeNotDeclaredError(Exception):
    def __init__(self, typename):
        super(TypeNotDeclaredError, self).__init__(UNKNOWN_TYPE_ERROR.format(typename))

class InvalidBitMaskValueError(Exception):
    def __init__(self, val, max_val):
        super(InvalidBitMaskValueError, self).__init__(BITMASK_VALUE_RANGE_ERROR.format(val, max_val))

class InvalidBitMaskValueTypeError(Exception):
    def __init__(self, val):
        super(InvalidBitMaskValueTypeError, self).__init__(BITMASK_VALUE_TYPE_ERROR.format(type(val), val))

class BitBase(object):
    def __init__(self, val = 0):
        if not self.keys:
            raise EmptyAttributeListError()
        if not len(self.keys) == len(set(self.keys)):
            raise DuplicateAttributeError(self.keys)
        self.load(val)
        self.bit_consts = None

    def __len__(self):
        return len(self.keys)

    def __str__(self):
        out = stringio.StringIO()
        out.write('Value: {0}\nBits: {1}\nAttributes:\n'.format(self.value(), self.bits()))
        for k in self.keys:
            out.write('  {0}: {1}\n'.format(k, 'Enabled' if getattr(self, k) else 'Disabled'))
        return out.getvalue()

    __unicode__ = __str__

    def fields(self):
        return [ k for k in self.keys ]

    def consts(self):
        if not self.bit_consts:
            self.bit_consts = {}
            for (k, v,) in zip([ BIT_CONST_STR.format(k.upper()) for k in self.keys ], map(pow, [2] * len(self.keys), range(len(self.keys)))):
                self.bit_consts[k] = v
        return self.bit_consts

    def bits(self):
        return '{{0:0{0}b}}'.format(len(self)).format(self.value())

    def value(self):
        bitmask = itertools.imap(pow, [2] * len(self), range(len(self)))
        return sum(itertools.compress(bitmask, [ getattr(self, k) for k in self.keys ]))

    def load(self, val):
        if type(val) is not int:
            raise InvalidBitMaskValueTypeError(val)
        if val > self.max_val:
            raise InvalidBitMaskValueError(val, self.max_val)
        active_bits = [ v for v in itertools.compress(self.keys, [ bool(int(x)) for x in reversed(list('{0:0b}'.format(val))) ]) ]
        for k in active_bits:
            setattr(self, k, True)
        for k in set(self.keys) - set(active_bits):
            setattr(self, k, False)

class BitSet(BitBase):
    def __init__(self, keys, val = 0):
        self.keys = keys
        self.max_val = pow(2, len(self.keys)) - 1
        for (k, i,) in zip(keys, range(len(self.keys))):
            setattr(BitSet, BIT_CONST_STR.format(k.upper()), pow(2, i))
        super(BitSet, self).__init__(val)
        self.load(val)

class BitSetTypeFactory(object):
    def __init__(self):
        self.types = {}

    def declareType(self, name, fields):
        if not fields: 
            raise EmptyAttributeListError()
        if name in self.types:
            raise DuplicateTypeError(name)
        self.types[name] = self.createType(name, fields)

    def createType(self, name, fields):
        d = {}
        d['keys'] = fields
        d['max_val'] = pow(2, len(fields)) - 1
        for (k, i,) in zip(fields, map(pow, [2] * len(fields), range(len(fields)))):
            d['BIT_{0}'.format(k.upper())] = i
        return type(name, (BitBase,), d)

    def create(self, name, val = 0):
        if name in self.types:
            return self.types[name](val)
        raise TypeNotDeclaredError(name)

BitSets = BitSetTypeFactory()
if __name__ == '__main__':
    features = BitSet(['dsps', 'sip', 'users', 'full_manipulation',  'vm'], val=2)
    print features
    features.dsps = True
    print features
    features.vm = True
    print features
    features.dsps = False
    features.vm = False
    print features
    Features = BitSets.createType('Features', ['field1', 'field2'])
    f = Features(2)
    print f
    print f.fields()
    print f.consts()
    BitSets.declareType('FeatureSet', ['Field_A', 'Field_B', 'Field_C'])
    my_features = BitSets.create('FeatureSet', val=2)
    print my_features
    my_features.Field_B = False
    print my_features
    try:
        BadSet = BitSet([])
    except EmptyAttributeListError as e:
        print 'ExpectedError: {0}'.format(e)
    try:
        BadSet = BitSet(['Field_A', 'Field_A', 'Field_B', 'Field_B', 'Field_C'])
    except DuplicateAttributeError as e:
        print 'ExpectedError: {0}'.format(e)
    field_list = ['Field_One', 'Field_Two']
    try:
        BadSet = BitSet(field_list, val='20')
    except InvalidBitMaskValueTypeError as e:
        print 'ExpectedError: {0}'.format(e)
    try:
        BadSet = BitSet(field_list, val=20)
    except InvalidBitMaskValueError as e:
        print 'ExpectedError: {0}'.format(e)
    try:
        BitSets.declareType('FeatureSet', field_list)
    except DuplicateTypeError as e:
        print 'ExpectedError: {0}'.format(e)
    try:
        my_set = BitSets.create('UnknownSet')
    except TypeNotDeclaredError as e:
        print 'ExpectedError: {0}'.format(e)
