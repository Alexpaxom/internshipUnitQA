import json


class FFParser:
    """Parser for first log file"""

    def parse(self, file_path, **params):
        result = {}
        with open(file_path) as file:
            file_data = json.load(file)
            result = self.parse_json(file_data)

        return result


    def parse_json(self, file_data, **params):
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
