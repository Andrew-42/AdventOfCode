import pathlib


chars = list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')


def load_data(file_name: pathlib.Path) -> list[str]:
    with open(file_name, 'r') as file:
        return [line.strip() for line in file.readlines()]


def rucksack_priority(items: str) -> int:
    compartment1 = set(items[:len(items)//2])
    compartment2 = set(items[len(items)//2:])
    common_item = (compartment1 & compartment2).pop()
    return chars.index(common_item) + 1


def calculate_priority(data: list[str]) -> int:
    return sum(rucksack_priority(items) for items in data)


def group_priority(members: list[str]) -> int:
    elf1 = set(members[0])
    elf2 = set(members[1])
    elf3 = set(members[2])
    badge = (elf1 & elf2 & elf3).pop()
    return chars.index(badge) + 1


def calculate_group_priority(data: list[str]) -> int:
    groups = []
    group = []
    for i, elf in enumerate(data):
        if ((i + 1) % 3) == 0:
            group.append(elf)
            groups.append(group)
            group = []
            continue
        group.append(elf)
    return sum(group_priority(members) for members in groups)


def test():
    data = [
        "vJrwpWtwJgWrhcsFMMfFFhFp",
        "jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL",
        "PmmdzqPrVvPwwTWBwg",
        "wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn",
        "ttgJtRGJQctTZtZT",
        "CrZsJsPPZsGzwwsLwLmpwMDw",
    ]
    assert 157 == calculate_priority(data)
    assert 70 == calculate_group_priority(data)


if __name__ == "__main__":
    test()
    input_data = load_data(pathlib.Path('input.txt'))
    print(calculate_priority(input_data))
    print(calculate_group_priority(input_data))
