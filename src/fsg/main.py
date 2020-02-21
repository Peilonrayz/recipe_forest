import csv
import datetime
from pprint import pprint

from . import io, models


def main():
    data = io.open_data("data.json")
    default_end = datetime.datetime.now().date()
    with open("relationships.csv", "w", newline="") as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow("Source, Target, Weight, Colour, Timeset, Type".split(", "))
        for id_1, id_2, type_, start, end in data.get_edges():
            row = [
                id_1,
                id_2,
                type_.value[0],
                type_.value[1],
                f"<[{start}, {end or default_end}]>",
                "Undirected",
            ]
            csv_writer.writerow(row)
