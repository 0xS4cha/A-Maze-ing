PYTHON			= python3
VENV			= venv
VENV_BIN		= $(VENV)/bin
V_PYTHON		= $(VENV_BIN)/python
V_PIP			= $(VENV_BIN)/python -m pip
MAIN			= a_maze_ing.py

MYPY_FLAGS = --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
DEPENDENCIES	= pytest flake8 mypy lib/mlx-2.2-py3-none-any.whl
FLAKE			= $(VENV_BIN)/flake8
MYPY			= $(VENV_BIN)/mypy
EXCLUDE			= $(VENV)
OUTPUT_FILE		= mazegen-1.0.0-py3-none-any.whl
SRCS			=	./src/mazegen/utils/buttons.py \
					./src/mazegen/utils/maze_utils.py \
					./src/mazegen/utils/mlx_utils.py \
					./src/mazegen/utils/generate_utils.py \
					./src/mazegen/algorithms/stacking.py \
					./src/mazegen/algorithms/prim.py \
					./src/mazegen/__init__.py \
					./src/mazegen/MazeGenerator.py \
					./src/mazegen/config.py \
					./src/mazegen/exception.py \
					./src/mazegen/parser.py \
					./src/mazegen/resolve.py

build: $(OUTPUT_FILE)

$(OUTPUT_FILE): $(SRCS)
	bash -c "\
	$(RM) -rf build_venv						&& \
	$(PYTHON) -m venv build_venv					&& \
	source ./build_venv/bin/activate				&& \
	$(PYTHON) -m pip install build				&& \
	$(PYTHON) -m build					&& \
	deactivate						&& \
	$(RM) -rf build_venv"
	cp ./dist/$(OUTPUT_FILE) .

$(VENV):
	$(PYTHON) -m venv $(VENV)
	$(V_PIP) install --upgrade pip

install: build $(VENV)
	$(V_PIP) install $(DEPENDENCIES)
	$(V_PIP) install $(OUTPUT_FILE) --force-reinstall

run: install
	$(V_PYTHON) a_maze_ing.py config.txt

debug: install
	$(V_PYTHON) -m pdb $(MAIN)

clean:
	rm -rf $(VENV) build_venv
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	rm -rf .mypy_cache .pytest_cache
	rm -rf $(OUTPUT_FILE) dist/

lint: install
	$(FLAKE) . --exclude '$(VENV)'
	$(MYPY) $(MYPY_FLAGS) src

lint-strict: install
	$(FLAKE) . --exclude '$(VENV)'
	$(MYPY) $(MYPY_FLAGS) --strict src

.PHONY: install run debug clean lint lint-strict