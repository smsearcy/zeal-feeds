default: pre-commit fmt fix mypy build tests

pre-commit:
  uvx pre-commit run --all-files

fmt:
  uv run ruff format .

check:
  uv run ruff check .

fix: fmt
  uv run ruff check . --fix

mypy:
  uv run mypy src --pretty

build:
  uv build

tests:
  uv run pytest --cov=src --cov-report html --cov-report term
