import dataclasses
import pathlib


def load_data(file_name: pathlib.Path) -> list[str]:
    with open(file_name, 'r') as file:
        return [line.strip() for line in file.readlines()]


@dataclasses.dataclass
class Interval:
    a: int
    b: int


def is_contained(interval1: Interval, interval2: Interval) -> bool:
    if (interval1.a <= interval2.a) & (interval2.b <= interval1.b):
        return True
    if (interval2.a <= interval1.a) & (interval1.b <= interval2.b):
        return True
    return False


def do_overlap(interval1: Interval, interval2: Interval) -> bool:
    if (interval1.a > interval2.a) & (interval1.a > interval2.b):
        return False
    if (interval1.a < interval2.a) & (interval1.b < interval2.a):
        return False
    return True


def parse_data(data: list[str]) -> list[tuple[Interval, Interval]]:
    split_data = [item.split(',') for item in data]
    to_intervals = [(item[0].split('-'), item[1].split('-')) for item in split_data]
    parsed_intervals = [
        (Interval(int(item[0][0]), int(item[0][1])), Interval(int(item[1][0]), int(item[1][1])))
        for item in to_intervals
    ]
    return parsed_intervals


def fully_contained_pairs(data: list[tuple[Interval, Interval]]) -> int:
    contained_pairs = [is_contained(pairs[0], pairs[1]) for pairs in data]
    return sum(contained_pairs)


def overlap_pairs(data: list[tuple[Interval, Interval]]) -> int:
    contained_pairs = [do_overlap(pairs[0], pairs[1]) for pairs in data]
    return sum(contained_pairs)


def test():
    data = [
        "2 - 4,6 - 8",
        "2 - 3,4 - 5",
        "5 - 7,7 - 9",
        "2 - 8,3 - 7",
        "6 - 6,4 - 6",
        "2 - 6,4 - 8",
    ]
    parsed_test_data = parse_data(data)
    assert 2 == fully_contained_pairs(parsed_test_data)
    assert 4 == overlap_pairs(parsed_test_data)


if __name__ == "__main__":
    test()
    input_data = load_data(pathlib.Path('input.txt'))
    parsed_data = parse_data(input_data)
    print(fully_contained_pairs(parsed_data))
    print(overlap_pairs(parsed_data))
