from LogAnalyzer import LogAnalyzer
import os
import json


if __name__ == '__main__':
    log_analayzer = LogAnalyzer()
    with open('settings.json') as file:
        params = json.load(file)

    try:
        tests = log_analayzer.process(file_1=params['log_path']['file_1'],
                                      file_2=params['log_path']['file_2'],
                                      file_3=params['log_path']['file_3'])
    except Exception as e:
        print(str(e))
        exit(0)

    # print(json.dumps(tests, indent=4))
    with open(os.path.join(params['result']['path'], params['result']['name']), 'w') as file:
        json.dump(tests, file, indent=4)
