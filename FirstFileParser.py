import json
from jsonschema import validate
from jsonschema import FormatChecker


class FFParser:
    """Parser for first log file"""

    def __init__(self, **params):
        if 'schema' in params:
            self.schema = params['schema']
            self.__validate = True
        else:
            self.__validate = False


    def parse(self, file_path, **params):
        result = {}
        with open(file_path) as file:
            result = self.parse_json(json.load(file), **params)

        return result


    def parse_json(self, file_data, **params):
        if self.__validate:
            self.__validate_json(file_data)

        result = {}

        if 'logs' not in file_data:
            return result

        for test_log in file_data['logs']:
            test = self.__parse_test_log(test_log)
            # if there are no duplicate keys
            if len(test.keys() & result.keys()) == 0:
                result.update(test)
            else:
                raise KeyError('Two tests have the same "time". We cannot distinguish them.')

        return result

    def __parse_test_log(self, test_log, **params):
        if 'time' not in test_log:
            raise KeyError('Field \'time\' is required!')

        result = {}

        time = int(test_log['time'])
        result[time] = {}

        if 'test' in test_log:
            result[time]['name'] = test_log['test']
        else:
            raise KeyError('Field \'test\' is required!')

        if 'output' in test_log:
            result[time]['status'] = test_log['output']
        else:
            raise KeyError('Field \'output\' is required!')

        return result

    def __validate_json(self, data, **params):
            validate(data, schema=self.schema, format_checker=FormatChecker())
