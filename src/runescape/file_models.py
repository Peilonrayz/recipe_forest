from __future__ import annotations

import dataclasses
import json
from typing import Any, Dict, List, Optional

from dataclasses_json import dataclass_json

from . import models


@dataclass_json
@dataclasses.dataclass(frozen=True)
class NameAmount:
    name: str
    amount: int


@dataclass_json
@dataclasses.dataclass(frozen=True)
class Experience:
    smithing: Optional[float] = None
    mining: Optional[float] = None


@dataclass_json
@dataclasses.dataclass(frozen=True)
class Skills:
    smithing: Optional[int] = None
    mining: Optional[int] = None


@dataclass_json
@dataclasses.dataclass(frozen=True)
class Requirements:
    members: bool
    skills: Skills


@dataclass_json
@dataclasses.dataclass(frozen=True)
class InternalVector:
    mats: List[NameAmount]
    to: str
    exp: Experience
    amount: int
    type: str
    requirements: Requirements


@dataclass_json
@dataclasses.dataclass
class Mats:
    resources: List[Any]
    transformations: List[InternalVector]


RESOURCES = {"Item": dataclass_json(models.Item).schema()}


def _load_nodes(resources: List[Any]):
    nodes = {}
    for resource in resources:
        model = RESOURCES[resource.pop("_type")].load(resource)
        nodes[model.name] = models.Node(model, [], [])
    return nodes


def load_transformations(
    transformations: List[InternalVector], nodes: Dict[str, models.Node]
):
    for trans in transformations:
        yield models.Vector(
            tuple(
                [models.NameAmount(nodes[mat.name], mat.amount) for mat in trans.mats]
            ),
            nodes[trans.to],
            trans.exp,
            trans.amount,
            trans.type,
            trans.requirements,
        )


def read_file(location):
    with open(location) as f:
        mats = Mats.schema().load(json.load(f))
        nodes = _load_nodes(mats.resources)
        for trans in load_transformations(mats.transformations, nodes):
            trans.to.recipes.append(trans)
            for mat in trans.mats:
                mat.name.uses.append(trans)
        return nodes
