import dataclasses
import datetime
import enum
import itertools
from typing import List, Optional

from typing_json.public import dataclasses_json

from . import events


@dataclasses_json.dataclass_json
@dataclasses.dataclass
class Person:
    id: int
    name: str
    birth: datetime.date
    death: Optional[datetime.date]


@dataclasses_json.dataclass_json
@dataclasses.dataclass
class Event:
    date: Optional[datetime.date]
    type: events.Friendship


@dataclasses_json.dataclass_json
@dataclasses.dataclass
class GroupPerson:
    person: Person
    joined: Optional[datetime.date]
    left: Optional[datetime.date]
    events: Optional[List[Event]]

    def get_events(self):
        return (
            [Event(self.joined or self.person.birth, events.Friendship.FRIENDS)]
            + ([] if self.events is None else self.events)
            + (
                []
                if self.left is None
                else [Event(self.left, events.Friendship.NOT_FRIENDS)]
            )
        )


@dataclasses_json.dataclass_json
@dataclasses.dataclass
class Group:
    name: str
    start: Optional[datetime.date]
    end: Optional[datetime.date]
    people: List[GroupPerson]
    events: Optional[List[Event]]

    def get_events(self):
        return (
            [Event(self.start, events.Friendship.FRIENDS)]
            + ([] if self.events is None else self.events)
            + (
                []
                if self.end is None
                else [Event(self.end, events.Friendship.NOT_FRIENDS)]
            )
        )

    def get_relationships(self):
        _events = self.get_events()
        people_events = sorted(
            [(person.person.id, list(person.get_events())) for person in self.people]
        )
        for (id_1, events_1), (id_2, events_2) in itertools.combinations(
            people_events, 2
        ):
            yield (id_1, id_2), events.merge_new_friendship(
                [_events, events_1, events_2]
            )


@dataclasses_json.dataclass_json
@dataclasses.dataclass
class Relationship:
    people: List[Person]
    events: Optional[List[Event]]
    start: Optional[datetime.date]
    end: Optional[datetime.date]
    type: Optional[events.Friendship]

    def get_events(self):
        default_start = max(p.birth for p in self.people)
        end = min((p.death for p in self.people if p.death), default=None)
        if self.events is not None:
            if self.start is not None or self.end is not None or self.type is not None:
                raise ValueError("Can't use events and non event in relationships.")
            return [
                Event(default_start, event.type) if event.date is None else event
                for event in self.events
            ] + ([] if (end) is None else [Event(end, events.Friendship.NOT_FRIENDS)])
        return [
            Event(self.start or default_start, self.type or events.Friendship.FRIENDS)
        ] + (
            []
            if (self.end or end) is None
            else [Event((self.end or end), events.Friendship.NOT_FRIENDS)]
        )

    def get_relationships(self):
        _events = self.get_events()
        return (
            (ids, _events)
            for ids in itertools.combinations(sorted(p.id for p in self.people), 2)
        )


@dataclasses.dataclass
class Data:
    people: List[Person]
    groups: List[Group]
    relationships: List[Relationship]

    def get_group_relationships(self):
        relationships = {}
        for group in self.groups:
            for ids, _events in group.get_relationships():
                relationships.setdefault(ids, []).append(_events)

        return {
            ids: events.merge_friends(_events) for ids, _events in relationships.items()
        }

    def get_relationships(self):
        relationships = self.get_group_relationships()
        for relationship in self.relationships:
            for ids, _events in relationship.get_relationships():
                relationships[ids] = events.overwrite_events(
                    relationships.get(id, []), _events
                )
        return relationships

    def get_edges(self):
        SENTINAL = object()
        for ids, _events in self.get_relationships().items():
            try:
                prev = next(_events)
            except StopIteration:
                continue
            for event in _events:
                if prev.type is not events.Friendship.NOT_FRIENDS:
                    yield (*ids, prev.type, prev.date, event.date)
                prev = event
            if prev.type is not events.Friendship.NOT_FRIENDS:
                yield (*ids, prev.type, prev.date, None)
