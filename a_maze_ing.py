#!/usr/bin/env python3

import sys
import src.mazegen.exception as exception
from mazegen import MazeGenerator


def main() -> None:
    """
    Main entry point for the maze generator application.
    Parses arguments, generates the maze, and handles the main event loop.

    Raises:
        exception.ArgsException: If insufficient arguments are provided.
        Exception: for any other critical failure during execution.
    """
    if len(sys.argv) <= 1:
        raise exception.ArgsException("Not enough arguments")
    try:
        maze_generator = MazeGenerator(sys.argv[1])
        maze = maze_generator.generate_maze()
        maze_generator.draw_control_buttons()
        maze_generator.draw_maze(maze)
        solution = maze_generator.get_solution(maze)
        print(f"solution is: {''.join(solution)}")
        maze_generator.draw_solution()
        if not maze_generator.generate_output(maze, solution):
            raise Exception("Could not build output file")
        else:
            print("Successfully built the output")
        maze_generator.run()
    except exception.ConfigException as e:
        print(f"Invalid config file: {e.args[0]}")
    except exception.MazeException as e:
        print(f"Maze generation failed: {e.args[0]}")
    except Exception as e:
        exception.display_errors(e.args[0])


if __name__ == "__main__":
    main()
    try:
        pass
    except SystemExit:
        pass
    except (exception.ArgsException, exception.ConfigException) as e:
        exception.display_errors(e.args[0])
    except Exception as e:
        exception.display_errors(f"An unexpected error occurred: {e.args[0]}")
