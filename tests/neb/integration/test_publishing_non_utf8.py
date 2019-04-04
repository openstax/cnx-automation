from tests import markers

from cli.neb import Neb


@markers.neb
@markers.nondestructive
@markers.parametrize("col_id,col_version", [("col23946", "latest")])
def test_get_and_publish_book_with_nonutf8_chars(neb_env, col_id, col_version):
    with Neb.get(env=neb_env, col_id=col_id, col_version=col_version) as book:
        pass  # WIP
        book

    # Download a book which contains non-utf8 characters

    # assert that Neb is decoding the non-utf8 chars for nice presentation

    # On neb publish, assert that (even though Neb has decoded the non-utf8 characters),
    # Neb detects no changes as there have been no other changes.
