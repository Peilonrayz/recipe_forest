import datetime
import enum
import itertools
import heapq


class Friendship(enum.Enum):
    ENIMIES = (2, 'red')
    NOT_FRIENDS = (0, '')
    IN_TOUCH = (1, 'gray')
    FRIENDS = (2, 'green')
    BEST_FRIENDS = (3, 'blue')


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
    return none_values, new_friendships


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
        if started and len(started_friendships) == len(friendships) and all(started_friendships.values()):
            yield event, id_
            break
    yield from merged_friendships


def merge_new_friendship(friendships):
    return (event for event, _ in _merge_new_friendship(friendships))


def overwrite_events(original, new):
    last = None
    for event in new:
        yield event
        last = event

    original = iter(original)
    if last is not None:
        for event in original:
            if event.date >= last.date:
                yield event
                break
    yield from original
