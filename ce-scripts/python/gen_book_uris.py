"""CNX Book URI Generator: Generate URLS for cnx.org book for testing
Usage:
  gen_book_urls.py <archive_host> <cnx_id>
  gen_book_urls.py (-h | --help)

"""
import os

from docopt import docopt
from rex_redirects import generate_cnx_uris

HERE = os.path.abspath(os.path.dirname(__file__))

OUTPUT_DIR = os.path.join(HERE, "output")


def cli():
    arguments = docopt(__doc__)

    # Assign arguments to variables
    archive_host = arguments["<archive_host>"]
    cnx_id = arguments["<cnx_id>"]

    with open(os.path.join(OUTPUT_DIR, f"{cnx_id}.txt"), "w") as outfile:
        for uri in generate_cnx_uris(archive_host, cnx_id):
            outfile.write(f"{uri}\n")

    print("uris generated successfully")


if __name__ == "__main__":
    cli()
