# SPDX-FileCopyrightText: 2023-present Scott Searcy <smsearcy14@outlook.com>
#
# SPDX-License-Identifier: MIT
"""Functionality related to Dash and the user contributed feeds it provides."""
from __future__ import annotations

import json
import time
from collections.abc import Iterable, Iterator, Mapping
from functools import cached_property
from typing import Optional, Union

import attrs
import requests
from cattrs import Converter
from cattrs.gen import make_dict_structure_fn, override
from platformdirs import user_data_path
from yarl import URL

from . import APP_NAME, ApplicationError

# TODO: ability to load from configuration file?
DASH_DOMAIN = "kapeli.com"
DASH_MIRRORS = ("sanfrancisco", "newyork", "london", "frankfurt")
ARCHIVE_URL = "https://kapeli.com/feeds/zzz/user_contributed/build/{id}/{archive}"

KAPELI_URL = URL(f"https://{DASH_DOMAIN}/feeds/zzz/user_contributed/build/")

_CACHED_INDEX_FILENAME = "index.json"


@attrs.define
class DocSet:
    """Model the user contributed docset data."""

    # Kapeli's index has separate `name` & `id` (e.g. "Perl6" and "Perl 6").
    # But Zeal docset.json has only `name` and it matches Kapeli's `id`
    # (underscores instead of spaces).
    id: str
    name: str
    author: DocSetAuthor
    archive: str
    version: str
    aliases: list[str] = attrs.field(factory=list)
    # *cattrs* evaluations this type hint, so we cannot use | when <= py3.10
    specific_versions: list[Union[DocSetVersion, DocSetComment]] = attrs.field(
        factory=list
    )
    icon: str = attrs.field(default=None, eq=False, repr=False)
    icon_2x: str = attrs.field(default=None, eq=False, repr=False)

    @property
    def archive_urls(self) -> list[str]:
        """URLs to download the archive from each mirror."""
        archive_url = URL(ARCHIVE_URL.format(id=self.id, archive=self.archive))
        return [str(url) for url in all_mirrors(archive_url)]

    def __str__(self):
        return f"{self.name} (id={self.id}) by {self.author} version={self.version}"


class DocSetCollection(Mapping[str, DocSet]):
    """Collection of DocSet information.

    This mapping is keyed by the DocSet ID,
    and provides other methods for searching the collection.

    """

    def __init__(self, docsets: Iterable[DocSet]):
        self._docsets = {self._normalize(docset.id): docset for docset in docsets}

    def __getitem__(self, item: str) -> DocSet:
        return self._docsets[self._normalize(item)]

    def __len__(self) -> int:
        return len(self._docsets)

    def __iter__(self):
        return iter(self._docsets)

    def find(self, value: str) -> DocSet | None:
        """Find matching package based on package ID or Name."""
        return self._packages_by_name_or_id.get(self._normalize(value))

    def search(self, value: str) -> list[DocSet]:
        """Search for packages that match the provided name."""
        raise NotImplementedError()

    @staticmethod
    def _normalize(value: str) -> str:
        return value.lower()

    @cached_property
    def _packages_by_name_or_id(self) -> dict[str, DocSet]:
        docset_index = self._docsets.copy()
        docset_index.update(
            {self._normalize(docset.name): docset for docset in self._docsets.values()}
        )
        return docset_index


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


def all_mirrors(url: URL) -> Iterator[URL]:
    """Yields URLs for all Dash mirrors."""
    url = url.with_host(DASH_DOMAIN)
    yield url
    for mirror in DASH_MIRRORS:
        host = f"{mirror}.{DASH_DOMAIN}"
        yield url.with_host(host)


def user_contrib_index() -> DocSetCollection:
    """Get the user contributed docset index information."""
    index_json_url = KAPELI_URL / "index.json"
    r = requests.get(str(index_json_url))
    if not r.ok:
        raise ApplicationError(
            "Failed to load information about user contributed docsets"
        )

    index_json = r.json()
    cached_index = user_data_path(APP_NAME) / _CACHED_INDEX_FILENAME
    cached_index.parent.mkdir(exist_ok=True)
    json.dump(index_json, cached_index.open("w"))

    return DocSetCollection(_parse_user_contrib_index(index_json))


def load_cached_index() -> DocSetCollection | None:
    """Try to load cached Docset index.json.

    Checks for existence of cached file and that it is less than 12 hours old.

    """
    cached_index = user_data_path(APP_NAME) / _CACHED_INDEX_FILENAME
    if not cached_index.exists():
        return None
    cache_updated = cached_index.stat().st_mtime
    if time.time() - cache_updated > 43_200:  # 12 hours in seconds
        return None

    cached_json = json.load(cached_index.open("r"))
    return DocSetCollection(_parse_user_contrib_index(cached_json))


def _parse_user_contrib_index(index_json: dict) -> Iterator[DocSet]:
    """Read docset data from the index.json file."""
    converter = Converter()
    # map "icon@2x" in JSON to "icon_2x" in dataclass
    converter.register_structure_hook(
        DocSet,
        make_dict_structure_fn(DocSet, converter, icon_2x=override(rename="icon@2x")),
    )

    for id_, docset in index_json["docsets"].items():
        docset["id"] = id_
        result = converter.structure(docset, DocSet)
        yield result
