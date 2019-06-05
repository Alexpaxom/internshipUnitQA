from FirstFileParser import FFParser
from SecondFileParser import SFParser
from ThirdFileParser import TFParser
from warnings import warn


class LogAnalyzer:
    """Processes information from few log files"""

    def process(self, **params):
        if 'file_1' not in params and params['file_1'] != '':
            raise FileNotFoundError('file_1 required parameter')

        if 'file_2' not in params and params['file_2'] != '':
            raise FileNotFoundError('file_2 required parameter')

        if 'file_3' not in params and params['file_3'] != '':
            raise FileNotFoundError('file_3 required parameter')

        return self.__process(file_1=params['file_1'], file_2=params['file_2'], file_3=params['file_3'])


    def __process(self, **params):
        ffparser = FFParser()
        sfparser = SFParser()
        tfparser = TFParser()

        log_1_tests = ffparser.parse(params['file_1'])
        log_2_tests = sfparser.parse(params['file_2'])

        test_results = tfparser.parse(params['file_3'])

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


        return result
