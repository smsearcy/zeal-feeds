"""Manage feeds for user contributed docsets in Zeal."""

from __future__ import annotations

# should this be loaded from project metadata?
APP_NAME = "zeal-feeds"
"""Application name, used for configuration folders."""


class ApplicationError(Exception):
    """Custom exception class for errors raised by the application."""

    pass
