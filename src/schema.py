from utils import str_to_dtype
from parameter import IntParameter, FloatParameter, NominalParameter, OrdinalParameter


###############
# EXCPETIONS
###############
class SchemaParameterException(Exception):
    pass


####################
# PARAMETER PARSERS
####################
class SchemaParser:
    def parse(self, line):
        parser = self._get_parser(line)
        return parser(line)

    def _get_parser(self, line):
        var_type = line[0]
        data_type = line[1]

        if var_type == 'integer':
            return self._parse_int_parameter
        elif var_type == 'float':
            return self._parse_float_parameter
        elif var_type == 'categorical':
            if data_type == 'nominal':
                return self._parse_nominal_parameter
            elif data_type == 'ordinal':
                return self._parse_ordinal_parameter
        else:
            raise Exception(f'Error in schema: the variable type {var_type} is not yet supported.')

    @staticmethod
    def _parse_int_parameter(param):

        if len(param) < 3 or len(param) > 3:
            raise SchemaParameterException(
                f'Nominal schema parameter error. Expected exactly 3 elements, got {len(param)}')

        data_type = str_to_dtype(param[1])
        variable_names = param[2]

        for var in variable_names:
            yield IntParameter(
                data_type=data_type,
                variable_name=var,
            )

    @staticmethod
    def _parse_float_parameter(param):

        if len(param) < 3:
            raise SchemaParameterException(
                f'Nominal schema parameter error. Expected at least 3 elements, got {len(param)}')

        if len(param) > 4:
            raise SchemaParameterException(
                f'Nominal schema parameter error. Expected at most 4 elements, got {len(param)}')

        data_type = str_to_dtype(param[1])
        variable_names = param[2]
        float_precision = param[3] if len(param) == 4 else 6

        for var in variable_names:
            yield FloatParameter(
                data_type=data_type,
                variable_name=var,
                float_precision=float_precision
            )

    @staticmethod
    def _parse_nominal_parameter(param):

        if len(param) < 3:
            raise SchemaParameterException(f'Nominal schema parameter error. Expected at least 3 elements, got {len(param)}')

        if len(param) > 4:
            raise SchemaParameterException(f'Nominal schema parameter error. Expected at most 4 elements, got {len(param)}')

        data_type = param[1]
        variable_names = param[2]
        nested_categories = param[3] if len(param) == 4 else None

        for (idx, var) in enumerate(variable_names):
            categories = nested_categories[idx] if len(nested_categories) > idx else None
            yield NominalParameter(
                data_type=data_type,
                variable_name=var,
                categories=categories
            )

    @staticmethod
    def _parse_ordinal_parameter(param):

        if len(param) < 4 or len(param) > 4:
            raise SchemaParameterException(
                f'Nominal schema parameter error. Expected exactly 4 elements, got {len(param)}')

        data_type = param[1]
        variable_names = param[2]
        nested_orders = param[3]

        for (idx, var) in enumerate(variable_names):
            yield OrdinalParameter(
                data_type=data_type,
                variable_name=var,
                order=nested_orders[idx]
            )


class Schema:

    def __init__(self, schema):
        '''
        The Schema class parses the schema input
        Example Schema
        # schema = [
        #     ['integer', 'int32', ['var1', 'var2']],
        #     ['float', 'float32', ['var3', 'var4']],
        #     ['nominal', ['var5']],
        #     ['ordinal', ['var6'], ['apple', 'orange']]
        # ]
        @param schema: nested array
        '''

        self.parameters = []

        schema_param_parser = SchemaParser()

        for line in schema:
            for parameter in schema_param_parser.parse(line):
                self.parameters.append(parameter)
