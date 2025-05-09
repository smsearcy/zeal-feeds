"""Command line entry point for `zeal-feeds`.

This module handles modules parsing and end-user interaction.

"""

from __future__ import annotations

import argparse
import random
from pathlib import Path

import requests
from platformdirs import user_runtime_path
from rich.progress import Progress

from zeal_feeds import ApplicationError, user_contrib
from zeal_feeds.console import console
from zeal_feeds.zeal import Zeal


def main():
    """Parse command line arguments and run sub-command."""
    parser = argparse.ArgumentParser(
        prog="zeal-feeds", description="Install user contributed Docsets into Zeal"
    )
    subparsers = parser.add_subparsers()

    install_parser = subparsers.add_parser("install", help="install docsets")
    install_parser.add_argument("docset", metavar="DOCSET", nargs="+")
    install_parser.add_argument("--url", default=user_contrib.USER_DOCSET_API)
    install_parser.add_argument("--config", help="Specify path to Zeal.conf file")
    install_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Downloads the docsets but does not install",
    )
    install_parser.set_defaults(func=install)

    search_parser = subparsers.add_parser("search", help="search available docsets")
    search_parser.add_argument("text", metavar="TEXT")
    search_parser.add_argument("--url", default=user_contrib.USER_DOCSET_API)
    search_parser.set_defaults(func=search)

    args = parser.parse_args()
    if not hasattr(args, "func"):
        parser.print_help()
        return 1

    try:
        return args.func(args)
    except ApplicationError as exc:
        return str(exc)


def search(args) -> str | None:
    """Search for matching docsets."""
    docset_data = _load_docset_index(args.url)
    fallback = False

    search_text = args.text

    matches = sorted(docset_data.search(search_text))
    if not matches:
        matches = sorted(docset_data.fallback_search(search_text))
        fallback = True
    if not matches:
        return "No matching docsets found"

    if fallback:
        console.print("No exact matches, did you mean:")
    else:
        console.print("Matching docsets:")
    for docset in matches:
        console.print(docset.name)
    return None


def install(args) -> str | None:
    """Install the specified DocSets."""
    zeal = Zeal.load_config(args.config) if args.config else Zeal.find_config()

    docset_data = _load_docset_index(args.url)

    docset_names = args.docset
    found_docsets = {name: docset_data.get(name) for name in docset_names}
    missing_docsets = [name for name, docset in found_docsets.items() if docset is None]
    if missing_docsets:
        return f"Failed to find the following docsets: {', '.join(missing_docsets)}"

    installed_docsets = set(zeal.installed_docsets())
    for docset in found_docsets.values():
        if docset is None:
            continue
        if docset.name in installed_docsets:
            console.print(f"Skipping {docset.name!r}, already installed")
            continue
        archive = _download_archive(docset)
        if args.dry_run:
            console.print(f"Skipping {docset.name!r} due to --dry-run")
        else:
            with console.status(f"Installing {docset.name}"):
                zeal.install_docset(docset, archive)

        archive.unlink()

    return None


def _load_docset_index(url: str) -> user_contrib.DocSetCollection:
    """Load the docset index, with a spinner."""
    if docsets := user_contrib.load_cached_index():
        # should I use Rich for "normal" output?
        console.print("Using cached index of user contributed docsets")
        return docsets
    with console.status("Loading index of user contributed docsets"):
        return user_contrib.user_contrib_index(url)


def _download_archive(docset: user_contrib.DocSet) -> Path:
    """Download the docset archive, from a random mirror, with progress bar.

    According to *zeal-user-contrib*, the random URL is what *Zeal* does.

    """
    archive_url = random.choice(docset.urls)
    archive_destination = user_runtime_path("zeal-feeds") / docset.archive
    archive_destination.parent.mkdir(exist_ok=True, parents=True)

    with (
        requests.get(archive_url, stream=True) as r,
        Progress() as progress,
        archive_destination.open("wb") as archive,
    ):
        file_size = int(r.headers["content-length"])
        download_task = progress.add_task(f"Downloading {docset.name}", total=file_size)

        for content in r.iter_content(chunk_size=512):
            archive.write(content)
            progress.update(download_task, advance=len(content))

    return archive_destination
