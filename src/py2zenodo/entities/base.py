from typing import Any, Dict, Optional

import requests

from py2zenodo import utils


class BaseEntity:

    url_key: str = "none"

    def __init__(self, access_token: Optional[str], sandbox: bool = False):
        self.access_token = access_token
        self.api_url = utils.get_url(self.url_key, sandbox=sandbox)
        self._r = None

    @property
    def connected(self) -> bool:
        return self.r is not None and self.r.ok

    @property
    def r(self) -> Optional[requests.Response]:
        return self._r

    def get_params(self, **kwargs) -> Dict[str, Any]:
        params = {"access_token": self.access_token}
        params.update({i: j for i, j in kwargs.items() if j is not None})
        return params


class BaseDepositionEntity(BaseEntity):

    url_key: str = "depositions"


class BaseRecordEntity(BaseEntity):

    url_key: str = "records"
