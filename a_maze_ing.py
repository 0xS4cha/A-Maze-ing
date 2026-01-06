#!/usr/bin/env python3

import sys
import exception
import config
import algorithms.backtracking as backtracking
import algorithms.eller as eller
import mlx


def print_maze(maze: list[list[int]], empty, full):
    for line in range(len(maze)):
        for column in range(len(maze[line])):
            if maze[line][column] == 0:
                print(empty, end="")
            elif maze[line][column] == 1:
                print(full, end="")
            elif maze[line][column] == 2:
                print(config.COLOR_STARTING + full + config.COLOR_RESET, end='')
            elif maze[line][column] == 3:
                print(config.COLOR_ENDING + full + config.COLOR_RESET, end='')
        print()


def generate_maze(_config: config.Config) -> bool:
    algo_list = [backtracking, eller]
    result: list[list[int]] = algo_list[_config.ALGORITHMS].generate(_config)
    # set entry and exit
    entry_x, entry_y = _config.ENTRY
    exit_x, exit_y = _config.EXIT
    if (entry_x < 1 or entry_y < 1 or entry_x > _config.WIDTH - 2 or entry_y > _config.HEIGHT - 2) \
            or (entry_x == exit_x and entry_y == exit_y):
        raise exception.ConfigException("Invalid entry or exit position, outside the map")
    result[entry_y][entry_x] = 2
    result[exit_y][exit_x] = 3
    print_maze(result, _config.EMPTY_CHAR, _config.FULL_CHAR)
    return True


def main():
    if len(sys.argv) <= 1:
        raise exception.ArgsException("Not enough arguments")
    try:
        _config = config.Config(sys.argv[1])
    except Exception as e:
        raise exception.ConfigException(f"Bad config file: {e}")
    generate_maze(_config)


if __name__ == "__main__":
    try:
        main()
    except (exception.ArgsException, exception.ConfigException) as e:
        exception.display_errors(e)
    except Exception as e:
        exception.display_errors(f"An unexpected error occurred: {e}")
