[![PyPI version](https://badge.fury.io/py/py2zenodo.svg)](https://badge.fury.io/py/py2zenodo)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)

# py2zenodo

A Python wrapper for Zenodo REST API

## Installation

We use [Poetry](https://python-poetry.org/) to manage this package.
To install py2zenodo, run the following at the project root directory

```bash
poetry install
```

## Use cases

### Getting record information

For all examples below, we will use the Zenodo record `1145370` that was created
for demonstration and testing purposes for `py2zenodo`.

#### Get record information using the record identifier

```python
from py2zenodo import Record

# Load information about a particular record given the record id
# Note: the sandbox option indicates that this is a sandbox record (https://sandbox.zenodo.org).
# For ordinary Zenodo record, set sandbox=False, or simply ignore this option.
rec = Record("1145370", sandbox=True)

# Print some key information about this record
print(rec.title)  # title of this record
print(rec.doi)  # doi of this record
print(rec.latest_link)  # link to the latest version of this record
print(rec.latest_recid)  # record id of the latest version of this record
print(rec.files)  # information about available files in this record

# Show all information associated with the record
print(rec.raw)  # alternatively, use `print(rec.show())` to print nicely formatted json
```

All available properties for `Record`:
- `conceptdoi`
- `conceptrecid`
- `doi`
- `files`
- `id`
- `latest_link`
- `latest_recid`
- `links`
- `metadata`
- `title`
- `raw`

#### Query records given a query string

```python
from py2zenodo import Records

# Query records with a query string
recs = Record("py2zenodo", sandbox=True)

# Print information about the records obtained from the query
print(rec.titles)
print(rec.dois)

# Get a particular record by indexing
rec = recs[0]
```

All available properties for `Records`:
- `conceptdois`
- `conceptrecids`
- `dois`
- `ids`
- `records`
- `titles`

#### Get all versions of a particular record

```python
from py2zenodo import Record, Records

# Load a record
rec = Record("1145373")

# Load all versions of that record by using the concept record identifier
recs = Records(rec.conceptrecid)
```
