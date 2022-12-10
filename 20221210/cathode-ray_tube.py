
def load_data(file_path: str) -> list[str]:
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]


def signal_strengths(data: list[str]) -> list[int]:
    cycle = [1 for _ in range(2*len(data))]
    current_cycle = 0
    current_value = 1
    for line in data:
        if line == "noop":
            cycle[current_cycle + 1] = current_value
            current_cycle += 1
            continue
        if line.startswith('addx'):
            num = int(line.split(' ')[1])
            cycle[current_cycle + 1] = current_value
            cycle[current_cycle + 2] = current_value + num
            current_value += num
            current_cycle += 2
    return cycle


def calculate_signal_strength(cycles: list[int]) -> int:
    signals = []
    for i in range (20, 221, 40):
        strength = i * cycles[i - 1]
        signals.append(strength)
    return sum(signals)


def render_screen_row(cycles: list[int]) -> list[str]:
    assert 40 == len(cycles)
    screen_row = ['.' for _ in cycles]
    sprite = [0, 1, 2]
    for i, cycle_value in enumerate(cycles):
        sprite = [cycle_value - 1, cycle_value, cycle_value + 1]
        if i in sprite:
            screen_row[i] = '#'
    return ''.join(screen_row)


def test() -> None:
    data1 = [
        "noop",
        "addx 3",
        "addx -5",
    ]
    assert -1 == signal_strengths(data1)[5]
    data2 = load_data('test_input.txt')
    signals = signal_strengths(data2)
    assert 21 == signals[19]
    assert 19 == signals[59]
    assert 18 == signals[99]
    assert 21 == signals[139]
    assert 16 == signals[179]
    assert 18 == signals[219]
    assert 13140 == calculate_signal_strength(signals)
    assert "##..##..##..##..##..##..##..##..##..##.." == render_screen_row(signals[:40])
    assert "###...###...###...###...###...###...###." == render_screen_row(signals[40:80])
    assert "####....####....####....####....####...." == render_screen_row(signals[80:120])
    assert "#####.....#####.....#####.....#####....." == render_screen_row(signals[120:160])
    assert "######......######......######......####" == render_screen_row(signals[160:200])
    assert "#######.......#######.......#######....." == render_screen_row(signals[200:240])


if __name__ == '__main__':
    test()
    input_data = load_data('input.txt')
    parsed_signals = signal_strengths(input_data)
    print(calculate_signal_strength(parsed_signals))
    for i in range(0, 240, 40):
        print(render_screen_row(parsed_signals[i:i+40]))
