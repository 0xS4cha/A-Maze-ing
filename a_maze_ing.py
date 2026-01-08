#!/usr/bin/env python3

import sys
import src.mazegen.exception as exception
from mazegen import MazeGenerator


def main():
    if len(sys.argv) <= 1:
        raise exception.ArgsException("Not enough arguments")
    try:
        maze_generator = MazeGenerator(sys.argv[1])
        maze = maze_generator.generate_maze()
        maze_generator.draw_control_buttons()
        maze_generator.draw_maze(maze)
        maze_generator.run()
    except Exception as e:
        raise exception.ConfigException(f"Bad config file: {e}")


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        pass
    except (exception.ArgsException, exception.ConfigException) as e:
        exception.display_errors(e)
    except Exception as e:
        exception.display_errors(f"An unexpected error occurred: {e}")
