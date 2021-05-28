import numpy as np
from os import path


def format_bytes_string(_bytes, decimals=2):
    if _bytes < 10**3:
        return f"{_bytes} Bytes"
    elif _bytes < 10**6:
        return f"{round(_bytes/10**3, decimals)} KB"
    elif _bytes < 10**9:
        return f"{round(_bytes/10**6, decimals)} MB"
    elif _bytes < 10**12:
        return f"{round(_bytes/10**9, decimals)} GB"
    elif _bytes < 10**15:
        return f"{round(_bytes/10**12, decimals)} TB"


def str_to_dtype(s_dtype):
    dtypes = {
        'int8': np.int8,
        'int16': np.int16,
        'int32': np.int32,
        'int64': np.int64,
        'uint8': np.uint8,
        'uint16': np.uint16,
        'uint32': np.uint32,
        'uint64': np.uint64,
        'float16': np.float16,
        'float32': np.float32,
        'float64': np.float64,
        'bool': bool,
    }
    try:
        print(s_dtype)
        return dtypes[s_dtype]
    except KeyError:
        raise Exception(f'Data type {s_dtype} not supported.')

def validate_filepath(p, type='input'):
    fname, extension = path.splitext(p)

    if extension not in ['.json', '.csv', '.parquet']:
        raise Exception(f'{type.capitalize()} file type not supported')


def find_optimal_int_dtype(min, max):
    if min == 0 and max == 1:
        return np.bool_
    elif min >= 0:
        if max <= 255:
            return np.uint8
        elif max <= 65535:
            return np.uint16
        elif max <= 4294967295:
            return np.uint32
        else:
            return np.uint64
    else:
        if min >= -128 and max <= 127:
            return np.int8
        elif min >= -32768 and max <= 32767:
            return np.int16
        elif min >= -2147483648 and max <= 2147483647:
            return np.int32
        else:
            return np.int64