# vis-utils

[![example workflow](https://github.com/wscs-2021/vis-utils/actions/workflows/test.yml/badge.svg)](https://github.com/wscs-2021/vis-utils/actions/workflows/test.yml)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.4889434.svg)](https://doi.org/10.5281/zenodo.4889434)

A visualization utility package for Brane.

## Features

Currently, we support three main features:

- `plot`: Automatically plot data set
- `plot_axes`: Plot user defined columns, in a generic plot
- `plot_options`: Plot user defined columns, in user defined plots

## Installation

Import directly from GitHub:

```sh
brane import wscs-2021/vis-utils
```

## Requirements

- pandas
- numpy
- matplotlib
- seaborn

### Dev requirements

- pytest

## Usage

Function **plot**:

`plot(input_path)`

```sh
> import vis-utils;
> plot("path/to/input.csv")
```

Function **plot_options**:

`plot_options(input_path, options)`

```sh
> import vis-utils;
> plot_options("path/to/input.csv", "options")
```

Options example: "[[['species', 'flipper_length_mm', 'sex'], 'violinplot'],[['species', 'bill_length_mm'], 'barplot']]"


Function **plot_axes**:

`plot_axes(input_path, <optional> x_axis, <optional> y_axis, <optional> hue_axis)`

```sh
> import vis-utils;
> plot_axes("path/to/input.csv", (optional)"<column_name>", (optional)"<column_name>", (optional)"<column_name>")
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
$ brane --debug test -d . plot

✔ The function the execute · plot

Please provide input for the chosen function:

[2021-05-26T10:28:13Z DEBUG] {}
✔ input_path (string) · /data/plot/test/penguins.csv
```

You should now see `<figure_name>.png` in `./<figure_name>.png`.
