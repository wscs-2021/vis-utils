from os import path, remove

import numpy as np
import pandas as pd
from optimiser import Optimiser
from schema import Schema

dummy_input_path = 'tests/dummy_data/dummy.csv'
dummy_output_dir =  'tests/dummy_data/'
dummy_output_filename = 'dummy_opt.parquet'

optimiser = Optimiser(
    input_path=dummy_input_path,
    output_dir=dummy_output_dir,
    schema=None,
    verbose=True
)


def test_downcast_int():
    data = {
        's_bool': pd.Series([0, 1]),
        's_uint8': pd.Series([0, 254]),
        's_uint16': pd.Series([254, 65535]),
        's_uint32': pd.Series([65535, 4294967295]),
        's_uint64': pd.Series([4294967296, 4294967297]),
        's_int8': pd.Series([-128, 127]),
        's_int16': pd.Series([-32768, 32767]),
        's_int32': pd.Series([-2147483648, 2147483647]),
        's_int64': pd.Series([-2147483649, 2147483648])
    }
    df = pd.DataFrame(data)
    optimiser.df = df
    optimiser.downcast_df()

    assert df.s_bool.dtype == bool
    assert df.s_uint8.dtype == np.uint8
    assert df.s_uint16.dtype == np.uint16
    assert df.s_uint32.dtype == np.uint32
    assert df.s_uint64.dtype == np.uint64
    assert df.s_int8.dtype == np.int8
    assert df.s_int16.dtype == np.int16
    assert df.s_int32.dtype == np.int32
    assert df.s_int64.dtype == np.int64


def test_downcast_float():
    data = {
        's_float32': pd.Series([12.3456]),
        's_float64': pd.Series([1234.56789]),
    }

    df = pd.DataFrame(data)
    optimiser.df = df
    optimiser.downcast_df()

    assert df.s_float32.dtype == np.float32
    assert df.s_float64.dtype == np.float64


def test_downcast_nominal():
    schema = Schema([['categorical', 'nominal', ['s_cat1', 's_cat2', 's_object'], [['apple', 'orange']]]])
    optimiser.schema = schema

    data = {
        's_cat1': pd.Series(['apple', 'orange', 'apple', 'orange', 'apple', 'orange']), #  categories are passed through schema
        's_cat2': pd.Series(['apple', 'orange', 'apple', 'orange', 'apple', 'orange']),
        's_object': pd.Series(['apple', 'orange', 'banana'])
    }

    df = pd.DataFrame(data)
    optimiser.df = df
    optimiser.downcast_df()

    assert df.s_cat1.dtype == bool
    assert df.s_cat2.dtype == bool
    assert df.s_object.dtype == object

    optimiser.schema = None

def test_schema_passed_dtype():
    schema = Schema([['integer', 'int8', ['s_passed_dtype']]])
    optimiser.schema = schema

    df = pd.DataFrame({'s_passed_dtype': pd.Series([1, 2, 3])})
    optimiser.df = df
    optimiser.downcast_df()
    assert df.s_passed_dtype.dtype == np.int8

    optimiser.schema = None


def test_file_saving():
    # 1. If dummy file exists delete it
    dummy_output_path = path.join(dummy_output_dir, dummy_output_filename)
    if path.exists(dummy_output_path):
        remove(dummy_output_path)

    # 2. Call function
    data = {
        'int32': pd.Series([1, 2, 3]),
    }

    df = pd.DataFrame(data)
    optimiser.df = df
    optimiser.downcast_df()

    # 3. Check if dummy file exists
    assert path.exists(dummy_output_path) is True

    # 3bis. Check content

    # 4. Cleanup
    if path.exists(dummy_output_path):
        remove(dummy_output_path)
