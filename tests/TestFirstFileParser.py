import unittest
import json
from FirstFileParser import FFParser


class TestFirstFileParser(unittest.TestCase):

    def setUp(self):
        self.parser = FFParser()


    def test_correct_files(self):
        # TEST
        json_res = json.dumps(self.parser.parse('tests\materials\File_1_empty_json.json'), sort_keys=True)
        json_expect = json.dumps({}, sort_keys=True)
        self.assertEqual(json_res, json_expect)

        # TEST
        json_res = json.dumps(self.parser.parse('tests\materials\File_1.json'), sort_keys=True)
        json_expect = json.dumps({'946684810': {'name': 'Test output A', 'status': 'fail'}}, sort_keys=True)
        self.assertEqual(json_res, json_expect)

        # TEST
        json_res = json.dumps(self.parser.parse('tests\materials\File_1_2records.json'), sort_keys=True)
        res_expect = {
            '946684810': {'name': 'Test output A', 'status': 'fail'},
            '952905600': {'name': 'Test output C', 'status': 'success'}
        }
        json_expect = json.dumps(res_expect, sort_keys=True)
        self.assertEqual(json_res, json_expect)


    def test_exceptions(self):
        # TEST
        with self.assertRaises(FileNotFoundError):
            self.parser.parse('not_existing _file')

        # TEST
        with self.assertRaises(json.decoder.JSONDecodeError):
            self.parser.parse('tests\materials\File_1_empty.json')

        # TEST
        with self.assertRaises(KeyError):
            self.parser.parse('tests\materials\File_1_without_status_and_name.json')

