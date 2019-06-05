import unittest
import json
from SecondFileParser import SFParser


class TestSecondFileParser(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
        self.parser = SFParser()


    def test_correct_files(self):
        # TEST
        json_res = json.dumps(self.parser.parse('tests\materials\File_empty_json.json'), sort_keys=True)
        json_expect = json.dumps({}, sort_keys=True)
        self.assertEqual(json_res, json_expect)

        # TEST
        json_res = json.dumps(self.parser.parse('tests\materials\File_2_without_cases.json'), sort_keys=True)
        json_expect = json.dumps({}, sort_keys=True)
        self.assertEqual(json_res, json_expect)

        # TEST
        json_res = json.dumps(self.parser.parse('tests\materials\File_2.json'), sort_keys=True)
        json_expect = json.dumps({'946684820': {'name': 'Test output B', 'status': 'errors: 0'}}, sort_keys=True)
        self.assertEqual(json_res, json_expect)

        # TEST
        json_res = json.dumps(self.parser.parse('tests\materials\File_2_few_records.json'), sort_keys=True)
        res_expect = {
            '946684820': {'name': 'Test output B', 'status': 'errors: 0'},
            '946684821': {'name': 'Test output E', 'status': 'errors: 0'},
            '946771220': {'name': 'Test output D', 'status': 'errors: 1'}
        }
        json_expect = json.dumps(res_expect, sort_keys=True)
        self.assertEqual(json_res, json_expect)

        # TEST keys have int type
        res = self.parser.parse('tests\materials\File_2_few_records.json')
        for key in res:
            self.assertTrue(isinstance(key, int))


    def test_exceptions(self):
        # TEST
        with self.assertRaises(FileNotFoundError):
            self.parser.parse('not_existing _file')

        # TEST
        with self.assertRaises(json.decoder.JSONDecodeError):
            self.parser.parse('tests\materials\File_empty.json')

        # TEST
        with self.assertRaises(KeyError):
            self.parser.parse('tests\materials\File_2_without_status_and_name.json')

    def test_fail(self):
        # TEST two tests have some "time" field and we cannot distinguish them
        with self.assertRaises(KeyError):
            self.parser.parse('tests\materials\File_2_fail_same_time.json')

