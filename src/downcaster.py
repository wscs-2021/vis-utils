import numpy as np
from utils import find_optimal_int_dtype


class Downcaster:

    def downcast(self, series, parameter):
        downcaster = self._get_downcaster(parameter)
        return downcaster(series, parameter)

    def _get_downcaster(self, parameter):
        if parameter.variable_type == 'integer':
            return self._downcast_int
        elif parameter.variable_type == 'float':
            return self._downcast_float
        elif parameter.variable_type == 'categorical':
            if parameter.data_type == 'nominal':
                return self._downcast_nominal
            elif parameter.data_type == 'ordinal':
                return self._downcast_ordinal
            else:
                raise Exception(f'The data type {parameter.data_type} is not supported yet')
        else:
            raise Exception(f'The variable type {parameter.variable_type} is not supported yet')

    @staticmethod
    def _downcast_int(series, parameter):
        # if self.verbose: print(f"Attempting downcast on '{series.name}'")

        if parameter.data_type is None:
            target_dtype = find_optimal_int_dtype(min=series.min(), max=series.max())
        else:
            target_dtype = parameter.data_type

        if series.dtype != target_dtype:
            # if self.verbose: print(f"\tDowncast integer: {series.dtype} -> {np.dtype(target_dtype).name}")
            return series.astype(target_dtype)
        else:
            # if self.verbose: print(f"\tNo downcast.")
            return series

    @staticmethod
    def _downcast_float(series, parameter):
        if parameter.data_type is None:
            ndigits = len(str(int(series.max())))

            if hasattr(parameter, 'float_precision'):
                fprecision = ndigits + parameter.float_precision
            else:
                fprecision = ndigits + 6

            print(fprecision)
            if fprecision > 8:
                target_dtype = np.float64
            else:
                target_dtype = np.float32
        else:
            target_dtype = parameter.data_type

        if series.dtype != target_dtype:
            # if self.verbose: print(f"\tDowncast float: {series.dtype} -> {np.dtype(target_dtype).name}")
            return series.astype(target_dtype)
        else:
            # if self.verbose: print(f"\tNo downcast.")
            return series

    @staticmethod
    def _downcast_nominal(series, parameter):

        if parameter.categories:
            categories = parameter.categories
        else:
            categories = series.unique()
            if len(categories) > 0.5 * series.shape[0]:
                return series

        mapper = {key: value for (value, key) in enumerate(categories)}
        dtype = find_optimal_int_dtype(0, len(categories)-1)
        return series.map(mapper).astype(dtype)

    @staticmethod
    def _downcast_ordinal(series):
        return series

    @staticmethod
    def _downcast_interval(series):
        return series

    @staticmethod
    def _downcast_ratio(series):
        return series