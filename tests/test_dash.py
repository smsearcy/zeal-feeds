# SPDX-FileCopyrightText: 2023-present Scott Searcy <smsearcy14@outlook.com>
#
# SPDX-License-Identifier: MIT
"""Test functionality in the `dash` module."""
import json

from yarl import URL
from zeal_feeds import dash


def test_mirrors():
    """Verify that mirrors are expanded correctly."""
    mirrors = [str(url) for url in dash.all_mirrors(URL("https://kapeli.com/foo"))]

    # TODO: is this too tightly coupled? (make the domain/mirrors parameters?)
    expected = [
        "https://kapeli.com/foo",
        "https://sanfrancisco.kapeli.com/foo",
        "https://newyork.kapeli.com/foo",
        "https://london.kapeli.com/foo",
        "https://frankfurt.kapeli.com/foo",
    ]

    assert mirrors == expected


def test_parse_user_contrib_index(data_folder):
    """Verify parsing of Dash user contributed index.json."""
    index_file = data_folder / "dash-user-contrib-index.json"
    index_json = json.loads(index_file.read_text())

    docsets = {
        docset.id: docset for docset in dash._parse_user_contrib_index(index_json)
    }
    print(docsets["structlog"])

    expected_structlog = dash.DocSet(
        id="structlog",
        name="structlog",
        author=dash.DocSetAuthor(
            name="Hynek Schlawack", link="https://github.com/hynek"
        ),
        archive="structlog.tgz",
        version="22.3.0",
    )
    assert docsets["structlog"] == expected_structlog
    assert len(docsets) == 547
