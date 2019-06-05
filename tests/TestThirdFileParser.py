import unittest
import json
from ThirdFileParser import TFParser


class TestThirdFileParser(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
        self.parser = TFParser()


    def test_correct_files(self):
        # TEST
        json_res = json.dumps(self.parser.parse('tests\materials\File_empty_json.json'), sort_keys=True)
        json_expect = json.dumps({}, sort_keys=True)
        self.assertEqual(json_res, json_expect)

        # TEST
        json_res = json.dumps(self.parser.parse('tests\materials\File_3.json'), sort_keys=True)
        res_expect = {
            '946684810': {'expected': 'A', 'actual': 'B'},
            '946684820': {'expected': 'B', 'actual': 'B'}
        }
        json_expect = json.dumps(res_expect, sort_keys=True)
        self.assertEqual(json_res, json_expect)

        # TEST
        json_res = json.dumps(self.parser.parse('tests\materials\File_3_few_records.json'), sort_keys=True)
        res_expect = {
            '946684810': {'expected': 'A', 'actual': 'B'},
            '946684820': {'expected': 'B', 'actual': 'B'},
            '952905600': {'expected': 'C', 'actual': 'C'},
            '946684821': {'expected': 'E', 'actual': 'E'},
            '946771220': {'expected': 'D', 'actual': 'B'},
        }
        json_expect = json.dumps(res_expect, sort_keys=True)
        self.assertEqual(json_res, json_expect)

        # TEST keys have int type
        res = self.parser.parse('tests\materials\File_3_few_records.json')
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
            self.parser.parse('tests\materials\File_3_without_expected_and_actual.json')

    def test_fail(self):
        # TEST two tests have some "time" field and we cannot distinguish them
        with self.assertRaises(KeyError):
            self.parser.parse('tests\materials\File_3_fail_same_time.json')

