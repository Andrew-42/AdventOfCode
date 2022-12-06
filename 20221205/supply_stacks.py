def load_data(path: str) -> list[str]:
    with open(path, 'r') as file:
        return file.readlines()


def parse_data(data: list[str]) -> tuple[list[tuple[int, str, str]], dict[str, list[str]]]:
    stacks = {
        "1": [],
        "2": [],
        "3": [],
        "4": [],
        "5": [],
        "6": [],
        "7": [],
        "8": [],
        "9": [],
    }
    for line in data:
        if " 1" in line:
            for key in stacks:
                stacks[key].reverse()
            break
        for j, i in enumerate(range(1, len(line), 4)):
            if (crate := line[i]) != ' ':
                stacks[str(j + 1)].append(crate)
    moves = []
    for line in data:
        if 'move' not in line:
            continue
        line_moves = line.strip().split(' ')
        moves.append((int(line_moves[1]), line_moves[3], line_moves[5]))
    return moves, stacks


def move_crates(data: tuple[list[tuple[int, str, str]], dict[str, list[str]]]) -> dict[str, list[str]]:
    moves = data[0]
    stacks = data[1]
    for move in moves:
        for n in range(move[0]):
            stacks[move[2]].append(stacks[move[1]].pop())
    return stacks


def move_crates2(data: tuple[list[tuple[int, str, str]], dict[str, list[str]]]) -> dict[str, list[str]]:
    moves = data[0]
    stacks = data[1]
    for move in moves:
        moved_crates = stacks[move[1]][-move[0]:]
        lower_crates = stacks[move[1]][:-move[0]]
        stacks[move[1]] = lower_crates
        stacks[move[2]].extend(moved_crates)
    return stacks


def get_result(stacks: dict[str, list[str]]) -> str:
    result = ""
    for key in stacks:
        try:
            result += stacks[key].pop()
        except IndexError:
            continue
    return result


def test():
    data = [
        "    [D]    ",
        "[N] [C]    ",
        "[Z] [M] [P]",
        " 1   2   3 ",
        "",
        "move 1 from 2 to 1",
        "move 3 from 1 to 3",
        "move 2 from 2 to 1",
        "move 1 from 1 to 2",
    ]
    result_stack = move_crates(parse_data(data))
    assert "CMZ" == get_result(result_stack)
    result_stack2 = move_crates2(parse_data(data))
    assert "MCD" == get_result(result_stack2)


if __name__ == "__main__":
    test()
    input_data = load_data('input.txt')
    parsed_data = parse_data(input_data)
    result_stack = move_crates2(parsed_data)
    print(get_result(result_stack))
