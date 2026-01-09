def hex_to_int(c):
    return int(c, 16)


with open("output.txt", "r") as f:
    lines = [line.strip() for line in f if line.strip()]
    maze = []
    i = 0
    while all(c in "0123456789ABCDEF" for c in lines[i]):
        maze.append(lines[i])
        i += 1
    h = len(maze)
    w = len(maze[0])

    ph = h * 2 + 1
    pw = w * 2 + 1

    # Initialize with walls (1)
    pixels = [['█' for _ in range(pw)] for _ in range(ph)]

    for y in range(h):
        for x in range(w):
            cell = hex_to_int(maze[y][x])

            px = 2 * x + 1
            py = 2 * y + 1

            # Cell space
            pixels[py][px] = ' '

            # Open walls if bit == 0
            if not (cell & 1):  # North
                pixels[py - 1][px] = ' '
            if not (cell & 2):  # East
                pixels[py][px + 1] = ' '
            if not (cell & 4):  # South
                pixels[py + 1][px] = ' '
            if not (cell & 8):  # West
                pixels[py][px - 1] = ' '

    entry = tuple(map(int, lines[i].split(",")))
    exit_ = tuple(map(int, lines[i + 1].split(",")))
    directions = lines[i + 2]

    for y in range(h * 2 + 1):
        for x in range(w * 2 + 1):
            if y == entry[1] and x == entry[0]:
                print("\033[35m██\033[0m", end='')
            elif y == exit_[1] and x == exit_[0]:
                print("\033[36m██\033[0m", end='')
            else:
                print(pixels[y][x]+pixels[y][x], end='')
        print()

    x, y = entry
    for op in directions:
        if op == 'N':
            y -= 1
        elif op == 'E':
            x += 1
        elif op == 'S':
            y += 1
        elif op == 'W':
            x -= 1
    if x == exit_[0] and y == exit_[1]:
        print("\033[32msuccess\033[0m")
    else:
        print("\033[31merror\033[0m")
