PYTHON			= python3
MAIN			= main.py
MYPY_FLAGS		= --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
DEPENDENCIES	=	src/mazegen/lib/mlx-2.2-py3-ubuntu-any.whl\
					pytest
FLAKE			= ~/.local/bin/flake8
OUTPUT_FILE		= mazegen-1.0.0-py3-none-any.whl
SRCS			=	./a_maze_ing.py \
					./src/mazegen/utils/buttons.py \
					./src/mazegen/utils/maze_utils.py \
					./src/mazegen/utils/mlx_utils.py \
					./src/mazegen/algorithms/backtracking.py \
					./src/mazegen/algorithms/eller.py \
					./src/mazegen/lib/mlx_CLXV/python/src/mlx/__init__.py \
					./src/mazegen/lib/mlx_CLXV/python/src/mlx/mlx.py \
					./src/mazegen/lib/mlx_CLXV/python/src/mlx/test/mlxtest.py \
					./src/mazegen/__init__.py \
					./src/mazegen/MazeGenerator.py \
					./src/mazegen/config.py \
					./src/mazegen/exception.py \
					./src/mazegen/parser.py \
					./src/mazegen/resolve.py

build: $(OUTPUT_FILE)

$(OUTPUT_FILE): $(SRCS)
	bash -c "\
	$(RM) -rf venv						&& \
	$(PYTHON) -m venv venv					&& \
	source ./venv/bin/activate				&& \
	$(PYTHON) -m pip install build				&& \
	$(PYTHON) -m build					&& \
	deactivate						&& \
	$(RM) -rf venv"
	cp ./dist/mazegen-*.whl .

install:
	$(PYTHON) -m pip install $(DEPENDENCIES)
	$(PYTHON) -m pip install mazegen-*.whl

run:
	$(PYTHON) a_maze_ing.py default_config.txt

debug:
	$(PYTHON) -m pdb $(MAIN)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .mypy_cache .pytest_cache

lint:
	flake8 . --exclude './src/mazegen/lib'
	mypy . $(MYPY_FLAGS)

lint-strict:
	flake8 . --exclude './src/mazegen/lib'
	mypy . --strict

.PHONY: install run debug clean lint lint-strict