from datetime import datetime
from datetime import timezone
from jsonschema import validate
from jsonschema import FormatChecker
import json


class SFParser:
    """Parser for second log file"""

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

        if 'suites' not in file_data:
            return result

        for suite in file_data['suites']:
            suite_cases = self.__parse_suites_log(suite)
            # if there are no duplicate keys
            if len(suite_cases.keys() & result.keys()) == 0:
                result.update(suite_cases)
            else:
                raise KeyError('Two tests have the same "time". We cannot distinguish them.')

        return result

    def __parse_suites_log(self, suite, **params):
        result = {}

        if 'cases' not in suite:
            return result

        for test_log in suite['cases']:
            case_test = self.__parse_test_log(test_log)
            # if there are no duplicate keys
            if len(case_test.keys() & result.keys()) == 0:
                result.update(case_test)
            else:
                raise KeyError('Two tests have the same "time". We cannot distinguish them.')

        return result

    def __parse_test_log(self, test_log, **params):
        if 'time' not in test_log:
            raise KeyError('Field \'time\' is required!')

        result = {}
        time = datetime.strptime(test_log['time'], '%A, %d-%b-%y %H:%M:%S %Z')
        time = int(time.replace(tzinfo=timezone.utc).timestamp())
        result[time] = {}

        if 'name' in test_log:
            result[time]['name'] = test_log['name']
        else:
            raise KeyError('Field \'name\' is required!')

        if 'errors' in test_log:
            result[time]['status'] = 'errors: ' + str(test_log['errors'])
        else:
            raise KeyError('Field \'errors\' is required!')

        return result

    def __validate_json(self, data, **params):
        validate(data, schema=self.schema, format_checker=FormatChecker())
