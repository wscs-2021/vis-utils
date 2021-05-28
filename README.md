# data-utils

A data utility package for Brane.

## Features

Currently, we only have a single feature:

-  Downcast data files, which makes sure that their data types per column are using the most efficient data type memory-wise.

## Installation

Import directly from GitHub:

```sh
brane import wscs-2021/data-utils
```

## Requirements

- pandas
- numpy
- parquet engine, e.g. fastparquet/pyarrow

### Dev requirements

- pytest

## Usage

1. Install dependencies via `pip install -r requirements.txt`.
2. Run via executable:
    ```bash
    INPUTPATH="path/to/input.csv" OUTPUTDIR="path/to/output/folder/" src/run.py downcast
    ```

## Test

Run unit tests with `pytest`:

```sh
pytest
```

Test whether the API is executable:

```sh
make test_executable
```

Test in Brane:

```sh
$ brane --debug test -d . downcast

✔ The function the execute · downcast

Please provide input for the chosen function:

[2021-05-26T10:28:13Z DEBUG] {}
✔ inputpath (string) · /data/downcast/test/sample.csv
[2021-05-26T10:28:23Z DEBUG] {}
✔ outputpath (string) · /data/downcast/test/output.parquet
```

You should now see `output.parquet` in `./downcast/test/output.parquet`.
