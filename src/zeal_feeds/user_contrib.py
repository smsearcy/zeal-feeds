# SPDX-FileCopyrightText: 2023-present Scott Searcy <smsearcy14@outlook.com>
#
# SPDX-License-Identifier: MIT
"""Functionality related to fetching the user contributed docsets."""
from __future__ import annotations

import json
import time
from collections.abc import Iterable, Iterator, Mapping
from typing import Optional

import attrs
import requests
from cattrs import Converter
from cattrs.gen import make_dict_structure_fn, override
from platformdirs import user_data_path

from . import APP_NAME, ApplicationError

USER_DOCSET_API = "https://zealusercontributions.vercel.app/api/docsets"
_CACHE_FILENAME = "docsets.json"


@attrs.define
class DocSet:
    """Model the user contributed docset data."""

    name: str
    author: DocSetAuthor
    archive: str
    version: str
    aliases: list[str] = attrs.field(factory=list)
    urls: list[str] = attrs.field(factory=list)
    icon: str = attrs.field(default=None, eq=False, repr=False)
    icon_2x: str = attrs.field(default=None, eq=False, repr=False)

    @property
    def title(self) -> str:
        """Pretty name of Docset."""
        return self.name.replace("_", " ")

    def __str__(self):
        return f"{self.name} ({self.version})"

    def __lt__(self, other: DocSet):
        return self.name < other.name


class DocSetCollection(Mapping[str, DocSet]):
    """Collection of DocSet information.

    This mapping is keyed by the DocSet ID,
    and provides other methods for searching the collection.

    """

    def __init__(self, docsets: Iterable[DocSet]):
        self._docsets = {self._normalize(docset.name): docset for docset in docsets}

    def __getitem__(self, item: str) -> DocSet:
        return self._docsets[self._normalize(item)]

    def __len__(self) -> int:
        return len(self._docsets)

    def __iter__(self):
        return iter(self._docsets)

    def search(self, text: str) -> Iterator[DocSet]:
        """Yield packages that match the provided name."""
        text = self._normalize(text)
        for id_, docset in self._docsets.items():
            if text in id_:
                yield docset
                continue
            if text in self._normalize(docset.title):
                yield docset
                continue
            if self._search_aliases(text, docset.aliases):
                yield docset
                continue

    def fallback_search(self, text: str) -> Iterator[DocSet]:
        """Yield packages that approximately match the provided name."""
        text = self._normalize(text)
        for id_, docset in self._docsets.items():
            if _edit_distance(text, id_) <= 2:
                yield docset

    @staticmethod
    def _normalize(value: str) -> str:
        return value.lower()

    def _search_aliases(self, text: str, aliases: list[str]) -> bool:
        return any(text in self._normalize(alias) for alias in aliases)


@attrs.define
class DocSetAuthor:
    """Model author for user contributed docset."""

    name: str
    link: str

    def __str__(self):
        return f"{self.name} ({self.link})"


@attrs.define
class DocSetVersion:
    """Model version for user contributed docset."""

    version: str
    archive: str
    # *cattrs* evaluations this type hint, so we cannot use | when <= py3.10
    author: Optional[DocSetAuthor] = None


@attrs.define
class DocSetComment:
    """Model comment for user contributed docset."""

    _comment: str


def user_contrib_index(docset_index: str) -> DocSetCollection:
    """Get the user contributed docset index information."""
    r = requests.get(docset_index)
    if not r.ok:
        raise ApplicationError(
            "Failed to load information about user contributed docsets"
        )

    index_json = r.json()
    cached_index = user_data_path(APP_NAME) / _CACHE_FILENAME
    cached_index.parent.mkdir(exist_ok=True, parents=True)
    json.dump(index_json, cached_index.open("w"))

    return DocSetCollection(_parse_docset_index(index_json))


def load_cached_index() -> DocSetCollection | None:
    """Try to load cached Docset index.json.

    Checks for existence of cached file and that it is less than 12 hours old.

    """
    cached_index = user_data_path(APP_NAME) / _CACHE_FILENAME
    if not cached_index.exists():
        return None
    cache_updated = cached_index.stat().st_mtime
    if time.time() - cache_updated > 43_200:  # 12 hours in seconds
        return None

    cached_json = json.load(cached_index.open("r"))
    return DocSetCollection(_parse_docset_index(cached_json))


def _parse_docset_index(index_json: dict) -> Iterator[DocSet]:
    """Yield docset data models from the `/api/docsets` data."""
    converter = Converter()
    # map "icon@2x" in JSON to "icon_2x" in dataclass
    converter.register_structure_hook(
        DocSet,
        make_dict_structure_fn(DocSet, converter, icon_2x=override(rename="icon@2x")),
    )

    for docset in index_json:
        yield converter.structure(docset, DocSet)


def _edit_distance(pattern: str, target: str) -> int:
    len_a, len_b = len(pattern), len(target)
    d = _edit_distance_matrix(len_a, len_b)
    for i, pattern_char in enumerate(pattern, start=1):
        for j, target_char in enumerate(target, start=1):
            cost = int(pattern_char != target_char)
            d[i][j] = min(
                d[i - 1][j] + 1,  # deletion
                d[i][j - 1] + 1,  # insertion
                d[i - 1][j - 1] + cost,  # substitution
            )
    return d[len_a][len_b]


def _edit_distance_matrix(pattern_length: int, target_length: int) -> list[list[int]]:
    rows, cols = pattern_length + 1, target_length + 1
    d = []
    for _ in range(rows):
        d.append([0] * cols)
    for i in range(rows):
        d[i][0] = i
    for j in range(cols):
        d[0][j] = j
    return d
