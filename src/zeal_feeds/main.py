# SPDX-FileCopyrightText: 2023-present Scott Searcy <smsearcy14@outlook.com>
#
# SPDX-License-Identifier: MIT
"""Main command line entry point for `zeal-feeds`.

This module handles modules parsing and end-user interaction.

"""
import argparse
import random
from pathlib import Path

import requests
from platformdirs import user_runtime_path
from rich.live import Live
from rich.progress import Progress
from rich.spinner import Spinner

from zeal_feeds import ApplicationError, dash, zeal


def main():
    """Main command line entry point.

    Parse arguments and execute sub-commands.

    """
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    install_parser = subparsers.add_parser("install", help="Install docset")
    install_parser.add_argument("docset", metavar="DOCSET", nargs="+")
    install_parser.set_defaults(func=install)

    args = parser.parse_args()
    try:
        return args.func(args)
    except ApplicationError as exc:
        return str(exc)


def install(args):
    """Install the specified DocSets."""
    docset_data = _load_docset_index()

    docset_names = args.docset
    found_docsets = {name: docset_data.find(name) for name in docset_names}
    missing_docsets = [name for name, docset in found_docsets.items() if docset is None]
    if missing_docsets:
        return f"Failed to find the following docsets: {', '.join(missing_docsets)}"

    installed_docsets = zeal.installed_docsets()

    for docset in found_docsets.values():
        if docset.id in installed_docsets:
            print(f"Skipping {docset.id}, already installed")
            continue
        archive = _download_archive(docset)
        spinner = Spinner("simpleDots", f"Installing {docset.id}")
        with Live(spinner):
            zeal.install(docset, archive)
        archive.unlink()
        return None


def _load_docset_index() -> dash.DocSetCollection:
    """Load the docset index, with a spinner."""
    if docsets := dash.load_cached_index():
        # should I use Rich for "normal" output?
        print("Using cached index of user contributed docsets")
        return docsets
    spinner = Spinner("dots", "Loading index of user contributed docsets")
    with Live(spinner):
        return dash.user_contrib_index()


def _download_archive(docset: dash.DocSet) -> Path:
    """Download the docset archive, from a random mirror, with progress bar.

    According to *zeal-user-contrib*, the random URL is what *Zeal* does.

    """
    archive_url = random.choice(docset.archive_urls)
    archive_destination = user_runtime_path("zeal-feeds") / docset.archive
    archive_destination.parent.mkdir(exist_ok=True)

    with (
        requests.get(archive_url, stream=True) as r,
        Progress() as progress,
        archive_destination.open("wb") as archive,
    ):
        file_size = int(r.headers["content-length"])
        download_task = progress.add_task(f"Downloading {docset.id}", total=file_size)

        for content in r.iter_content(chunk_size=512):
            archive.write(content)
            progress.update(download_task, advance=len(content))

    return archive_destination
