# vis-utils

[![example workflow](https://github.com/wscs-2021/vis-utils/actions/workflows/test.yml/badge.svg)](https://github.com/wscs-2021/vis-utils/actions/workflows/test.yml)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.4889434.svg)](https://doi.org/10.5281/zenodo.4889434)

A visualization utility package for Brane.

## Features

Currently, we support three main features in one function:

- `plot`: 
  - Automatically plot data set
  - Plot user defined columns, in a generic plot
  - Plot user defined columns, in user defined plots

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

```
plot(input_path, 
    <optional> x_axis, 
    <optional> y_axis, 
    <optional> hue_axis, 
    <optional> options, 
    <optional> output_path)
```

### Examples

> Empty strings `""` indicate `None`.

Plot all:

```sh
> import vis-utils;
> plot("path/to/input.csv", 
      "", 
      "", 
      "", 
      "", 
      ""
  )
```

Plot with options:

```sh
> import vis-utils;
> plot("path/to/input.csv", 
      "", 
      "", 
      "", 
      [
        [['species', 'flipper_length_mm', 'sex'], 'violinplot'],
        [['species', 'bill_length_mm'], 'barplot']
      ],
      ""
  )
```

Plot with axes given:

```sh
> import vis-utils;
> plot("path/to/input.csv", 
      "species", 
      "island", 
      "", 
      "",
      ""
  )
```

### Arguments

- REQUIRED `input_path`: string, path to .csv/.json/.parquet data file
    - Example: "tests/dummy_data/penguins.csv"
- OPTIONAL `x_axis`: string, column name of desired x_axis
    - Example: "species"
    - Default: None
- OPTIONAL `y_axis`: string, column name of desired y_axis
    - Example: "flipper_length_mm"
    - Default: None
- OPTIONAL `hue_axis`: string, column name of desired hue_axis
    - Example: "sex"
    - Default: None
- OPTIONAL `options`: string, list of sublists, containing [subsublist of column names] and a plot name 
    - Example: `"[[['species', 'sex'], 'barplot'],[['species', 'flipper_length_mm'],'violinplot']]"`
    - Possible plot names: `'relplot', 'scatterplot', 'lineplot', 'displot', 'histplot', 'kdeplot',
      'ecdfplot', 'rugplot', 'catplot', 'stripplot', 'swarmplot', 'boxplot',
      'violinplot', 'pointplot', 'barplot'`
    - Default: None
- OPTIONAL `output_path`: string, path to directory where figures will be written
    - Example: "tests"
    - Default: None

### Notes

- Omitting an optional parameter can be done by passing an empty string `""`, e.g. `plot("path/to/input.csv", "species", "island", "", "" ,"")`
- If no optional params are given, the function automatically plots all possible columns
- If options is given, axes will be disregarded
- Not all axes need to be specified, all three can be combined in any way (e.g. pass only x_axis and hue_axis)
- If `output_path` is not specified, it will output to the same directory as the `input_path`

### Output

- Output text: string, paths to files and/or possible errors
- Output files: .png, plots in (optional) output_path

## Automatic Plotting
The following plots are chosen for automatic plotting of data

**No axes and options given**:
- x_axis (string) and y_axis (string): `catplot`
- Else: `barplot`

**Axes given (no options)**:
- Only x_axis: `displot`
- Else: `catplot`

## Test

Run unit tests with `pytest`:

```sh
pytest
```

Test whether the API is executable:

```sh
make test_plot_executable
make test_options_executable
make test_axes_executable
```

Test in Brane:

```sh
$ brane --debug test -d . plot

✔ The function the execute · plot

Please provide input for the chosen function:

[2021-05-26T10:28:13Z DEBUG] {}
✔ input_path (string) · /data/plot/test/penguins.csv
```

You should now see `<figure_name>.png` in `/data/plot/test/<figure_name>.png`.
