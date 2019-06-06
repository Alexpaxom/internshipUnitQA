import json

from FirstFileParser import FFParser
from SecondFileParser import SFParser
from ThirdFileParser import TFParser
from jsonschema import validate
from jsonschema import FormatChecker
from warnings import warn
import os


class LogAnalyzer:
    """Processes information from few log files"""

    def process(self, **params):
        if params.get('file_1') is None:
            raise FileNotFoundError('file_1 required parameter')

        if params.get('file_2') is None:
            raise FileNotFoundError('file_2 required parameter')

        if params.get('file_3') is None:
            raise FileNotFoundError('file_3 required parameter')

        if 'schema_1' in params:
            with open(params['schema_1']) as file_schema:
                self.ffparser = FFParser(schema=json.load(file_schema))
        else:
            self.ffparser = FFParser()

        if 'schema_2' in params:
            with open(params['schema_2']) as file_schema:
                self.sfparser = SFParser(schema=json.load(file_schema))
        else:
            self.sfparser = SFParser()

        if 'schema_3' in params:
            with open(params['schema_3']) as file_schema:
                self.tfparser = TFParser(schema=json.load(file_schema))
        else:
            self.tfparser = TFParser()

        return self.__process(**params)

    def __process(self, **params):
        log_1_tests = self.ffparser.parse(params['file_1'])
        log_2_tests = self.sfparser.parse(params['file_2'])

        test_results = self.tfparser.parse(params['file_3'])

        tests = {}

        if len(log_1_tests.keys() & log_2_tests.keys()) == 0:
            tests = {**log_1_tests, **log_2_tests}
        else:
            raise KeyError('Two tests have the same "time". We cannot distinguish them.')

        result = []

        for test_key in sorted(test_results.keys()):
            if test_key in tests:
                result.append({**tests[test_key], **test_results[test_key]})
            else:
                warn('There are results of the "test" but its description was not found in the log file (name and status)', RuntimeWarning)
                result.append({'name': None, 'status': None, **test_results[test_key]})

        if 'schema_res' in params:
            with open(params['schema_res']) as schema_file:
                self.__validate_json(result, json.load(schema_file))

        return result

    def __validate_json(self, data, schema, **params):
        validate(data, schema=schema, format_checker=FormatChecker())
