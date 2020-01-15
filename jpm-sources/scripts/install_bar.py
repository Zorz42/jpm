import os


def install_bar(current, total, _):
    width = os.get_terminal_size().columns - 2
    print("\r[", end='')
    for i in range(int(width / total * current)):
        print(chr(9608), end='')
    for i in range(int(width / total * (total - current))):
        print(" ", end='')
    print("]", end='', flush=True)
