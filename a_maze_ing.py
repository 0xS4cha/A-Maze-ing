#!/usr/bin/env python3

import sys
import exception
import config
import recursive_backtracker


def generate_maze(config) -> bool:
    algo_list = [recursive_backtracker]
    return (algo_list[config.algo].generate(config))


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
