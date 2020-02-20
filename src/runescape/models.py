from __future__ import annotations

import dataclasses
import functools
import operator
from typing import Any, List, Optional, Tuple, TypeVar, Union

from .transparent_lists import Item, Items, ItemsCommonMixin

T = TypeVar('T')


def reduce_req_exp(values, op=operator.add):
    values = list(values)
    reqs, exps = zip(*values)
    return functools.reduce(op, reqs), functools.reduce(op, exps)


@dataclasses.dataclass(frozen=True)
class Requirement(Item[T]):
    item: T
    amount: float

    __add__ = operator.add
    __mul__ = operator.mul

    def make_from(self, items):
        req, exp = self.item.make_from(items)
        return req * self.amount, exp * self.amount


class Requirements(Items[Requirement[T]], ItemsCommonMixin):
    pass


@dataclasses.dataclass(frozen=True)
class Experience(Item[str]):
    item: T
    amount: float

    __add__ = operator.add
    __mul__ = operator.mul


class Experience_(Items[Experience], ItemsCommonMixin):
    pass


@dataclasses.dataclass(frozen=True)
class Item:
    name: str


@dataclasses.dataclass(frozen=True)
class NameAmount:
    name: Node
    amount: int


@dataclasses.dataclass(frozen=True)
class EXP:
    smithing: Optional[float]


@dataclasses.dataclass(frozen=True)
class Skills:
    smithing: Optional[int]


@dataclasses.dataclass(frozen=True)
class Reqs:
    members: bool
    skills: Skills


@dataclasses.dataclass(frozen=True)
class Vector:
    mats: Tuple[NameAmount, ...]
    to: Node
    exp: EXP
    amount: int
    type: str
    requirements: Reqs


@dataclasses.dataclass
class Node:
    item: Any
    recipes: List[Vector]
    uses: List[Vector]

    def make_from(self, items, amount=1):
        if not self.recipes:
            reqs, exp = Requirements([Requirement(self.item, 1)]), Experience_()
        elif len(self.recipes) != 1:
            raise ValueError("Doesn't work with multiple recipes.")
        else:
            recipe = self.recipes[0]
            if not recipe.mats:
                reqs, exp = Requirements([Requirement(self.item, 1)]), Experience_()
            elif self.item not in items:
                reqs, exp = reduce_req_exp(
                    mat.name.make_from(items, mat.amount) for mat in recipe.mats
                )
                exp += Experience_([Experience('Smithing', recipe.exp.smithing)])
            else:
                reqs, exp = Requirements([Requirement(self.item, 1)]), Experience_()
        reqs *= amount
        exp *= amount
        return reqs, exp
