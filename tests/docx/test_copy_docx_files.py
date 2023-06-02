import os

from zipfile import ZipFile


def test_copy_docx_files():
    base_to_dir = "/Users/om9/Documents/Projects/cnx-automation"
    base_from_dir = "/Users/om9/downloads"

    zip_file_old = (
        "openstax-osbooks-astronomy-4c7cc35c6b5b84bf37f1afaf6126c2f98f9520d0-git-2462-docx.zip"
    )
    zip_file_new = (
        "openstax-osbooks-astronomy-4db9073bf550e6e95ee66092ee243bacda3aff85-git-2607-docx.zip"
    )

    from_dir_old = f"{base_from_dir}/{zip_file_old}"
    to_old_dir = f"{base_to_dir}/docxs_old"

    from_dir_new = f"{base_from_dir}/{zip_file_new}"
    to_new_dir = f"{base_to_dir}/docxs_new"

    os.system(f"sudo cp {from_dir_old} {to_old_dir}")
    os.system(f"sudo cp {from_dir_new} {to_new_dir}")

    with ZipFile(f"{base_to_dir}/docxs_old/{zip_file_old}", "r") as zobj:
        zobj.extractall(path=to_old_dir)

    with ZipFile(f"{base_to_dir}/docxs_new/{zip_file_new}", "r") as zobj:
        zobj.extractall(path=to_new_dir)
