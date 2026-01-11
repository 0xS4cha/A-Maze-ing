import sys
import os
from typing import Any
import pytest
from unittest.mock import MagicMock, patch
import importlib

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.mazegen.utils import maze_utils  # noqa: E402
from src.mazegen import exception  # noqa: E402
from src.mazegen.MazeGenerator import MazeGenerator  # noqa: E402

mg_module = importlib.import_module("src.mazegen.MazeGenerator")


class MockConfig:
    """Mock configuration to isolate tests."""
    def __init__(self, path: str = "") -> None:
        self.WIDTH = 51
        self.HEIGHT = 51
        self.SEED = "0"
        self.PERFECT = False
        self.ENTRY = [1, 1]
        self.EXIT = [49, 49]
        self.ANIMATION = False
        self.COLORS: list[dict[int, int]] = [{}, {}, {}, {}, {}]
        self.DELAY = 0


class MockXVar:
    """Mock for the XVar graphics context."""
    def __init__(self) -> None:
        self.mlx = MagicMock()
        self.mlx_ptr = MagicMock()
        self.win_1 = MagicMock()
        self.show_path = False
        self.path: list[str] = []
        self.screen_w = 1920
        self.screen_h = 1080
        self.color_palette = 0
        self.img = None
        self.img_data = None


def test_add_symbol_perfect() -> None:
    """Verifies that the symbol is added correctly in a perfect maze."""
    width, height = 50, 50
    maze = [[1 for _ in range(width)] for _ in range(height)]

    maze_utils.add_symbol(maze, maze_utils.ft_symbol)

    found_symbol = False
    for row in maze:
        if 2 in row:
            found_symbol = True
            break
    assert found_symbol, "The symbol (value 2) should be present in the maze"


def test_add_symbol_imperfect() -> None:
    """Verifies that the symbol is added correctly in an imperfect maze."""
    width, height = 50, 50
    maze = [[1 for _ in range(width)] for _ in range(height)]

    maze_utils.add_symbol(maze, maze_utils.ft_symbol)

    found_symbol = False
    for row in maze:
        if 2 in row:
            found_symbol = True
            break
    assert found_symbol, "The symbol (value 2) should be present in the maze"


@patch.object(mg_module, 'Mlx')
@patch('src.mazegen.config.Config', side_effect=MockConfig)
@patch('src.mazegen.utils.maze_utils.resolve')
@patch('src.mazegen.utils.maze_utils.prim')
def test_generate_maze_prim_success(mock_prim: Any,
                                    mock_resolve: Any,
                                    MockConfigClass: Any,
                                    MockMlx: Any) -> None:
    """Tests the full maze generation flow with Prim algorithm (mocked)."""
    # Setup mocks
    mock_instance = MockMlx.return_value
    mock_instance.mlx_init.return_value = MagicMock()
    mock_instance.mlx_get_screen_size.return_value = (0, 1920, 1080)
    mock_instance.mlx_new_window.return_value = MagicMock()

    # The maze that will be "generated"
    config = MockConfig()
    fake_maze = [[1 for _ in range(config.WIDTH)]
                 for _ in range(config.HEIGHT)]
    mock_prim.generate.return_value = fake_maze
    mock_resolve.return_value = [(1, 1), (2, 2)]

    # Instantiate MazeGenerator
    gen = MazeGenerator("dummy_path")

    # Run generation
    result = gen.generate_maze()

    assert result is not None
    assert len(result) == config.HEIGHT
    assert len(result[0]) == config.WIDTH

    mock_prim.generate.assert_called_once()


@patch.object(mg_module, 'Mlx')
@patch('src.mazegen.config.Config', side_effect=MockConfig)
@patch('src.mazegen.utils.maze_utils.resolve')
@patch('src.mazegen.utils.maze_utils.stacking')
def test_generate_maze_stacking_success(mock_stacking: Any,
                                        mock_resolve: Any,
                                        MockConfigClass: Any,
                                        MockMlx: Any) -> None:
    """Tests the full maze generation flow with
    stacking algorithm (mocked)."""
    # Setup mocks
    mock_instance = MockMlx.return_value
    mock_instance.mlx_init.return_value = MagicMock()
    mock_instance.mlx_get_screen_size.return_value = (0, 1920, 1080)
    mock_instance.mlx_new_window.return_value = MagicMock()

    # Configure for perfect maze (stacking)
    def custom_config(path: str = ""):
        c = MockConfig()
        c.PERFECT = True
        return c
    MockConfigClass.side_effect = custom_config

    config = custom_config()  # just for assertions

    fake_maze = [[1 for _ in range(config.WIDTH)]
                 for _ in range(config.HEIGHT)]
    mock_stacking.generate.return_value = fake_maze
    mock_resolve.return_value = [(1, 1), (2, 2)]

    # Instantiate MazeGenerator
    gen = MazeGenerator("dummy_path")

    # Run generation
    result = gen.generate_maze()

    assert result is not None
    assert len(result) == config.HEIGHT
    assert len(result[0]) == config.WIDTH

    mock_stacking.generate.assert_called_once()


@patch.object(mg_module, 'Mlx')
@patch('src.mazegen.config.Config', side_effect=MockConfig)
def test_generate_maze_invalid_entry_exit(MockConfigClass: Any,
                                          MockMlx: Any) -> None:
    """Verifies that MazeGenerator raises an
    exception if entry/exit are invalid."""

    mock_instance = MockMlx.return_value
    mock_instance.mlx_init.return_value = MagicMock()

    def custom_config(path: str = ""):
        c = MockConfig()
        c.ENTRY = [123, 10]
        c.EXIT = [-1, 10]
        return c
    MockConfigClass.side_effect = custom_config

    with pytest.raises(exception.ConfigException):
        MazeGenerator("dummy_path")


@patch.object(mg_module, 'Mlx')
@patch('src.mazegen.config.Config', side_effect=MockConfig)
def test_generate_maze_out_of_bounds(MockConfigClass: Any,
                                     MockMlx: Any) -> None:
    """Verifies that generation fails if entry or exit are out of bounds."""

    mock_instance = MockMlx.return_value
    mock_instance.mlx_init.return_value = MagicMock()

    def custom_config(path: str = ""):
        c = MockConfig()
        c.ENTRY = [51 + 5, 1]  # Out of bounds
        return c
    MockConfigClass.side_effect = custom_config

    with pytest.raises(exception.ConfigException):
        MazeGenerator("dummy_path")


if __name__ == "__main__":
    sys.exit(pytest.main(["-v", __file__]))
