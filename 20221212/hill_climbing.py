import heapq
from copy import deepcopy
from dataclasses import dataclass, field
from typing import Optional


ELEVATION = 'abcdefghijklmnopqrstuvwxyz'


def load_data(file_path: str) -> list[list[str]]:
    with open(file_path, 'r') as file:
        return [list(line.strip()) for line in file.readlines()]


@dataclass
class Node:
    x: int
    y: int
    cost: int
    parent: Optional['Node'] = field(compare=False, default=None)

    def get_position(self) -> tuple[int, int]:
        return self.x, self.y

    def __lt__(self, other: 'Node') -> bool:
        if self.x < other.x:
            return True
        if self.y < other.y:
            return True
        return False


@dataclass
class Problem:
    map: list[list[str]]
    _terminal: Node = None

    def __post_init__(self) -> None:
        self._terminal = self.get_terminal()

    def get_initial(self) -> Node:
        for i, row in enumerate(self.map):
            try:
                j = row.index('S')
                self.map[i][j] = 'a'
                return Node(x=j, y=i, cost=0, parent=None)
            except ValueError:
                continue
        raise ValueError('There must be an initial node.')

    def is_terminal(self, node: Node) -> bool:
        return (self._terminal.x == node.x) & (self._terminal.y == node.y)

    def get_terminal(self) -> Node:
        for i, row in enumerate(self.map):
            try:
                j = row.index('E')
                self.map[i][j] = 'z'
                return Node(x=j, y=i, cost=0, parent=None)
            except ValueError:
                continue
        raise ValueError('There must be a terminal node.')

    def distance_to_terminal(self, node: Node) -> int:
        return abs(self._terminal.x - node.x) + abs(self._terminal.y - node.y)

    def expand(self, node: Node) -> list[Node]:
        nodes = []
        el_index = ELEVATION.index(self.map[node.y][node.x])
        new_els = ELEVATION[:min(len(ELEVATION), el_index + 2)]
        try:
            if self.map[max(0, node.y - 1)][node.x] in new_els:
                nodes.append(Node(x=node.x, y=max(0, node.y - 1), parent=None, cost=node.cost + 1))
        except IndexError:
            pass
        try:
            if self.map[node.y + 1][node.x] in new_els:
                nodes.append(Node(x=node.x, y=node.y + 1, parent=None, cost=node.cost + 1))
        except IndexError:
            pass
        try:
            if self.map[node.y][max(0, node.x - 1)] in new_els:
                nodes.append(Node(x=max(0, node.x - 1), y=node.y, parent=None, cost=node.cost + 1))
        except IndexError:
            pass
        try:
            if self.map[node.y][node.x + 1] in new_els:
                nodes.append(Node(x=node.x + 1, y=node.y, parent=None, cost=node.cost + 1))
        except IndexError:
            pass
        return nodes


def shortest_path(problem: Problem) -> Optional[Node]:
    init_node = problem.get_initial()
    frontier = []
    heapq.heappush(frontier, (0, init_node))
    reached: dict[tuple[int, int], Node] = {init_node.get_position(): init_node}
    while len(frontier) > 0:
        node = heapq.heappop(frontier)[1]
        if problem.is_terminal(node):
            return node
        for child in problem.expand(node):
            if (child.get_position() not in reached) or (child.cost < reached[child.get_position()].cost):
                reached[child.get_position()] = child
                heapq.heappush(frontier, (child.cost + problem.distance_to_terminal(child), child))
    return None


def shortest_a_path(map: list[list[str]]) -> int:
    shortest = 500
    problem_a = deepcopy(map)
    problem_a[0][0] = 'a'
    count = 0
    for j in range(len(problem_a[0])):
        for i in range(len(problem_a)):
            if problem_a[i][j] == 'a':
                new_map = deepcopy(problem_a)
                new_map[i][j] = 'S'
                node = shortest_path(Problem(new_map))
                if node is None:
                    continue
                if node.cost < shortest:
                    shortest = node.cost
                count += 1
                if count > 60:
                    return shortest
    return shortest


def path_length(node: Node) -> int:
    length = 0
    current_node = node
    while True:
        if current_node is None:
            break
        length += 1
        current_node = node.parent
    return length


def test():
    data = [
        "Sabqponm",
        "abcryxxl",
        "accszExk",
        "acctuvwj",
        "abdefghi",
    ]
    assert 31 == shortest_path(Problem([list(row) for row in data])).cost
    assert 29 == shortest_a_path([list(row) for row in data])


if __name__ == '__main__':
    test()
    print(shortest_path(Problem(load_data('input.txt'))))
    print(shortest_a_path(load_data('input.txt')))
