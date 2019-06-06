import unittest
import json
from LogAnalyzer import LogAnalyzer

import warnings


class TestLogAnalyzer(unittest.TestCase):

    def setUp(self):
        self.log_analayzer = LogAnalyzer()


    def test_correct_files(self):
        # TEST
        tests = self.log_analayzer.process(file_1='tests\materials\File_1.json',
                                           file_2='tests\materials\File_2.json',
                                           file_3='tests\materials\File_3.json')
        with open('tests\materials\Result_4_1.json') as file:
            res_expect = json.load(file)
        self.assertEqual(json.dumps(tests), json.dumps(res_expect))

        # TEST
        tests = self.log_analayzer.process(file_1='tests\materials\File_1_2records.json',
                                           file_2='tests\materials\File_2_few_records.json',
                                           file_3='tests\materials\File_3_few_records.json')
        with open('tests\materials\Result_4_2.json') as file:
            res_expect = json.load(file)
        self.assertEqual(json.dumps(tests), json.dumps(res_expect))

        # TEST
        tests = self.log_analayzer.process(file_1='tests\materials\File_empty_json.json',
                                           file_2='tests\materials\File_empty_json.json',
                                           file_3='tests\materials\File_empty_json.json')
        self.assertEqual(json.dumps(tests), json.dumps([]))

        # TEST
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            tests = self.log_analayzer.process(file_1='tests\materials\File_empty_json.json',
                                               file_2='tests\materials\File_2_few_records.json',
                                               file_3='tests\materials\File_3_few_records.json')

            self.assertTrue(issubclass(w[-1].category, RuntimeWarning))
            with open('tests\materials\Result_4_3_not_all_data.json') as file:
                res_expect = json.load(file)
            self.assertEqual(json.dumps(tests), json.dumps(res_expect))


    def test_exceptions(self):
        # TEST
        with self.assertRaises(FileNotFoundError):
            self.log_analayzer.process(file_1='not_existing',
                                       file_2='tests\materials\File_empty_json.json',
                                       file_3='tests\materials\File_empty_json.json')

        # TEST
        with self.assertRaises(json.decoder.JSONDecodeError):
            self.log_analayzer.process(file_1='tests\materials\File_empty.json',
                                       file_2='tests\materials\File_empty_json.json',
                                       file_3='tests\materials\File_empty_json.json')

        # TEST
        with self.assertRaises(KeyError):
            self.log_analayzer.process(file_1='tests\materials\File_1_without_status_and_name.json',
                                       file_2='tests\materials\File_empty_json.json',
                                       file_3='tests\materials\File_empty_json.json')

        # TEST
        with self.assertRaises(FileNotFoundError):
            self.log_analayzer.process(file_1='',
                                       file_2='tests\materials\File_empty_json.json',
                                       file_3='tests\materials\File_empty_json.json')


    def test_fail(self):
        # TEST two tests have some "time" field and we cannot distinguish them
        with self.assertRaises(KeyError):
            self.log_analayzer.process(file_1='tests\materials\File_1_fail_same_time.json',
                                       file_2='tests\materials\File_empty_json.json',
                                       file_3='tests\materials\File_empty_json.json')

        # TEST two tests have some "time" field and we cannot distinguish them
        with self.assertRaises(KeyError):
            self.log_analayzer.process(file_1='tests\materials\File_empty_json.json',
                                       file_2='tests\materials\File_2_fail_same_time.json',
                                       file_3='tests\materials\File_empty_json.json')
        # TEST two tests have some "time" field and we cannot distinguish them
        with self.assertRaises(KeyError):
            self.log_analayzer.process(file_1='tests\materials\File_1.json',
                                       file_2='tests\materials\File_2_fail_same_time.json',
                                       file_3='tests\materials\File_3_fail_same_time.json')

    def test_json_schema(self):
        # TEST
        tests = self.log_analayzer.process(file_1='tests\materials\File_1.json',
                                           file_2='tests\materials\File_2.json',
                                           file_3='tests\materials\File_3.json',
                                           schema_res='schemas\ResultFileSchema.json')
        with open('tests\materials\Result_4_1.json') as file:
            res_expect = json.load(file)
        self.assertEqual(json.dumps(tests), json.dumps(res_expect))


