from typing import Tuple

import click

from py2zenodo import Deposition
from py2zenodo.utils import check_files


@click.command()
@click.argument("files", nargs=-1, type=click.Path())
@click.option("-t", "--token", help="Access token.")
@click.option("-s", "--sandbox", is_flag=True, help="Use sandbox.")
@click.option("-v", "--verbose", is_flag=True)
def main(files: Tuple[str, ...], token: str, sandbox: bool, verbose: bool):
    check_files(files)
    depo = Deposition(access_token=token, sandbox=sandbox)
    depo.create_new_depo(verbose=verbose)
    for file in files:
        depo.upload_file(file)
