import pandas as pd
from os import path

from pathlib import Path

from utils import format_bytes_string
from schema import Schema
from downcaster import Downcaster
from parameter import GenericParameterFactory


class Optimiser:

    def __init__(self, input_path, output_dir, schema=None, float_precision=None, verbose=False):
        """
        The DataTypeOptimiser handles the context for optimising the datatypes in the provided dataset. It reads
        the input file, applies the downcasting and writes the final file to disk.
        @param input_path: string, path to input dataset file
        @param output_path: string, path to output dataset file
        @param schema: nested array
        @param float_precision: int, minimum decimal places for floats
        @param verbose: bool, True or False
        """
        self.df = None
        self.input_path = input_path
        self.output_dir = output_dir

        self.verbose = verbose
        self.float_precision = float_precision if float_precision is not None else 6

        self.pre_d_u = None
        self.pre_mem_u = None
        self.post_d_u = None
        self.post_mem_u = None

        self.schema = Schema(schema) if schema else None

        self._read_input()

    def _read_input(self):
        i_ftype = self.input_path.split('.')[-1]

        if i_ftype == 'csv':
            self.df = pd.read_csv(self.input_path)
        elif i_ftype == 'json':
            self.df = pd.read_json(self.input_path)
        elif i_ftype == 'parquet':
            self.df = pd.read_parquet(self.input_path)

        self.pre_d_u = round(Path(self.input_path).stat().st_size, 2)
        self.pre_mem_u = round(self.df.memory_usage().sum(), 2)

    def _write_output(self):
        filename = path.splitext(self.input_path)[0].split('/')[-1]
        output_path = path.join(self.output_dir, f'{filename}_opt.parquet')
        self.df.to_parquet(output_path)

        self.post_d_u = round(Path(output_path).stat().st_size, 2)
        diff_d_u = (self.post_d_u - self.pre_d_u) / self.pre_d_u

        self.post_mem_u = round(self.df.memory_usage().sum(), 2)
        diff_mem_u = (self.post_mem_u - self.pre_mem_u) / self.pre_mem_u

        return (f"Wrote optimised file to a parquet file.\n"
                f"\tDisk Usage: {format_bytes_string(self.pre_d_u)} -> {format_bytes_string(self.post_d_u)} ({round(diff_d_u * 100, 2)}%)\n"
                f"\tMemory Usage: {format_bytes_string(self.pre_mem_u)} -> {format_bytes_string(self.post_mem_u)} ({round(diff_mem_u * 100, 2)}%)\n")

    def downcast_df(self):
        '''
        Goes through each columns in the dataframe to apply appropriate downcasting. Where available, the schema will be
        used and take priority. Otherwise, an estimation of the best downcasting for each data type is made (currently
        only for int, float and nominal datatypes).

        After downcasting, the new dataset is written to a file.
        @return: None
        '''

        downcaster = Downcaster()
        parameter_factory = GenericParameterFactory()
        downcasted_columns = []

        # 1. Apply schema
        if self.schema:
            for parameter in self.schema.parameters:
                column = parameter.variable_name
                downcasted_columns.append(column)
                self.df[column] = downcaster.downcast(self.df[column], parameter)

        # 2. Apply
        for column in self.df.columns:
            if column in downcasted_columns:
                continue

            parameter = parameter_factory.create_parameter(self.df[column])

            if parameter:
                self.df[column] = downcaster.downcast(self.df[column], parameter)

        return self._write_output()