# SPDX-FileCopyrightText: 2023-present Scott Searcy <smsearcy14@outlook.com>
#
# SPDX-License-Identifier: MIT
"""Functionality related to Zeal application."""

from __future__ import annotations

import json
import sys
import tarfile
from collections.abc import Iterator
from configparser import ConfigParser
from pathlib import Path

import attrs
from cattrs import Converter
from platformdirs import user_config_path

from . import ApplicationError
from .user_contrib import DocSet

FEED_URL = "https://zealusercontributions.vercel.app/api/docsets/{name}.xml"


@attrs.define
class MetaData:
    """Model metadata to save with DocSet for Zeal."""

    name: str
    title: str
    version: str
    feed_url: str
    urls: list[str]


@attrs.define
class Zeal:
    """Class for interacting with the installed Zeal application."""

    docset_path: Path

    @classmethod
    def from_config(cls):
        """Get the path where Docsets are installed to."""
        if sys.platform == "win32":
            docset_path = _windows_docset_install_path()
        else:
            docset_path = _linux_docset_install_path()
        if not docset_path.exists():
            docset_path.mkdir(parents=True)
        return cls(docset_path)

    def installed_docsets(self) -> Iterator[str]:
        """List of locally installed DocSets."""
        for meta_json in self.docset_path.glob("*/meta.json"):
            metadata = json.load(meta_json.open("r"))
            yield metadata["name"]

    def install_docset(self, docset: DocSet, tarball: Path) -> None:
        """Install a docset into the Zeal data directory."""
        # TODO: don't install if docset already installed
        with tarfile.open(tarball) as docset_archive:
            docset_folder = docset_archive.next()
            if not (docset_folder and docset_folder.name.endswith(".docset")):
                raise ApplicationError(f"Unexpected contents for {docset.name} archive")
            docset_archive.extractall(self.docset_path)

        # ensure docset folder given the correct name
        expected_folder_name = f"{docset.name}.docset"
        if docset_folder.name != expected_folder_name:
            destination = self.docset_path / expected_folder_name
            if destination.exists():
                raise ApplicationError(
                    f"Destination folder already exists: {destination}"
                )
            source = self.docset_path / docset_folder.name
            source.rename(destination)

        converter = Converter()
        meta_json = self.docset_path / expected_folder_name / "meta.json"
        metadata = MetaData(
            name=docset.name,
            title=docset.title,
            version=docset.version,
            urls=docset.urls,
            feed_url=FEED_URL.format(name=docset.name),
        )
        json.dump(converter.unstructure(metadata), meta_json.open("w"), indent=2)


def _linux_docset_install_path() -> Path:
    """Get the docset path from the Zeal configuration file."""
    config_file = user_config_path("Zeal") / "Zeal.conf"
    if not config_file.exists():
        raise ApplicationError("Zeal configuration not found.")
    zeal_config = ConfigParser()
    zeal_config.read_file(config_file.open())

    docset_path = zeal_config.get("docsets", "path")
    return Path(docset_path)


def _windows_docset_install_path() -> Path:
    """Get the docset path from the Zeal registry entries."""
    # gatekeeper so that mypy doesn't choke on `winreg` in Linux
    if sys.platform != "win32":
        raise RuntimeError("Incorrect platform for Windows registry")

    import winreg

    try:
        with winreg.OpenKey(
            winreg.HKEY_CURRENT_USER, r"SOFTWARE\Zeal\Zeal\docsets"
        ) as key:
            docset_path = winreg.QueryValueEx(key, "path")[0]
    except OSError as exc:
        raise ApplicationError(
            f"Failed to read docset path from registry: {exc}"
        ) from None

    return Path(docset_path)
