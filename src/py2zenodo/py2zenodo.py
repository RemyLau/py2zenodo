import logging
import os
from typing import Any, Dict, Optional, Union

import requests
from tqdm import tqdm
from tqdm.utils import CallbackIOWrapper

from py2zenodo import utils

logger = logging.getLogger(__name__)

ZENODO_URL = "https://zenodo.org/api/deposit/depositions"
SANDBOX_URL = "https://sandbox.zenodo.org/api/deposit/depositions"


def upload(filepath, access_token):
    params = {"access_token": access_token}
    print(f"{params=!r}")

    s = requests.Session()
    s.params.update(params)

    r = s.post(ZENODO_URL, json={})
    if not r.ok:
        msg = r.json().get("message", "")
        raise requests.exceptions.HTTPError(f"{r!r} {msg}")

    # TODO: check if file exist
    file_size = os.stat(filepath).st_size
    print(f"File size: {file_size:,} Bytes")

    # Upload file with progress bar, see
    # https://gist.github.com/tyhoff/b757e6af83c1fd2b7b83057adf02c139
    bucket_url = r.json()["links"]["bucket"]
    upload_url = f"{bucket_url}/{filepath.name}"
    with open(filepath, "rb") as fp:
        with tqdm(total=file_size, unit="B", unit_scale=True, unit_divisor=1024) as t:
            wrapped_file = CallbackIOWrapper(t.update, fp, "read")
            s.put(upload_url, data=wrapped_file)

    print("Done.")


def get_records(
    q: Optional[str] = None,
    all_versions: bool = True,
    sandbox: bool = False,
    return_response: bool = False,
    **kwargs,
) -> Union[requests.Response, Dict[str, Any]]:
    """Search for Zenodo records.

    Args:
        q: Query string.
        all_versions: Get all versions if set to True.
        return_response: Return the full response object if set to True,
            otherise only return the JSON.

    See https://developers.zenodo.org/#records

    """
    params = {"q": q, "all_versions": 1 if all_versions else 0}
    params.update(kwargs)

    url = utils.get_url("records", sandbox=sandbox)
    r = requests.get(url, params=params)

    if return_response:
        return r
    elif not r.ok:
        raise requests.exceptions.RequestsException(r)
    else:
        return r.json()
