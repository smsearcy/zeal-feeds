# SPDX-FileCopyrightText: 2023-present Scott Searcy <smsearcy14@outlook.com>
#
# SPDX-License-Identifier: MIT
"""Entrypoint for `python -m zeal_feeds`."""
import sys

from zeal_feeds import main

if __name__ == "__main__":
    sys.exit(main.main())
