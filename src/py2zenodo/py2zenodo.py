import os

import requests
from tqdm import tqdm
from tqdm.utils import CallbackIOWrapper


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
        with tqdm(total=file_size, unit="B", unit_scale=True, unit_divisor=2**20) as t:
            wrapped_file = CallbackIOWrapper(t.update, fp, "read")
            s.put(upload_url, data=wrapped_file)

    print("Done.")
