import numpy as np
from numpy import ndarray


def load_data(file_path: str) -> list[str]:
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]


def create_matrix(data: list[str]) -> ndarray:
    list_matrix = [[int(digit) for digit in row] for row in data]
    matrix = np.array(list_matrix)
    return matrix


def visible_edge_trees(matrix: ndarray) -> int:
    return sum(2 * matrix.shape) - 4


def visible_interior_trees(matrix: ndarray) -> int:
    top_down = top_down_visibility(matrix)
    left_right = left_right_visibility(matrix)
    visible_trees = top_down + left_right
    return len(np.nonzero(visible_trees)[0])


def top_down_visibility(matrix: ndarray) -> ndarray:
    visible_trees = np.zeros_like(matrix)
    for col in range(1, matrix.shape[1] - 1):
        forest_column = matrix[:, col]
        top_tree_height = forest_column[0]
        while True:
            index = top_left_visibility(forest_column, top_tree_height)
            if index == -1:
                break
            visible_trees[index, col] = 1
            top_tree_height = forest_column[index]

        down_tree_height = forest_column[-1]
        while True:
            index = down_right_visibility(forest_column, down_tree_height)
            if index == -1:
                break
            visible_trees[index, col] = 1
            down_tree_height = forest_column[index]
        visible_trees[0, col] = 0
        visible_trees[-1, col] = 0
    return visible_trees


def left_right_visibility(matrix: ndarray) -> ndarray:
    visible_trees = np.zeros_like(matrix)
    for row in range(1, matrix.shape[0] - 1):
        forest_row = matrix[row, :]
        left_tree_height = forest_row[0]
        while True:
            index = top_left_visibility(forest_row, left_tree_height)
            if index == -1:
                break
            visible_trees[row, index] = 1
            left_tree_height = forest_row[index]

        right_tree_height = forest_row[-1]
        while True:
            index = down_right_visibility(forest_row, right_tree_height)
            if index == -1:
                break
            visible_trees[row, index] = 1
            right_tree_height = forest_row[index]
        visible_trees[row, 0] = 0
        visible_trees[row, -1] = 0
    return visible_trees


def top_left_visibility(forest_row: ndarray, height: int) -> int:
    higher_trees = forest_row - height
    try:
        return min(np.argwhere(higher_trees > 0))
    except ValueError:
        return -1


def down_right_visibility(forest_row: ndarray, height: int) -> int:
    higher_trees = forest_row - height
    try:
        return max(np.argwhere(higher_trees > 0))
    except ValueError:
        return -1


def scenic_score(matrix: ndarray) -> int:
    highest_score = 0
    for i in range(1, matrix.shape[0] - 1):
        for j in range(1, matrix.shape[1] - 1):
            this_tree = matrix[i, j]
            top = top_scenery(matrix[:i, j], this_tree)
            down = down_scenery(matrix[i+1:, j], this_tree)
            left = left_scenery(matrix[i, :j], this_tree)
            right = right_scenery(matrix[i, j+1:], this_tree)
            score = top * down * left * right
            if score > highest_score:
                highest_score = score
    return highest_score


def top_scenery(forest_row: ndarray, height: int) -> int:
    higher_trees = forest_row - height
    try:
        return len(forest_row) - np.max(np.argwhere(higher_trees >= 0))
    except ValueError:
        return len(forest_row)


def down_scenery(forest_row: ndarray, height: int) -> int:
    higher_trees = forest_row - height
    try:
        return np.min(np.argwhere(higher_trees >= 0)) + 1
    except ValueError:
        return len(forest_row)


def left_scenery(forest_row: ndarray, height: int) -> int:
    higher_trees = forest_row - height
    try:
        return len(forest_row) - np.max(np.argwhere(higher_trees >= 0))
    except ValueError:
        return len(forest_row)


def right_scenery(forest_row: ndarray, height: int) -> int:
    higher_trees = forest_row - height
    try:
        return np.min(np.argwhere(higher_trees >= 0)) + 1
    except ValueError:
        return len(forest_row)


def test() -> None:
    input_data = [
        "30373",
        "25512",
        "65332",
        "33549",
        "35390",
    ]
    matrix = create_matrix(input_data)
    assert 16 == visible_edge_trees(matrix)
    assert 5 == visible_interior_trees(matrix)
    assert 21 == visible_edge_trees(matrix) + visible_interior_trees(matrix)
    assert 8 == scenic_score(matrix)


if __name__ == '__main__':
    test()
    matrix = create_matrix(load_data('input.txt'))
    print(visible_edge_trees(matrix) + visible_interior_trees(matrix))
    print(scenic_score(matrix))
