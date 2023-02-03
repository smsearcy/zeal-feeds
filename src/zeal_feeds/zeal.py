# SPDX-FileCopyrightText: 2023-present Scott Searcy <smsearcy14@outlook.com>
#
# SPDX-License-Identifier: MIT
"""Functionality related to Zeal application."""

from __future__ import annotations

import functools
import json
import re
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


@attrs.define
class MetaData:
    """Model metadata to save with DocSet for Zeal."""

    name: str
    title: str
    version: str
    feed_url: str
    urls: list[str]


FEED_URL = "https://zealusercontributions.vercel.app/api/docsets/{name}.xml"


@functools.cache
def docset_install_path() -> Path:
    """Get the path where Docsets are installed to."""
    if sys.platform == "win32":
        install_path = _windows_docset_install_path()
    else:
        install_path = _linux_docset_install_path()
    if not install_path.exists():
        install_path.mkdir(parents=True)
    return install_path


def installed_docsets() -> Iterator[str]:
    """List of locally installed DocSets."""
    docset_path = docset_install_path()

    for meta_json in docset_path.glob("*/meta.json"):
        metadata = json.load(meta_json.open("r"))
        yield metadata["name"]


def install(docset: DocSet, tarball: Path):
    """Install a docset into the Zeal data directory."""
    # TODO: don't install if docset already installed
    docset_path = docset_install_path()

    with tarfile.open(tarball) as docset_archive:
        docset_folder = docset_archive.next()
        if not (docset_folder and re.match(r"\w+\.docset", docset_folder.name)):
            raise ApplicationError(f"Unexpected contents for {docset.name} archive")
        docset_archive.extractall(docset_path)

    converter = Converter()
    meta_json = docset_path / docset_folder.name / "meta.json"
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
