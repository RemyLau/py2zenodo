import logging
from pprint import pformat
from typing import Any, Dict, List, Optional, Union

import requests

from py2zenodo import config
from py2zenodo.entities.base import BaseRecordEntity

logger = logging.getLogger(__name__)


class Record(BaseRecordEntity):
    def __init__(
        self,
        raw: Optional[Union[Dict[str, Any], str]] = None,
        /,
        *,
        access_token: Optional[str] = None,
        sandbox: bool = False,
        load_latest: bool = False,
    ):
        super().__init__(access_token, sandbox)

        if raw is None:
            self._raw = {}
        elif isinstance(raw, str):
            self.load_from_recid(raw, load_latest)
        else:
            self.raw = raw

    def load_from_recid(self, recid: str, load_latest: bool = False):
        r = requests.get(url := f"{self.api_url}/{recid}")
        logger.info(f"Loading record from {url}")
        if not r.ok:
            raise requests.exceptions.RequestException(r)
        self.raw = r.json()

        if load_latest and (self.latest_recid != self.id):
            logger.info(
                f"Found latest version {self.latest_recid} for the current "
                f"concept {self.conceptrecid}.",
            )
            self.load_from_recid(self.latest_recid, False)

    @property
    def raw(self) -> Dict[str, Any]:
        return self._raw

    @raw.setter
    def raw(self, raw: Dict[str, Any]):
        unknowns = [i for i in raw if i not in config.RECORD_ATTRS]
        if unknowns:
            raise ValueError(
                f"{len(unknowns)} out of {len(config.RECORD_ATTRS)} record "
                f"attributes are unknown: {unknowns}",
            )
        self._raw = raw
        logger.info(f"Loaded record {self.id}")

    @property
    def conceptdoi(self) -> Optional[str]:
        return self.getattr("conceptdoi")

    @property
    def conceptrecid(self) -> Optional[str]:
        return self.getattr("conceptrecid")

    @property
    def doi(self) -> Optional[str]:
        return self.getattr("doi")

    @property
    def id(self) -> Optional[str]:
        return self.getattr("id")

    @property
    def links(self) -> Optional[Dict[str, str]]:
        return self.getattr("links")

    @property
    def latest_link(self) -> str:
        return self.links.get("latest")

    @property
    def latest_recid(self) -> str:
        return self.latest_link.split("/")[-1]

    @property
    def metadata(self) -> Optional[Dict[str, str]]:
        return self.getattr("metadata")

    @property
    def title(self) -> str:
        return self.metadata.get("title")

    def getattr(self, name):
        if name not in config.RECORD_ATTRS:
            raise AttributeError(f"Unknown record attribute {name!r}")
        return self.raw.get(name)

    def show(self):
        return pformat(self.raw)


class Records(BaseRecordEntity):
    def __init__(
        self,
        q: Optional[str] = None,
        /,
        *,
        access_token: Optional[str] = None,
        sandbox: bool = False,
        **kwargs,
    ):
        super().__init__(access_token, sandbox)
        self._records = []

        if q is not None:
            self.load_from_query(q, **kwargs)

    def __len__(self) -> int:
        return len(self._records)

    def __getitem__(self, i: int) -> Record:
        return self.records[i]

    def __iter__(self):
        yield from self.records.__iter__()

    @property
    def records(self) -> List[Record]:
        return self._records

    @property
    def conceptdois(self) -> List[str]:
        return [i.conceptdoi for i in self]

    @property
    def conceptrecids(self) -> List[str]:
        return [i.conceptrecid for i in self]

    @property
    def dois(self) -> List[str]:
        return [i.doi for i in self]

    @property
    def ids(self) -> List[str]:
        return [i.id for i in self]

    @property
    def titles(self) -> List[str]:
        return [i.title for i in self]

    def add_record(self, rec: Union[Record, Dict[str, Any]]):
        self._records.append(rec if isinstance(rec, Record) else Record(rec))

    def _query(
        self,
        q: str,
        /,
        *,
        all_versions: bool = True,
        **kwargs,
    ) -> requests.Response:
        params = self.get_params(q=q, all_versions=1 if all_versions else 0, **kwargs)
        r = requests.get(self.api_url, params=params)
        if not r.ok:
            raise requests.exceptions.RequestException(r)

        return r

    def load_from_query(self, q: str, /, *, all_versions: bool = True, **kwargs):
        r = self._query(q, all_versions=all_versions, **kwargs)

        for rec in r.json()["hits"]["hits"]:
            self.add_record(rec)
