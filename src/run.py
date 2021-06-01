#!/usr/bin/env python3

import os
import sys

import yaml

from plot_optimiser import PlotOptimiser

def plot(input_path, x_axis, y_axis, hue_axis, options, output_path):
  optimiser = PlotOptimiser(
    input_path=input_path,
    x_axis=x_axis,
    y_axis=y_axis,
    hue_axis=hue_axis,
    options=options,
    output_path=output_path
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
  output_path = os.environ.get("OUTPUT_PATH", "")
  functions = {
    "plot": plot,
  }
  output = functions[command](input_path, x_axis, y_axis, hue_axis, options, output_path)
  print(yaml.dump({"output": output}))
