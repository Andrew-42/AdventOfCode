import pathlib


opponent = {
    'A': 'ROCK',
    'B': 'PAPER',
    'C': 'SCISSORS',
}
me = {
    'X': 'ROCK',
    'Y': 'PAPER',
    'Z': 'SCISSORS',
}
outcome = {
    'X': 'LOSS',
    'Y': 'DRAW',
    'Z': 'WIN',
}
shape_points = {
    'ROCK': 1,
    'PAPER': 2,
    'SCISSORS': 3,
}
outcome_points = {
    'LOSS': 0,
    'DRAW': 3,
    'WIN': 6,
}


def load_data(path: pathlib.Path) -> list[str]:
    with open(path, 'r') as file:
        return file.readlines()


def game_outcome(player1: str, player2: str) -> int:
    if player1 == 'ROCK':
        if player2 == 'ROCK':
            return 3
        if player2 == 'PAPER':
            return 6
        if player2 == 'SCISSORS':
            return 0
    if player1 == 'PAPER':
        if player2 == 'ROCK':
            return 0
        if player2 == 'PAPER':
            return 3
        if player2 == 'SCISSORS':
            return 6
    if player1 == 'SCISSORS':
        if player2 == 'ROCK':
            return 6
        if player2 == 'PAPER':
            return 0
        if player2 == 'SCISSORS':
            return 3
    raise ValueError("Invalid player input")


def shape_played(player1: str, result: str) -> str:
    if player1 == 'ROCK':
        if result == 'LOSS':
            return 'SCISSORS'
        if result == 'DRAW':
            return 'ROCK'
        if result == 'WIN':
            return 'PAPER'
    if player1 == 'PAPER':
        if result == 'LOSS':
            return 'ROCK'
        if result == 'DRAW':
            return 'PAPER'
        if result == 'WIN':
            return 'SCISSORS'
    if player1 == 'SCISSORS':
        if result == 'LOSS':
            return 'PAPER'
        if result == 'DRAW':
            return 'SCISSORS'
        if result == 'WIN':
            return 'ROCK'
    raise ValueError("Invalid player input")


def process_data_1(data: list[str]) -> int:
    split_lines = (item.strip().split(' ') for item in data)
    replacement = [(opponent[item[0]], me[item[1]]) for item in split_lines]
    total_shape_points = sum(shape_points[item[1]] for item in replacement)
    total_game_points = sum(game_outcome(item[0], item[1]) for item in replacement)
    return total_shape_points + total_game_points


def process_data_2(data: list[str]) -> int:
    split_lines = (item.strip().split(' ') for item in data)
    replacement = [(opponent[item[0]], shape_played(opponent[item[0]], outcome[item[1]])) for item in split_lines]
    total_shape_points = sum(shape_points[item[1]] for item in replacement)
    total_game_points = sum(game_outcome(item[0], item[1]) for item in replacement)
    return total_shape_points + total_game_points


def test():
    dummy_data = ['A Y', 'B X', 'C Z']
    assert 15 == process_data_1(dummy_data)
    assert 12 == process_data_2(dummy_data)


if __name__ == "__main__":
    test()
    input_data = load_data(pathlib.Path('input.txt'))
    print(process_data_1(input_data))
    print(process_data_2(input_data))
