from dataclasses import dataclass


def load_data(file_path: str) -> list[str]:
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]


@dataclass(frozen=True)
class Coordinates:
    x: int
    y: int

    def touches(self, other: "Coordinates") -> bool:
        if abs(self.x - other.x) > 1:
            return False
        if abs(self.y - other.y) > 1:
            return False
        return True


def tail_move(tail: Coordinates, head: Coordinates) -> Coordinates:
    if tail.touches(head):
        return tail

    # Same column
    if tail.x == head.x:
        if tail.y > head.y:
            return Coordinates(tail.x, tail.y - 1)
        else:
            return Coordinates(tail.x, tail.y + 1)
    # Same row
    if tail.y == head.y:
        if tail.x > head.x:
            return Coordinates(tail.x - 1, tail.y)
        else:
            return Coordinates(tail.x + 1, tail.y)
    # Left Diagonals
    if tail.x > head.x:
        if tail.y > head.y:
            return Coordinates(tail.x - 1, tail.y - 1)
        else:
            return Coordinates(tail.x - 1, tail.y + 1)
    if tail.x < head.x:
        if tail.y < head.y:
            return Coordinates(tail.x + 1, tail.y + 1)
        else:
            return Coordinates(tail.x + 1, tail.y - 1)

    raise ValueError("Invalid direction.")


def tail_positions(coordinates: list[Coordinates]) -> int:
    return len(set(coordinates))


def head_movements(move: str, current_head: Coordinates) -> list[Coordinates]:
    new_heads = [current_head]
    direction, distance = move.split(' ')
    distance = int(distance)
    if direction == 'R':
        for i in range(distance):
            new_head = Coordinates(new_heads[-1].x + 1, new_heads[-1].y)
            new_heads.append(new_head)
        return new_heads[1:]
    if direction == 'L':
        for i in range(distance):
            new_head = Coordinates(new_heads[-1].x - 1, new_heads[-1].y)
            new_heads.append(new_head)
        return new_heads[1:]
    if direction == 'U':
        for i in range(distance):
            new_head = Coordinates(new_heads[-1].x, new_heads[-1].y + 1)
            new_heads.append(new_head)
        return new_heads[1:]
    if direction == 'D':
        for i in range(distance):
            new_head = Coordinates(new_heads[-1].x, new_heads[-1].y - 1)
            new_heads.append(new_head)
        return new_heads[1:]
    raise ValueError("Invalid direction.")


def simulate_large_movement(data: list[str], n_tail: int) -> list[Coordinates]:
    head_moves = [Coordinates(0, 0)]
    for move in data:
        head_moves.extend(head_movements(move, head_moves[-1]))
    for tail in range(n_tail):
        tail_moves = []
        current_tail = Coordinates(0, 0)
        for new_head in head_moves[1:]:
            new_tail = tail_move(current_tail, new_head)
            current_tail = new_tail
            tail_moves.append(new_tail)
        head_moves = tail_moves
    return head_moves


def test():
    data = [
        "R 4",
        "U 4",
        "L 3",
        "D 1",
        "R 4",
        "D 1",
        "L 5",
        "R 2",
    ]
    positions = simulate_large_movement(data, 1)
    assert 13 == tail_positions(positions)
    positions2 = simulate_large_movement(data, 9)
    assert 1 == tail_positions(positions2)
    data2 = [
        "R 5",
        "U 8",
        "L 8",
        "D 3",
        "R 17",
        "D 10",
        "L 25",
        "U 20",
    ]
    positions3 = simulate_large_movement(data2, 9)
    assert 36 == tail_positions(positions3)


if __name__ == '__main__':
    test()
    positions1 = simulate_large_movement(load_data('input.txt'), 1)
    print(tail_positions(positions1))
    positions2 = simulate_large_movement(load_data('input.txt'), 9)
    print(tail_positions(positions2))
