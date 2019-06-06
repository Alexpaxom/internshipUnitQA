from LogAnalyzer import LogAnalyzer
import json
import sys
import argparse


def create_cmd_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f1', '--file_1')
    parser.add_argument('-f2', '--file_2')
    parser.add_argument('-f3', '--file_3')

    parser.add_argument('-o', '--file_out')

    return parser


if __name__ == '__main__':
    cmd_parser = create_cmd_parser()
    args = cmd_parser.parse_args(sys.argv[1:])

    log_analayzer = LogAnalyzer()
    with open('settings.json') as file:
        params = json.load(file)

    tests = log_analayzer.process(file_1=args.file_1,
                                  file_2=args.file_2,
                                  file_3=args.file_3,
                                  schema_1=params['schemas_path']['schema_1'],
                                  schema_2=params['schemas_path']['schema_2'],
                                  schema_3=params['schemas_path']['schema_3'],
                                  schema_res=params['schemas_path']['schema_res'])

    with open(args.file_out, 'w') as file:
        json.dump(tests, file, indent=4)
