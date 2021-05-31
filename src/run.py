#!/usr/bin/env python3

import os
import sys

import yaml

from plot_optimiser import PlotOptimiser
from plot_axes_optimiser import PlotAxesOptimiser
from plot_options_optimiser import PlotOptionsOptimiser

def plot(input_path, x_axis, y_axis, hue_axis, options):
  optimiser = PlotOptimiser(
    input_path=input_path
  )
  saved_space: str = optimiser.decide_plot()
  return saved_space


def plot_options(input_path, x_axis, y_axis, hue_axis, options):
  optimiser = PlotOptionsOptimiser(
    input_path=input_path,
    options=options
  )
  saved_space: str = optimiser.decide_plot()
  return saved_space


def plot_axes(input_path, x_axis, y_axis, hue_axis, options):
  optimiser = PlotAxesOptimiser(
    input_path=input_path,
    x_axis=x_axis,
    y_axis=y_axis,
    hue_axis=hue_axis
  )
  saved_space: str = optimiser.decide_plot()
  return saved_space


if __name__ == "__main__":
  command = sys.argv[1]
  input_path = os.environ["INPUT_PATH"]
  options = os.environ.get("OPTIONS", "")
  x_axis = os.environ.get("X_AXIS", "")
  y_axis = os.environ.get("Y_AXIS", "")
  hue_axis = os.environ.get("HUE_AXIS", "")
  functions = {
    "plot": plot,
    "plot_options": plot_options,
    "plot_axes": plot_axes,
  }
  output = functions[command](input_path, x_axis, y_axis, hue_axis, options)
  print(yaml.dump({"output": output}))
