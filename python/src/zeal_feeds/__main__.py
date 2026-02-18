"""Entrypoint for `python -m zeal_feeds`."""

from __future__ import annotations

import sys

from zeal_feeds import main

if __name__ == "__main__":
    sys.exit(main.main())
