default: pre-commit fix mypy build tests

# Run pre-commit
pre-commit:
  uvx pre-commit run --all-files

# Format with Ruff
fmt:
  uv run ruff format .

# Lint with Ruff (no fixes)
check:
  uv run ruff check .

# Ruff: format and lint (with fixes)
fix: fmt
  uv run ruff check . --fix

# Check types with mypy
mypy:
  uv run mypy src --pretty

# Build package
build:
  uv build

# Run pytest with in current environment
tests:
  uv run pytest --cov=src --cov-report html --cov-report term

# Run pytest across multiple environments with tox
tox:
  uvx --with tox-uv tox
