#!/usr/bin/env python3

import os
import sys

from typing import Union
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

def get_env_var(key: str) -> Union[str, None]:
  """Returns environment variable by key. 
  If the value is an empty string, it returns None instead.

  Args:
      key (str): env var key

  Returns:
      Union[str, None]: value of the env var
  """
  result = os.environ.get(key, None)
  if result == "" or result == "\"\"":
    return None
  return result

if __name__ == "__main__":
  command = sys.argv[1]
  input_path = get_env_var("INPUT_PATH")
  options = get_env_var("OPTIONS")
  x_axis = get_env_var("X_AXIS")
  y_axis = get_env_var("Y_AXIS")
  hue_axis = get_env_var("HUE_AXIS")
  output_path = get_env_var("OUTPUT_PATH")
  functions = {
    "plot": plot,
  }
  output = functions[command](input_path, x_axis, y_axis, hue_axis, options, output_path)
  print(yaml.dump({"output": output}))
