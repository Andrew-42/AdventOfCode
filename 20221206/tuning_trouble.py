def load_data(file_path: str) -> str:
    with open(file_path, 'r') as file:
        return file.readlines()[0]


def get_packet_marker_position(data: str) -> int:
    for i in range(len(data)):
        if len(set(data[i:i+4])) == 4:
            return i + 4
    raise ValueError("Invalid data.")


def get_message_marker_position(data: str) -> int:
    for i in range(len(data)):
        if len(set(data[i:i+14])) == 14:
            return i + 14
    raise ValueError("Invalid data.")


def test() -> None:
    test_packet_data = [
        "bvwbjplbgvbhsrlpgdmjqwftvncz",
        "nppdvjthqldpwncqszvftbrmjlhg",
        "nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg",
        "zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw",
    ]
    assert 5 == get_packet_marker_position(test_packet_data[0])
    assert 6 == get_packet_marker_position(test_packet_data[1])
    assert 10 == get_packet_marker_position(test_packet_data[2])
    assert 11 == get_packet_marker_position(test_packet_data[3])
    test_message_data = [
        "mjqjpqmgbljsphdztnvjfqwrcgsmlb",
        "bvwbjplbgvbhsrlpgdmjqwftvncz",
        "nppdvjthqldpwncqszvftbrmjlhg",
        "nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg",
        "zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw",
    ]
    assert 19 == get_message_marker_position(test_message_data[0])
    assert 23 == get_message_marker_position(test_message_data[1])
    assert 23 == get_message_marker_position(test_message_data[2])
    assert 29 == get_message_marker_position(test_message_data[3])
    assert 26 == get_message_marker_position(test_message_data[4])


if __name__ == '__main__':
    test()
    data = load_data('input.txt')
    print(get_packet_marker_position(data))
    print(get_message_marker_position(data))
