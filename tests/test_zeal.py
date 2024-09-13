"""Test functionality in the `zeal` module."""

from zeal_feeds.zeal import Zeal
from zeal_feeds.user_contrib import DocSet, DocSetAuthor


def test_docset_install(data_folder, tmp_path) -> None:

    docset_name = "wxPython"
    docset_archive = "wxPython.tgz"

    zeal = Zeal(tmp_path)
    docset_tarball = data_folder / docset_archive

    docset_meta = DocSet(
        name=docset_name,
        author=DocSetAuthor(
            name="",
            link="",
        ),
        archive=docset_archive,
        version="",
    )

    zeal.install_docset(docset_meta, docset_tarball)
    print("Directory contents:", list(tmp_path.iterdir()))
    assert (tmp_path / f"{docset_name}.docset").is_dir()
