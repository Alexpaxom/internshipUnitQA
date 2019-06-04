import json
from datetime import datetime


class TFParser:
    """Parser for first third file"""

    def parse(self, file_path, **params):
        result = {}
        with open(file_path) as file:
            file_data = json.load(file)
            result = self.parse_json(file_data)

        return result


    def parse_json(self, file_data, **params):
        result = {}

        if 'captures' not in file_data:
            return result

        for test_log in file_data['captures']:
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
        time = datetime.strptime(test_log['time'], '%Y-%m-%dT%H:%M:%S%z')
        time = int(time.timestamp())

        result[time] = {}

        if 'expected' in test_log:
            result[time]['expected'] = test_log['expected']
        else:
            raise KeyError('Field \'expected\' is required!')

        if 'actual' in test_log:
            result[time]['actual'] = test_log['actual']
        else:
            raise KeyError('Field \'actual\' is required!')

        return result
