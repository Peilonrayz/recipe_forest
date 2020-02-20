from __future__ import annotations

from typing import Any, List, Generic, TypeVar, Union
import dataclasses
import math
import operator
import functools


T = TypeVar('T')

NULL = object()


def _get_key_item(self):
    return {
        item.item: item
        for item in self._data
    }


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
            raise TypeError(f'{other!r} is not an instance of {type(self)!r}')
        items = _merge(
            method,
            _get_key_item(self),
            _get_key_item(other),
        )
        return type(self)(items)
    return fn

BLACKLIST = {
    '__init__',
    '__repr__',
    '__module__',
    '__qualname__',
    '__iter__',
    '__annotations__',
    '__orig_bases__',
}

class ItemsMeta(type):
    def __new__(self, name, bases, props):
        for key, prop in props.items():
            if key.startswith('__') and key.endswith('__') and key not in BLACKLIST:
                props[key] = _build_special(prop)
        return type.__new__(self, name, bases, props)


class Items(metaclass=ItemsMeta):
    def __init__(self, *args, **kwargs):
        self._data = tuple(*args, **kwargs)

    def __repr__(self):
        return type(self).__name__ + repr(self._data)

    def __iter__(self):
        return iter(self._data)

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


def _build_item_special(method):
    def fn(self, other):
        if isinstance(other, (int, float)):
            pass
        elif not isinstance(other, type(self)):
            raise TypeError(f'{other!r} is not an instance of {type(self)!r}')
        elif self.item != other.item:
            raise ValueError(f"Can't mix conflicting items.")
        else:
            other = other.amount
        return type(self)(self.item, method(self.amount, other))
    return fn


class ItemMeta(type):
    def __new__(self, name, bases, props):
        for key, prop in props.items():
            if key.startswith('__') and key.endswith('__') and key not in BLACKLIST:
                props[key] = _build_item_special(prop)
        return type.__new__(self, name, bases, props)


class Item(metaclass=ItemMeta):
    pass

########
# Core #
########

def reduce_req_exp(values, op=operator.add):
    reqs, exps = zip(*values)
    return functools.reduce(op, reqs), functools.reduce(op, exps)


@dataclasses.dataclass(frozen=True)
class Requirement(Generic[T], Item):
    item: T
    amount: int = 1

    __add__ = operator.add
    __mul__ = operator.mul

    def make_from(self, items):
        req, exp = self.item.make_from(items)
        return req * self.amount, exp * self.amount


class Requirements(Items):
    pass


@dataclasses.dataclass(frozen=True)
class Experiance(Item):
    item: str
    amount: float

    __add__ = operator.add
    __mul__ = operator.mul


class Experiance_(Items):
    pass


@dataclasses.dataclass(frozen=True)
class Ore:
    name: str
    exp: float

    def make_from(self, items):
        return (
            Requirements([Requirement(self, 1)]),
            Experiance_([Experiance('Mining', self.exp)])
        )


@dataclasses.dataclass(frozen=True)
class Ingot:
    name: str
    exp: float
    requirements: List[Requirement[Ore]]

    def make_from(self, items):
        if self not in items:
            reqs, exp = reduce_req_exp(
                r.make_from(items) for r in self.requirements
            )
        else:
            reqs, exp = Requirements([Requirement(self, 1)]), Experiance_()
        exp += Experiance_([Experiance('Smithing', self.exp)])
        return reqs, exp


@dataclasses.dataclass(frozen=True)
class ForgeItem:
    name: str
    rank: int
    exp: int
    requirements: List[Requirement[Union[ForgeItem, Ingot]]]

    def make_from(self, items):
        if self not in items:
            reqs, exp = reduce_req_exp(
                r.make_from(items) for r in self.requirements
            )
        else:
            reqs, exp = Requirements([Requirement(self, 1)]), Experiance_()
        exp += Experiance_([Experiance('Smithing', self.exp)])
        return reqs, exp


orichalcite_ore = Ore('Orichalcite Ore', 436.8)
drakolith_ore = Ore('Drackolith Ore', 436.8)
orikalkum_bar = Ingot('Orikalkum Ingot', 13, Requirements([Requirement(orichalcite_ore, 1), Requirement(drakolith_ore, 1)]))
orikalkum_forge_item = ForgeItem('Orikalkum Forge Item', 0, 350, Requirements([Requirement(orikalkum_bar, 1)]))
orikalkum_forge_item_1 = ForgeItem('Orikalkum Forge Item+1', 1, 350, Requirements([Requirement(orikalkum_forge_item, 1), Requirement(orikalkum_bar, 1)]))
orikalkum_forge_item_2 = ForgeItem('Orikalkum Forge Item+2', 2, 700, Requirements([Requirement(orikalkum_forge_item_1, 1), Requirement(orikalkum_bar, 2)]))
orikalkum_forge_item_3 = ForgeItem('Orikalkum Forge Item+3', 3, 1400, Requirements([Requirement(orikalkum_forge_item_2, 1), Requirement(orikalkum_bar, 4)]))
orikalkum_forge_item_burial = ForgeItem('Orikalkum Forge Item Burial', -1, 1400, Requirements([Requirement(orikalkum_forge_item_3, 1)]))

exp = input('Wanted Smithing EXP: ')
reqs, exps = orikalkum_forge_item_burial.make_from([])
smith_exp = next(e for e in exps if e.item == 'Smithing')
amount_needed = math.ceil(int(exp) / smith_exp.amount)
reqs *= amount_needed
print('You need:')
for req in reqs:
    print(f'{req.amount} {req.item.name}')

print('You get:')
exps *= amount_needed
for exp in exps:
    print(f'{exp.amount} {exp.item} exp')
