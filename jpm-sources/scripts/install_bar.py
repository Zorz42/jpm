from os import get_terminal_size


def install_bar(current, total, _):
    width = get_terminal_size().columns - 2
    print("\r[", end='')
    for i in range(int(width / total * current)):
        print(chr(9608), end='')
    for i in range(int(width / total * (total - current))):
        print(" ", end='')
    print("]", end='', flush=True)
