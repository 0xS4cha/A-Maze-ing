#!/usr/bin/env python3

import sys
import exception
import config
import algorithms.backtracking as backtracking
import algorithms.eller as eller


def print_maze(maze: list[list[int]], empty, full, start_point, end_point):
    start_x, start_y = start_point
    end_x, end_y = end_point
    for line in range(len(maze)):
        for column in range(len(maze[line])):
            if maze[line][column] == 1:
                print(full, end="")
            else:
                print(empty, end="")
        print()


def generate_maze(_config) -> bool:
    algo_list = [backtracking, eller]
    result = algo_list[_config.ALGORITHMS].generate(_config)
    print_maze(result, _config.EMPTY_CHAR, _config.FULL_CHAR, _config.ENTRY, _config.EXIT)
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
