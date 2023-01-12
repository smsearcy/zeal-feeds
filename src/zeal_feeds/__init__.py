# SPDX-FileCopyrightText: 2023-present Scott Searcy <smsearcy14@outlook.com>
#
# SPDX-License-Identifier: MIT
"""Manage feeds for user contributed docsets in Zeal."""


# should this be loaded from project metadata?
APP_NAME = "zeal-feeds"
"""Application name, used for configuration folders."""


class ApplicationError(Exception):
    """Custom exception class for errors raised by the application."""

    pass
