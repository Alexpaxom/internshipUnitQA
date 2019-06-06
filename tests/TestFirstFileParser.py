import unittest
import json
import jsonschema
from FirstFileParser import FFParser


class TestFirstFileParser(unittest.TestCase):

    def setUp(self):
        self.parser = FFParser()


    def test_correct_files(self):
        # TEST
        json_res = json.dumps(self.parser.parse('tests\materials\File_empty_json.json'), sort_keys=True)
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

        # TEST keys have int type
        res = self.parser.parse('tests\materials\File_1_2records.json')
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
            self.parser.parse('tests\materials\File_1_without_status_and_name.json')

    def test_fail(self):
        # TEST two tests have some "time" field and we cannot distinguish them
        with self.assertRaises(KeyError):
            self.parser.parse('tests\materials\File_1_fail_same_time.json')

    def test_json_schema(self):
        # TEST
        with open('schemas/FirstFileSchema.json') as schema:
            parser = FFParser(schema=json.load(schema))
            json_res = json.dumps(parser.parse('tests\materials\File_empty_json.json'), sort_keys=True)
            json_expect = json.dumps({}, sort_keys=True)
            self.assertEqual(json_res, json_expect)

        # TEST
        with open('schemas/FirstFileSchema.json') as schema:
            parser = FFParser(schema=json.load(schema))
            json_res = json.dumps(parser.parse('tests\materials\File_1.json'), sort_keys=True)
            json_expect = json.dumps({'946684810': {'name': 'Test output A', 'status': 'fail'}}, sort_keys=True)
            self.assertEqual(json_res, json_expect)

        # TEST
        with open('schemas/FirstFileSchema.json') as schema:
            parser = FFParser(schema=json.load(schema))
            with self.assertRaises(jsonschema.exceptions.ValidationError):
                json.dumps(parser.parse('tests\materials\File_1_error_for_schema.json'), sort_keys=True)

