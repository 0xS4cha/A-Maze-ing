import sys
import os
from typing import Any
import pytest
from unittest.mock import MagicMock, patch

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.mazegen.utils import maze_utils  # noqa: E402
from src.mazegen import exception  # noqa: E402


class MockConfig:
    """Mock configuration to isolate tests."""
    def __init__(self) -> None:
        self.WIDTH = 51
        self.HEIGHT = 51
        self.PERFECT = False
        self.ENTRY = (1, 1)
        self.EXIT = (49, 49)
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


@patch('src.mazegen.utils.maze_utils.resolve')
@patch('src.mazegen.utils.maze_utils.prim')
def test_generate_maze_prim_success(mock_prim: Any,
                                    mock_resolve: Any) -> None:
    """Tests the full maze generation flow with Prim algorithm (mocked)."""
    config = MockConfig()
    xvar = MockXVar()

    mock_prim.generate.return_value = [[1 for _ in range(config.WIDTH)]
                                       for _ in range(config.HEIGHT)]

    mock_resolve.return_value = [(1, 1), (2, 2)]

    result = maze_utils.generate_maze(config, xvar)

    assert result is not None
    assert len(result) == config.HEIGHT
    assert len(result[0]) == config.WIDTH

    mock_prim.generate.assert_called_once()


@patch('src.mazegen.utils.maze_utils.resolve')
@patch('src.mazegen.utils.maze_utils.stacking')
def test_generate_maze_stacking_success(mock_stacking: Any,
                                        mock_resolve: Any) -> None:
    """Tests the full maze generation flow
    with stacking algorithm (mocked)."""
    config = MockConfig()
    config.PERFECT = True
    xvar = MockXVar()

    mock_stacking.generate.return_value = [[1 for _ in range(config.WIDTH)]
                                           for _ in range(config.HEIGHT)]

    mock_resolve.return_value = [(1, 1), (2, 2)]

    result = maze_utils.generate_maze(config, xvar)

    assert result is not None
    assert len(result) == config.HEIGHT
    assert len(result[0]) == config.WIDTH

    mock_stacking.generate.assert_called_once()


@patch('src.mazegen.utils.maze_utils.prim')
def test_generate_maze_invalid_entry_exit(mock_prim: Any) -> None:
    """Verifies that generate_maze raises an
    exception if entry/exit are invalid."""
    config = MockConfig()
    xvar = MockXVar()

    config.ENTRY = (10, 10)
    config.EXIT = (10, 10)

    mock_prim.generate.return_value = [[1 for _ in range(config.WIDTH)]
                                       for _ in range(config.HEIGHT)]

    with pytest.raises(exception.ConfigException):
        maze_utils.generate_maze(config, xvar)


@patch('src.mazegen.utils.maze_utils.prim')
def test_generate_maze_out_of_bounds(mock_prim: Any) -> None:
    """Verifies that generation fails if entry or exit are out of bounds."""
    config = MockConfig()
    xvar = MockXVar()

    config.ENTRY = (config.WIDTH + 5, 1)

    mock_prim.generate.return_value = [[1 for _ in range(config.WIDTH)]
                                       for _ in range(config.HEIGHT)]

    with pytest.raises((exception.ConfigException, IndexError)):
        maze_utils.generate_maze(config, xvar)


if __name__ == "__main__":
    sys.exit(pytest.main(["-v", __file__]))
