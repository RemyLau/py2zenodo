import logging
from typing import Any, Dict, Optional, Union

import requests

from py2zenodo import utils

logger = logging.getLogger(__name__)


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
