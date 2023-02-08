# SPDX-FileCopyrightText: 2023-present Scott Searcy <smsearcy14@outlook.com>
#
# SPDX-License-Identifier: MIT
"""Test functionality in the `user_contrib` module."""
import json

import pytest
from zeal_feeds import user_contrib


def test_parse_docset_index(data_folder):
    """Verify parsing of docset JSON."""
    index_file = data_folder / "docsets.json"
    index_json = json.loads(index_file.read_text())

    docsets = list(user_contrib._parse_docset_index(index_json))

    expected_docset = user_contrib.DocSet(
        name="pika",
        author=user_contrib.DocSetAuthor(
            name="Dan Girellini", link="https://github.com/dangitall"
        ),
        archive="pika.tgz",
        version="1.0.0b1",
        urls=[
            "https://kapeli.com/feeds/zzz/user_contributed/build/pika/pika.tgz",
            "https://sanfrancisco.kapeli.com/feeds/zzz/user_contributed/build/pika/pika.tgz",
            "https://newyork.kapeli.com/feeds/zzz/user_contributed/build/pika/pika.tgz",
            "https://london.kapeli.com/feeds/zzz/user_contributed/build/pika/pika.tgz",
            "https://frankfurt.kapeli.com/feeds/zzz/user_contributed/build/pika/pika.tgz",
        ],
    )
    assert docsets[0] == expected_docset
    assert len(docsets) == 540


DOCSETS = {
    "foobar": user_contrib.DocSet(
        name="FooBar",
        aliases=["Foo Bar", "foo-bar"],
        author=user_contrib.DocSetAuthor(
            name="Arthur Dent",
            link="https://hhgttg.net/adent",
        ),
        archive="FooBar.tgz",
        version="1.0",
        urls=[],
    ),
    "foo": user_contrib.DocSet(
        name="Foo",
        author=user_contrib.DocSetAuthor(
            name="Ford Prefect",
            link="https://hhgttg.net/ford",
        ),
        archive="Foo.tgz",
        version="2.0",
        urls=[],
    ),
    "acme": user_contrib.DocSet(
        name="ACME",
        author=user_contrib.DocSetAuthor(
            name="Wile E. Coyote",
            link="https://acme.com/coyote",
        ),
        archive="ACME.tgz",
        version="0.5.6",
        urls=[],
    ),
    "beep_beep": user_contrib.DocSet(
        name="Beep_Beep",
        author=user_contrib.DocSetAuthor(
            name="Roadrunner",
            link="https://fast.com/rr",
        ),
        archive="Beep_Beep.tgz",
        version="15.6",
        urls=[],
    ),
}
COLLECTION = user_contrib.DocSetCollection(DOCSETS.values())


@pytest.mark.parametrize(
    ("item", "expected"),
    [
        ("ACME", DOCSETS["acme"]),
        ("foobar", DOCSETS["foobar"]),
        ("nada", None),
    ],
)
def test_docset_collection_get(item, expected):
    """Verify Docsets can be accessed by name."""
    assert COLLECTION.get(item) == expected


@pytest.mark.parametrize(
    ("search", "expected"),
    [
        ("foo bar", [DOCSETS["foobar"]]),
        ("foo", [DOCSETS["foo"], DOCSETS["foobar"]]),
    ],
)
def test_docset_collection_search(search, expected):
    """Verify docset search functionality."""
    assert sorted(COLLECTION.search(search)) == sorted(expected)


@pytest.mark.parametrize(
    ("search", "expected"),
    [
        ("food", [DOCSETS["foo"]]),
        ("foobra", [DOCSETS["foobar"]]),
        ("acec", [DOCSETS["acme"]]),
        ("amecs", []),
    ],
)
def test_docset_collection_fuzzy_search(search, expected):
    """Verify docset search functionality."""
    assert sorted(COLLECTION.fallback_search(search)) == sorted(expected)
