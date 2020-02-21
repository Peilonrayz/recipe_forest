from __future__ import annotations

from abc import ABCMeta
from typing import Generic, Sequence, TypeVar

T = TypeVar("T")

NULL = object()


def _get_key_item(self):
    return {item.item: item for item in self._data}


def _merge(fn, first, second):
    output = []
    seen = set()
    for key, value in first.items():
        output.append(fn(value, second.get(key, NULL)))
        seen.add(key)
    for key, value in second.items():
        if key not in seen:
            output.append(fn(NULL, value))
    return output


def _scalar_merge(fn, items, amount):
    return [fn(item, amount) for item in items]


def _build_special(method):
    def fn(self, other):
        if isinstance(other, (int, float)):
            return type(self)(_scalar_merge(method, self, other))
        if not isinstance(other, type(self)):
            raise TypeError(f"{other!r} is not an instance of {type(self)!r}")
        items = _merge(method, _get_key_item(self), _get_key_item(other),)
        return type(self)(items)

    return fn


def _build_item_special(method):
    def fn(self, other):
        if isinstance(other, (int, float)):
            pass
        elif not isinstance(other, type(self)):
            raise TypeError(f"{other!r} is not an instance of {type(self)!r}")
        elif self.item != other.item:
            raise ValueError(f"Can't mix conflicting items.")
        else:
            other = other.amount
        return type(self)(self.item, method(self.amount, other))

    return fn


BLACKLIST = {
    "__init__",
    "__repr__",
    "__module__",
    "__qualname__",
    "__iter__",
    "__annotations__",
    "__orig_bases__",
    "__getitem__",
    "__len__",
    "__slots__",
    "__class_getitem__",
    "__dict__",
    "__parameters__",
    "__weakref__",
    "__abstractmethods__",
    "__contains__",
    "__reversed__",
}


class ItemsMeta(ABCMeta):
    def __new__(self, name, bases, props):
        for base in bases:
            for key in dir(base):
                if (
                    key.startswith("__")
                    and key.endswith("__")
                    and key not in BLACKLIST
                    and not hasattr(NULL, key)
                    and key not in props
                ):
                    props[key] = getattr(base, key)

        for key, prop in props.items():
            if key.startswith("__") and key.endswith("__") and key not in BLACKLIST:
                props[key] = _build_special(prop)
        return ABCMeta.__new__(self, name, bases, props)


class Items(Sequence[T], metaclass=ItemsMeta):
    def __init__(self, *args, **kwargs):
        self._data = tuple(*args, **kwargs)

    def __repr__(self):
        return type(self).__name__ + repr(self._data)

    def __iter__(self):
        return iter(self._data)

    def __getitem__(self, i: int) -> T:
        return self._data[i]

    def __len__(self) -> int:
        return len(self._data)


class ItemMeta(type):
    def __new__(self, name, bases, props):
        for key, prop in props.items():
            if key.startswith("__") and key.endswith("__") and key not in BLACKLIST:
                props[key] = _build_item_special(prop)
        return type.__new__(self, name, bases, props)


class Item(Generic[T], metaclass=ItemMeta):
    item: T
    amount: float


class ItemsCommonMixin:
    def __add__(self, other):
        if self is NULL:
            return other
        if other is NULL:
            return self
        return self + other

    def __mul__(self, other):
        if self is NULL:
            return other
        if other is NULL:
            return self
        return self * other
