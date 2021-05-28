#!/usr/bin/env python3

import os
import sys

import yaml

from optimiser import Optimiser


def downcast(input_path, output_dir):
  # schema = [['integer', 'int32', ['prop_id']]]
  optimiser = Optimiser(
      input_path=input_path,
      output_dir=output_dir,
      # schema=schema,
  )
  saved_space: str = optimiser.downcast_df()
  return saved_space


if __name__ == "__main__":
  command = sys.argv[1]
  input_path = os.environ["INPUTPATH"]
  output_dir = os.environ["OUTPUTDIR"]
  functions = {
    "downcast": downcast,
  }
  output = functions[command](input_path, output_dir)
  print(yaml.dump({"output": output}))
