#!/usr/bin/env python3
"""Main module for the Maze Generator application logic."""

import random
from . import exception
from . import config
import secrets
from mlx import Mlx
from .utils.mlx_utils import manage_expose, manage_close, manage_key_simple
from .utils.mlx_utils import XVar, render_maze_to_mlx, \
                            calculate_window_size
from .utils.maze_utils import generate_maze as utils_generate_maze
from .utils.buttons import mouse_handler, buttons_init, \
                           draw_buttons, button_toggle_path
from .resolve import resolve
from .parser import generate_output as parser_generate_output


class MazeGenerator:
    """A class to generate, solve, and visualize mazes using MLX."""

    def __init__(
            self,
            path: str,
            seed: str = "0",
            size: tuple[int, int] = (-1, -1)
            ) -> None:
        """
        Initialize the maze generator with a configuration file.

        Args:
            path (str): The path to the configuration file.
            seed (str): The seed for random number generation. Defaults to "0".
            size (tuple[int, int]): Optional override for maze size.

        Raises:
            exception.ConfigException: If the configuration is invalid or MLX
            cannot be initialized.
        """
        self.__xvar = XVar()
        try:
            self.__xvar.mlx = Mlx()
        except Exception as e:
            raise exception.ConfigException(f"Can't initialize MLX: {e}")

        self.__config = config.Config(path)
        if (size[0] != -1 and size[1] != -1):
            self.__config.WIDTH, self.__config.HEIGHT = size

        try:
            if self.__config.EXIT[0] < 0 or \
                    self.__config.EXIT[0] > self.__config.WIDTH:
                raise Exception(f"EXIT X position is out of range \
(min 0, max {self.__config.WIDTH})")
            if self.__config.EXIT[1] < 0 or \
                    self.__config.EXIT[1] > self.__config.HEIGHT:
                raise Exception(f"EXIT Y position is out of range \
(min 0, max {self.__config.HEIGHT})")
            if self.__config.ENTRY[0] < 0 or \
                    self.__config.ENTRY[0] > self.__config.WIDTH:
                raise Exception(f"ENTRY X position is out of range \
(min 0, max {self.__config.WIDTH})")
            if self.__config.ENTRY[1] < 0 or \
                    self.__config.ENTRY[1] > self.__config.HEIGHT:
                raise Exception(f"ENTRY Y position is out of range \
(min 0, max {self.__config.HEIGHT})")
            new_seed = self.__config.SEED
            if new_seed == "0":
                new_seed = secrets.token_hex(8)
            if (seed != "0"):
                new_seed = seed
            random.seed(new_seed)
            self.__config.SEED = new_seed
            self.__xvar.mlx_ptr = self.__xvar.mlx.mlx_init()
            ret, self.__xvar.screen_w, self.__xvar.screen_h =\
                self.__xvar.mlx.mlx_get_screen_size(self.__xvar.mlx_ptr)

            required_w, required_h, _ = calculate_window_size(
                self.__config,
                self.__xvar.screen_w,
                self.__xvar.screen_h,
                ui_width=250
            )

            self.__xvar.win_w = required_w
            self.__xvar.win_h = required_h
            self.__xvar.win_1 = self.__xvar.mlx.mlx_new_window(
                self.__xvar.mlx_ptr, required_w,
                required_h,
                "A-Maze-ing"
            )
            if not self.__xvar.win_1:
                raise Exception("Can't create MLX window")

            self.__xvar.mlx.mlx_mouse_hook(
                self.__xvar.win_1,
                mouse_handler,
                self.__xvar
            )
            self.__xvar.mlx.mlx_key_hook(
                self.__xvar.win_1,
                manage_key_simple,
                self.__xvar
            )
            self.__xvar.mlx.mlx_hook(
                self.__xvar.win_1,
                33, 0,
                manage_close,
                self.__xvar
            )
            self.__xvar.mlx.mlx_expose_hook(
                self.__xvar.win_1,
                self.__main_expose,
                self.__xvar
            )
        except Exception as e:
            raise exception.ConfigException(f"MLX error: {e}")

    def __main_expose(self, xvar: XVar) -> None:
        """
        Handle window exposure events (redraws buttons).

        Args:
            xvar (XVar): The variable container.
        """
        manage_expose(xvar)
        draw_buttons(xvar)

    def generate_maze(self) -> list[list[int]]:
        """
        Generate a maze based on the loaded configuration.

        Returns:
            list[list[int]]: The generated maze as a 2D grid.
        """

        self.__xvar.maze_data = utils_generate_maze(self.__config, self.__xvar)
        return self.__xvar.maze_data

    def draw_maze(self, maze: list[list[int]]) -> None:
        """
        Render the maze to the MLX window.

        Args:
            maze (list[list[int]]): The maze grid to draw.
        """
        render_maze_to_mlx(
            self.__xvar.mlx,
            self.__xvar.mlx_ptr,
            self.__xvar.win_1,
            maze,
            self.__config,
            self.__xvar
        )

    def draw_control_buttons(self) -> None:
        """
        Initialize and draw the control buttons on the window.
        """
        buttons_init(self.__config, self.__xvar)
        draw_buttons(self.__xvar)

    def get_solution(self, maze: list[list[int]]) -> list[tuple[int, int]]:
        """
        Solve the maze and return the solution path.

        Args:
            maze (list[list[int]]): The maze grid.

        Returns:
            list[tuple[int, int]]: The solution path as a list of coordinates.

        Raises:
            exception.MazeException: If no solution is found.
        """
        pos = tuple(self.__config.ENTRY)
        result = resolve(
            pos,
            0,
            maze,
            None,
            self.__config,
            self.__xvar
        )
        if type(result) is list:
            return result
        else:
            raise exception.MazeException("The maze has no possible solution")

    def draw_solution(self) -> None:
        """
        Highlight the solution path on the window.
        """
        button_toggle_path(self.__config, self.__xvar, True)

    def hide_solution(self) -> None:
        """
        Hide the solution path on the window.
        """
        button_toggle_path(self.__config, self.__xvar, False)

    def generate_output(self, maze: list[list[int]],
                        solution: list[tuple]) -> bool:
        """
        Write the maze and solution to the output file.

        Args:
            maze (list[list[int]]): The maze grid.
            solution (list[tuple]): The solution path.

        Returns:
            bool: True if successful, False otherwise.
        """
        return parser_generate_output(
            maze,
            solution,
            self.__config
        )

    def run(self) -> None:
        """
        Start the MLX event loop.
        """
        self.__xvar.mlx.mlx_loop(self.__xvar.mlx_ptr)
        self.__xvar.mlx.mlx_destroy_window(
            self.__xvar.mlx_ptr,
            self.__xvar.win_1
        )
        self.__xvar.mlx.mlx_release(self.__xvar.mlx_ptr)
