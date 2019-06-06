from LogAnalyzer import LogAnalyzer
import json
import sys
import argparse
import logging
import jsonschema



def create_cmd_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f1', '--file_1')
    parser.add_argument('-f2', '--file_2')
    parser.add_argument('-f3', '--file_3')

    parser.add_argument('-o', '--file_out')

    return parser


if __name__ == '__main__':
    cmd_parser = create_cmd_parser()
    log_analayzer = LogAnalyzer()

    with open('settings.json') as file:
        params = json.load(file)

    logging.basicConfig(filename=params['logs']['path'], level=logging.INFO)
    log = logging.getLogger('errors')

    try:
        args = cmd_parser.parse_args(sys.argv[1:])

        tests = log_analayzer.process(file_1=args.file_1,
                                      file_2=args.file_2,
                                      file_3=args.file_3,
                                      schema_1=params['schemas_path']['schema_1'],
                                      schema_2=params['schemas_path']['schema_2'],
                                      schema_3=params['schemas_path']['schema_3'],
                                      schema_res=params['schemas_path']['schema_res'])

        with open(args.file_out, 'w') as file:
            json.dump(tests, file, indent=4)

    except FileNotFoundError as ex:
        template = 'File non found. An exception of type {0} occurred. Arguments:\n{1!r}'
        message = template.format(type(ex).__name__, ex.args)
        log.exception(message)
        print(message)
    except json.decoder.JSONDecodeError as ex:
        template = 'Bad JSON. An exception of type {0} occurred. Arguments:\n{1!r}'
        message = template.format(type(ex).__name__, ex.args)
        log.exception(message)
        print(message)
    except jsonschema.exceptions.ValidationError as ex:
        template = 'File is not valid... An exception of type {0} occurred. Arguments:\n{1!r}'
        message = template.format(type(ex).__name__, ex.args)
        log.exception()
        print(message)
    except Exception as ex:
        template = 'An exception of type {0} occurred. Arguments:\n{1!r}'
        message = template.format(type(ex).__name__, ex.args)
        log.exception()
        print(message)
