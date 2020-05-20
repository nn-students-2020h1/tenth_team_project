import unittest
import re

class TestAuxiliaryTools(unittest.TestCase):
    def test_001_space_regex(self):
        string = " 123 "
        result = re.findall(r"^\s*(.+?)\s*$", string)[0]
        self.assertEqual(result, "123")

    def test_001_space_regex_phrase(self):
        string = "   hello world  "
        result = re.findall(r"^\s*(.+?)\s*$", string)[0]
        self.assertEqual(result, "hello world")

    def test_001_space_regex_ok(self):
        string = "hello world"
        result = re.findall(r"^\s*(.+?)\s*$", string)[0]
        self.assertEqual(result, "hello world")