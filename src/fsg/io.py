import datetime
import json

import marshmallow.fields
from typing_json.mm import fields
from typing_json.public.dataclasses_json import Converter

from . import models


class Date(fields.Field):
    def _deserialize(self, value, attr, data, **kwargs):
        year, month, day, *_ = (*value.split("-"), 1, 1)
        return datetime.date(int(year), int(month), int(day))


def person_field(people):
    people_by_id = {person.id: person for person in people}

    class Person(fields.Field):
        def _deserialize(self, value, attr, data, **kwargs):
            return people_by_id[value]

    return Person


def open_data(path):
    with open(path) as f:
        data = json.load(f)

    converter = Converter({datetime.date: Date})
    people = models.Person.schema(converter=converter).load(data["people"], many=True)
    converter.conversions[models.Person] = person_field(people)
    return models.Data(
        people,
        models.Group.schema(converter=converter).load(data["groups"], many=True),
        models.Relationship.schema(converter=converter).load(
            data["relationships"], many=True
        ),
    )
