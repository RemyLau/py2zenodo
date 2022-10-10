import os
from pprint import pformat
from typing import Tuple, Union
from urllib.parse import urljoin

from py2zenodo import config

logger = config.get_logger(__name__)


def get_url(where, /, *, sandbox: bool = False) -> str:
    if (url := config.URL_DICT.get(where)) is None:
        raise ValueError(f"Invalid url option {where!r}")

    url_base = config.URL_BASE_SANDBOX if sandbox else config.URL_BASE_ZENODO
    url_full = urljoin(url_base, url)
    logger.debug(f"{where=}, {sandbox=}, url: {url_full}")

    return url_full


def check_files(files: Union[str, Tuple[str, ...]]):
    files = [files] if isinstance(files, str) else files

    failed_list = []
    for file in files:
        if not os.path.isfile(file):
            failed_list.append(file)

    if failed_list:
        raise FileNotFoundError(
            f"{len(failed_list)} out of {len(files)} not found:\n"
            f"{pformat(failed_list)}",
        )
