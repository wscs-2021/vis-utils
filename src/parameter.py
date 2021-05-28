import numpy as np
import logging


###############
# PARAMETERS
###############
class GenericParameterFactory:
    @staticmethod
    def create_parameter(series):
        if series.dtype in [np.int16, np.int32, np.int64]:
            return GenericParameter(variable_name=series.name, variable_type='integer')
        elif series.dtype.type is np.float64:
            return GenericParameter(variable_name=series.name, variable_type='float')
        else:
            logging.warning(f"Series of type '{series.dtype}' is not yet supported.")


class GenericParameter:
    def __init__(self, variable_name, variable_type):
        self.data_type = None
        self.variable_name = variable_name
        self.variable_type = variable_type


class IntParameter:
    def __init__(self, data_type, variable_name):
        self.data_type = data_type
        self.variable_name = variable_name
        self.variable_type = 'integer'


class FloatParameter:
    def __init__(self, data_type, variable_name, float_precision):
        self.data_type = data_type
        self.variable_name = variable_name
        self.variable_type = 'float'
        self.float_precision = float_precision


class NominalParameter:
    def __init__(self, data_type, variable_name, categories):
        self.data_type = data_type
        self.variable_name = variable_name
        self.variable_type = 'categorical'
        self.categories = categories


class OrdinalParameter:
    def __init__(self, data_type, variable_name, order):
        self.data_type = data_type
        self.variable_name = variable_name
        self.variable_type = 'categorical'
        self.order = order