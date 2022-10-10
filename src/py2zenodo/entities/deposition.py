import json
import os
from dataclasses import dataclass
from pprint import pprint
from typing import Any, Dict, Optional

import requests
from tqdm import tqdm
from tqdm.utils import CallbackIOWrapper

from py2zenodo import utils
from py2zenodo.entities.base import BaseEntity


@dataclass
class Metadata:
    title: str = "new"
    description: str = "none"
    upload_type: str = "dataset"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "metadata": {
                "title": self.title,
                "description": self.description,
                "upload_type": self.upload_type,
            },
        }

    def to_stream(self) -> str:
        return json.dumps(self.to_dict())


class Deposition(BaseEntity):
    def __init__(self, access_token: Optional[str] = None, sandbox: bool = False):
        self.access_token = access_token
        self.api_url = utils.get_url("depositions", sandbox=sandbox)
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

    def create_new_depo(
        self,
        metadata: Optional[Metadata] = None,
        verbose: bool = False,
    ):
        """Create a new deposition for uploading files.

        See https://developers.zenodo.org/#representation

        """
        kwargs = {
            "params": self.get_params(),
            "json": {},
            "headers": {"Content-Type": "application/json"},
        }
        if metadata is not None:
            kwargs["data"] = metadata.to_stream()
        self._r = requests.post(self.api_url, **kwargs)

        if verbose:
            pprint(self._r.json())

    def upload_file(self, filepath: str, pbar: bool = True):
        if not os.path.isfile(filepath):
            raise FileNotFoundError(filepath)

        if not self.connected:
            raise Exception("Not connected")  # XXX:

        file_size = os.stat(filepath).st_size
        print(f"File size: {file_size:,} Bytes")

        bucket_url = self._r.json()["links"]["bucket"]
        filename = os.path.split(filepath)[1]
        upload_url = f"{bucket_url}/{filename}"
        params = self.get_params()

        s = requests.Session()
        s.params.update(params)

        with open(filepath, "rb") as fp:
            # Upload file with progress bar, see
            # https://gist.github.com/tyhoff/b757e6af83c1fd2b7b83057adf02c139
            with tqdm(
                total=file_size,
                unit="B",
                unit_scale=True,
                unit_divisor=1024,
                disable=not pbar,
            ) as t:
                wrapped_file = CallbackIOWrapper(t.update, fp, "read")
                s.put(upload_url, data=wrapped_file)
