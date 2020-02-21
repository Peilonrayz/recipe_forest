import dataclasses
import datetime
import enum
import itertools


@dataclasses.dataclass
class Friendship(enum.Enum):
    ENIMIES = (2, "red")
    NOT_FRIENDS = (0, "")
    IN_TOUCH = (1, "gray")
    FRIENDS = (2, "green")
    BEST_FRIENDS = (3, "blue")


@dataclasses.dataclass
class Person:
    id: int
    name: str
    birth: datetime.date
    death: Optional[datetime.date]


@dataclasses.dataclass
class Event:
    date: Optional[datetime.date]
    type: Friendship


@dataclasses.dataclass
class GroupPerson:
    person: Person
    joined: Optional[datetime.date]
    left: Optional[datetime.date]
    events: Optional[List[Event]]

    def get_events(self):
        return (
            [Event(self.joined or self.person.birth, Friendship.FRIENDS)]
            + ([] if self.events is None else self.events)
            + ([] if self.left is None else [Event(self.left, Friendship.NOT_FRIENDS)])
        )


@dataclasses.dataclass
class Group:
    name: str
    start: Optional[datetime.date]
    end: Optional[datetime.date]
    people: List[GroupPerson]
    events: Optional[List[Event]]

    def get_events(self):
        return (
            [Event(self.start, Friendship.FRIENDS)]
            + ([] if self.events is None else self.events)
            + ([] if self.end is None else [Event(self.end, Friendship.NOT_FRIENDS)])
        )

    def get_relationships(self):
        events = self.get_events()
        people_events = sorted(
            [
                (person.person.id, merge_new_friendship(events, person.get_events()))
                for person in self.people
            ]
        )
        for (id_1, events_1), (id_2, events_2) in itertools.combinations(
            people_events, 2
        ):
            yield id_1, id_2, merge_new_friendship(events_1, events_2)


@dataclasses.dataclass
class Relationship:
    people: List[People]
    events: Optional[List[Events]]
    start: Optional[datetime.date]
    end: Optional[datetime.date]
    type: Optional[Friendship]

    def get_events(self):
        if self.events is not None:
            if self.start is not None or self.end is not None or self.type is not None:
                raise ValueError("Can't use events and non event in relationships.")
            return list(self.events)
        return [
            Event(
                self.start or max(p.birth for p in people),
                self.type or Friendship.FRIENDS,
            )
        ] + ([] if self.end is None else [Event(self.end, Friendship.NOT_FRIENDS)])

    def get_relationships(self):
        events = self.get_events()
        return (
            (*ids, event)
            for ids in itertools.combinations(sorted(self.people), 2)
            for event in events
        )


def _add_friendship_identifier(friendships):
    def inner(events, identifier):
        return ((event, identifier) for event in events)

    identifiers = [object() for _ in range(len(friendships))]
    return [inner(events, id_) for events, id_ in zip(friendships, identifiers)]


def _prime_friends(friendships):
    none_values = []
    new_friendships = []
    for events in map(iter, friendships):
        for event in events:
            if event[0].date is not None:
                new_friendships.append(itertools.chain([event], events))
                break
            none_values.append(event)
    return new_friendships


def _merge_friends(friendships):
    fs1 = _add_friendship_identifier(friendships)
    none_values, fs2 = _prime_friends(fs1)
    yield from none_values
    yield from heapq.merge(*fs2, key=lambda i: i[0].date)


def merge_friends(friendships):
    return (event for event, _ in _merge_friends(friendships))


def _merge_new_friendship(friendships):
    started_friendships = {}
    merged_friendships = _merge_friends(friendships)
    for event, id_ in merged_friendships:
        started = event.type == Friendship.FRIENDS
        started_friendships[id_] = started
        if (
            started
            and len(started_friendships) == len(friendships)
            and all(started_friendships.values())
        ):
            yield event, id_
            break
    yield from merged_friendships


def merge_new_friendship(friendships):
    return (event for event, _ in _merge_new_friendship(friendships))
