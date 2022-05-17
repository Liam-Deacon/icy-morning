import random

def random_line(filename: str) -> str:
    selected: str = None
    with open(filename, 'r') as f:
        index = 0
        while not selected:
            line = f.readline()
            if random.randrange(index + 1) == 0:
                selected = line
    return selected


def random_line2(filename: str) -> str:
    selected: str = None
    line_count: int = 0
    with open(filename, 'r+') as f:
        eof: bool = False
        previous_pos: int = None
        while f.readline() and not eof:
            pos: int = f.tell()
            eof = pos == previous_pos
            previous_pos = pos
            line_count += 1
        selected_index: int = random.randint(0, line_count - 1)
        f.seek(0)
        for _ in range(selected_index + 1):
            selected = f.readline()
    return selected
