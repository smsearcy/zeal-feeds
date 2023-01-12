# SPDX-FileCopyrightText: 2023-present Scott Searcy <smsearcy14@outlook.com>
#
# SPDX-License-Identifier: MIT
"""pytest configuration."""
from pathlib import Path

import pytest


@pytest.fixture(scope="module")
def data_folder() -> Path:
    """Fixture to simplify accessing test data files."""
    return Path(__file__).parent / "data"
