PYTHON			= python3
MAIN			= main.py
MYPY_FLAGS		= --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
DEPENDENCIES	= src/mazegen/lib/mlx-2.2-py3-ubuntu-any.whl

build:
	bash -c "\
	$(RM) -rf venv						&& \
	$(PYTHON) -m venv venv				&& \
	source ./venv/bin/activate			&& \
	$(PYTHON) -m pip install build		&& \
	$(PYTHON) -m build					&& \
	deactivate							&& \
	$(RM) -rf venv"
	cp ./dist/mazegen-*.whl .

install:
	pip install $(DEPENDENCIES)
	#$(CP) lib/mlx_CLXV/libmlx.so ~/.local/lib/python3.10/site-packages/mlx/
	pip install 

run:
	$(PYTHON) $(MAIN)

debug:
	$(PYTHON) -m pdb $(MAIN)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .mypy_cache .pytest_cache

lint:
	flake8 .
	mypy . $(MYPY_FLAGS)

lint-strict:
	flake8 .
	mypy . --strict

.PHONY: install run debug clean lint lint-strict