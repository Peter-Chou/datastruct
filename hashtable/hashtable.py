# -*- coding: utf-8 -*-

from ..array import FixedArray


class Slot(object):
    """定义了hashtable的槽"""

    def __init__(self, key, value):
        self.key, self.value = key, value


class HashTable(object):

    UNUSED = None   # 没被使用过
    EMPTY = Slot(None, None)

    def __init__(self):
        self._table = FixedArray(8, init=HashTable.UNUSED)
        self.length = 0

    @property
    def _load_factor(self):
        # 如果 load_factor 超过0.8 rehash
        return self.length / float(len(self._table))

    def __len__(self):
        return self.length

    def _hash(self, key):
        return abs(hash(key)) % len(self._table)

    def _find_key(self, key):
        index = self._hash(key)
        _len = len(self._table)
        while self._table[index] is not HashTable.UNUSED:
            if self._table[index] is HashTable.EMPTY:   # 槽为空
                index = (index * 5 + 1) % _len
                continue
            elif self._table[index] == key:  # 槽有值且为key
                return index
            else:               # 槽有值但不为key
                index = (index * 5 + 1) % _len
        return None

    def _slot_can_insert(self, index):
        return (self._table[index] is HashTable.EMPTY or
                self._table[index] is HashTable.UNUSED)

    def _find_slot_for_insert(self, key):
        index = self._hash(key)
        _len = len(self._table)
        while not self._slot_can_insert(index):
            index = (index * 5 + 1) % _len
        return index

    def __contains__(self, key):    # 重新定义 in operator
        index = self._find_key(key)
        return index is not None

    def add(self, key, value):
        if key in self:
            index = self._find_key(key)
            self._table[index] = value
            return False
        else:
            index = self._find_slot_for_insert(key)
            self._table[index] = Slot(key, value)
            self.length += 1
            if self._load_factor >= 0.8:
                self._rehash()
            return True

    def _rehash(self):
        old_table = self._table
        newsize = len(self._table) * 2
        self._table = FixedArray(newsize, HashTable.UNUSED)
        self.length = 0
        for slot in old_table:
            if slot is not HashTable.UNUSED and slot is not HashTable.EMPTY:
                index = self._find_slot_for_insert(slot.key)
                self._table[index] = slot
                self.length += 1

    def get(self, key, default=None):
        index = self._find_key(key)
        if index is None:
            return default
        else:
            return self._table[index].value

    def remove(self, key):
        index = self._find_key(key)
        if index is None:
            raise KeyError()
        value = self._table[index].value
        self.length -= 1
        self._table[index] = HashTable.EMPTY
        return value

    def __iter__(self):
        for slot in self._table:
            if slot not in (HashTable.UNUSED, HashTable.EMPTY):
                yield slot.key