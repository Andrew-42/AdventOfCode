from dataclasses import dataclass


def load_data(file_path: str) -> list[str]:
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]


@dataclass
class Node:
    name: str
    file_sizes: int = 0
    total_size: int = 0
    children: list["Node"] = None
    parent: "Node" = None


def separate_on_dir_step(data: list[str]) -> list[list[str]]:
    cd_separated = []
    dir_content = []
    total_size = len(data)
    for i, line in enumerate(data):
        if line == '$ cd ..':
            if len(dir_content) > 0:
                cd_separated.append(dir_content)
            cd_separated.append([line])
            dir_content = []
            continue
        if line.startswith('$ cd'):
            if len(dir_content) > 0:
                cd_separated.append(dir_content)
            dir_content = [line]
            continue
        dir_content.append(line)
        if i == (total_size - 1):
            if len(dir_content) > 0:
                cd_separated.append(dir_content)
    return cd_separated


def count_file_size(data: list[str]) -> int:
    file_size = 0
    for line in data:
        size = line.split(' ')[0]
        try:
            file_size += int(size)
        except ValueError:
            continue
    return file_size


def add_node(separated_data: list[list[str]]) -> tuple[Node, list[list[str]]]:
    folder_data = separated_data[0]
    new_separated_data = separated_data[1:]
    node = Node(name=folder_data[0].split(' ')[2])
    assert '$ ls' == folder_data[1]
    node.file_sizes = count_file_size(folder_data[2:])
    node.total_size = node.file_sizes
    node.children = list()
    children_nodes = [child for child in folder_data[2:] if child.startswith('dir')]
    for cd_child_node in children_nodes:
        assert cd_child_node.split(' ')[1] == new_separated_data[0][0].split(' ')[2]
        child_node, new_separated_data = add_node(new_separated_data)
        child_node.parent = node
        node.total_size += child_node.total_size
        node.children.append(child_node)

    if len(new_separated_data) == 0:
        return node, []
    if new_separated_data[0][0] == '$ cd ..':
        return node, new_separated_data[1:]


def create_tree(data: list[str]) -> Node:
    separated_data = separate_on_dir_step(data)
    tree, data = add_node(separated_data)
    assert len(data) == 0
    return tree


def iterate_tree(node: Node, accumulator: list[Node]) -> list[Node]:
    new_accumulator = accumulator
    for child in node.children:
        new_accumulator = iterate_tree(child, new_accumulator)
    if node.total_size < 100_000:
        new_accumulator.append(node)
    return new_accumulator


def find_node(node: Node, lowest_node: Node, min_size: int) -> Node:
    node_delta = node.total_size - min_size
    delta = lowest_node.total_size - min_size
    if (node_delta > 0) & (node_delta < delta):
        new_low_node = node
    else:
        new_low_node = lowest_node

    for child in node.children:
        new_low_node = find_node(child, new_low_node, min_size)
    return new_low_node


def test():
    TOTAL_SPACE = 70000000
    data = [
        "$ cd /",
        "$ ls",
        "dir a",
        "14848514 b.txt",
        "8504156 c.dat",
        "dir d",
        "$ cd a",
        "$ ls",
        "dir e",
        "29116 f",
        "2557 g",
        "62596 h.lst",
        "$ cd e",
        "$ ls",
        "584 i",
        "$ cd ..",
        "$ cd ..",
        "$ cd d",
        "$ ls",
        "4060174 j",
        "8033020 d.log",
        "5626152 d.ext",
        "7214296 k",
    ]
    tree = create_tree(data)
    low_size_nodes = iterate_tree(tree, list())
    assert 95437 == sum([node.total_size for node in low_size_nodes])
    free_space = TOTAL_SPACE - tree.total_size
    assert 21618835 == free_space
    to_delete_at_least = 30000000 - free_space
    folder = find_node(tree, tree, to_delete_at_least)
    assert 'd' == folder.name
    assert 24933642 == folder.total_size


if __name__ == '__main__':
    test()
    tree = create_tree(load_data('input.txt'))
    print(sum([node.total_size for node in iterate_tree(tree, list())]))
    free_space = 70_000_000 - tree.total_size
    to_delete_at_least = 30_000_000 - free_space
    folder = find_node(tree, tree, to_delete_at_least)
    print(folder.total_size)
