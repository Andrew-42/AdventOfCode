from dataclasses import dataclass
from typing import Callable
from functools import partial


def load_data(file_path: str) -> list[str]:
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]


@dataclass
class Monkey:
    items: list[int]
    operation: Callable[[int], int]
    test_div: int
    true_res: int
    false_res: int
    n_inspections: int = 0
    gcd: int = 1

    def inspect(self, monkeys: list["Monkey"]) -> list["Monkey"]:
        for item in self.items:
            self.n_inspections += 1
            # new = self.operation(item) // 3
            new = self.operation(item)
            if new % self.test_div == 0:
                monkeys[self.true_res].items.append(new % self.gcd)
            else:
                monkeys[self.false_res].items.append(new)
        self.items = []
        return monkeys


def plus(a: int, b: int) -> int:
    return a + b


def times(a: int, b: int) -> int:
    return a * b


def power(a: int, b: int) -> int:
    return a ** b


def parse_monkeys(data: list[str]) -> list[Monkey]:
    monkey_data = []
    one_monkey = []
    gcd = 1
    for line in data:
        if line == "":
            monkey_data.append(one_monkey)
            one_monkey = []
            continue
        one_monkey.append(line)
        if line.startswith('Test:'):
            gcd *= int(line.split(' ')[-1])
    monkey_data.append(one_monkey)
    monkey_list = []
    for monkey_d in monkey_data:
        assert monkey_d[0].startswith('Monkey ')
        items = [int(item) for item in monkey_d[1][16:].split(', ')]
        if '*' in monkey_d[2]:
            var = monkey_d[2].split(' ')[-1]
            if var == 'old':
                operation = partial(power, b=2)
            else:
                const = int(var)
                operation = partial(times, b=const)
        elif '+' in monkey_d[2]:
            var = monkey_d[2].split(' ')[-1]
            if var == 'old':
                operation = partial(times, b=2)
            else:
                const = int(var)
                operation = partial(plus, b=const)
        else:
            raise ValueError('Invalid operation.')
        test_div = int(monkey_d[3].split(' ')[-1])
        true_res = int(monkey_d[4].split(' ')[-1])
        false_res = int(monkey_d[5].split(' ')[-1])
        monkey_list.append(
            Monkey(items, operation, test_div, true_res, false_res, 0, gcd)
        )
    return monkey_list


def get_monkey_state(data: list[str], n_rounds: int) -> list[Monkey]:
    monkey_list = parse_monkeys(data)
    for round in range(n_rounds):
        for i in range(len(monkey_list)):
            monkey_list = monkey_list[i].inspect(monkey_list)
    return monkey_list


def get_monkey_business(monkey_data: list[Monkey]) -> int:
    first, second = sorted(monkey_data, key=lambda i: -i.n_inspections)[:2]
    return first.n_inspections * second.n_inspections


def test():
    data = [
        "Monkey 0:",
        "Starting items: 79, 98",
        "Operation: new = old * 19",
        "Test: divisible by 23",
        "If true: throw to monkey 2",
        "If false: throw to monkey 3",
        "",
        "Monkey 1:",
        "Starting items: 54, 65, 75, 74",
        "Operation: new = old + 6",
        "Test: divisible by 19",
        "If true: throw to monkey 2",
        "If false: throw to monkey 0",
        "",
        "Monkey 2:",
        "Starting items: 79, 60, 97",
        "Operation: new = old * old",
        "Test: divisible by 13",
        "If true: throw to monkey 1",
        "If false: throw to monkey 3",
        "",
        "Monkey 3:",
        "Starting items: 74",
        "Operation: new = old + 3",
        "Test: divisible by 17",
        "If true: throw to monkey 0",
        "If false: throw to monkey 1",
    ]
    monkeys_1 = get_monkey_state(data, 750)
    # assert [20, 23, 27, 26] == monkeys_1[0].items
    # assert [2080, 25, 167, 207, 401, 1046] == monkeys_1[1].items
    # assert [] == monkeys_1[2].items
    # assert [] == monkeys_1[3].items
    # assert 10605 == get_monkey_business(get_monkey_state(data, 20))
    assert 2713310158 == get_monkey_business(get_monkey_state(data, 10_000))


if __name__ == '__main__':
    test()
    print(get_monkey_business(get_monkey_state(load_data('input.txt'), 10_000)))

