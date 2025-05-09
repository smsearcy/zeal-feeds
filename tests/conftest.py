"""pytest configuration."""

from __future__ import annotations

from pathlib import Path

import pytest


@pytest.fixture(scope="module")
def data_folder() -> Path:
    """Fixture to simplify accessing test data files."""
    return Path(__file__).parent / "data"
