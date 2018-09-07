import unittest
import io
import validate_addr_spec


class TestProblem3(unittest.TestCase):
    def test_execute(self):
        io_in = io.StringIO('aa@hoge\n"""@moge.com\n')
        io_out = io.StringIO()
        validate_addr_spec.execute(io_in, io_out)
        io_out.seek(0)
        self.assertEqual(io_out.read(), 'ok\nng\n')

    def test_is_address_valid(self):
        cases = [
            ('hoge.moge@fuga.com', True),
            ('moge@.com', False),
            ('hoge.@fuga.com', False),
            ('-..-@a.com', False),
            (r'"aaa"a@a', False),
            (r'"aa\!aaa\""@a', False),
            ('"' + r"!#$%&'*+-/=?" + '"@aa', True),
            (r'"^_`{|}~(),.:;<>@[]\"\\"@a', True),
            (r'""@a', True),
            (r'"@.."@a', True),
            (r'"@a', False),
        ]
        for (test, expected) in cases:
            self.assertEqual(validate_addr_spec.is_address_valid(test), expected, test)

    def test_split_adress(self):
        self.assertEqual(
            validate_addr_spec.split_address("!#$%&'*+-/=?^_`{|}~.aA1@!#$%&'*+-/=?^_`{|}~.aA1"),
            ("!#$%&'*+-/=?^_`{|}~.aA1", "!#$%&'*+-/=?^_`{|}~.aA1"))
        self.assertEqual(
            validate_addr_spec.split_address("!#$%&'*+-/=?^_`{|}~(),.:;<>@[]\"\\@!#$%&'*+-/=?^_`{|}~.aA1"),
            ("!#$%&'*+-/=?^_`{|}~(),.:;<>@[]\"\\", "!#$%&'*+-/=?^_`{|}~.aA1"))

    def test_has_at_mark(self):
        self.assertTrue(validate_addr_spec.has_at_mark('aaabb.c@eeee'))
        self.assertFalse(validate_addr_spec.has_at_mark('aabg()aa'))

    def test_is_local_quoted(self):
        cases = [
            (r'"aaa"', True),
            (r'"\""', True),
            (r'"', False),
            (r'"aaa', False),
            (r'aaa"', False),
            (r'aa"aa', False),
        ]
        for (test, expected) in cases:
            self.assertEqual(validate_addr_spec.is_local_quoted(test), expected, test)

    def test_d1_is_valid_non_quote_chars_no_parameterized(self):
            self.assertTrue(validate_addr_spec.d1_is_valid_non_quote_chars('hogehoge'))
            self.assertTrue(validate_addr_spec.d1_is_valid_non_quote_chars("!#$%&'*+-/=?^_`{|}~.azAZ019"))
            self.assertFalse(validate_addr_spec.d1_is_valid_non_quote_chars("\""))
            self.assertFalse(validate_addr_spec.d1_is_valid_non_quote_chars('aa"aaa'))
            self.assertFalse(validate_addr_spec.d1_is_valid_non_quote_chars('aa\\aaa'))

    def test_d1_is_valid_non_quote_chars(self):
        cases = [
            ('hogehoge', True),
            ("!#$%&'*+-/=?^_`{|}~.azAZ019", True),
            ("\"", False),
            ('aa"aaa', False),
            ('aa\\aaa', False),
        ]
        for (test, expected) in cases:
            self.assertEqual(validate_addr_spec.d1_is_valid_non_quote_chars(test), expected, test)

    def test_d2_not_starts_with_dot(self):
        cases = [
            ('aa.aa.', True),
            ('.aa.ee', False),
            ('', True),
            ('.', False),
        ]
        for (test, expected) in cases:
            self.assertEqual(validate_addr_spec.d2_not_starts_with_dot(test), expected, test)

    def test_d3_not_ends_with_dot(self):
        cases = [
            ('.aa.aa', True),
            ('', True),
            ('aa.ee.', False),
            ('.', False),
        ]
        for (test, expected) in cases:
            self.assertEqual(validate_addr_spec.d3_not_ends_with_dot(test), expected, test)

    def test_d4_not_appear_double_dot(self):
        self.assertTrue(validate_addr_spec.d4_not_appear_double_dot('a.b.c.d'))
        self.assertFalse(validate_addr_spec.d4_not_appear_double_dot('a..bcde'))

    def test_d5_is_valid_non_quote_len(self):
        cases = [
            ('', False),
            ('a', True),
            ('aaaa', True),
        ]
        for (test, expected) in cases:
            self.assertEqual(validate_addr_spec.d5_is_valid_non_quote_len(test), expected, test)

    def test_is_domain_valid(self):
        cases = [
            ('hogehoge', True),
            ("!#$%&'*+-/=?^_`{|}~.azAZ019", True),
            ("\"", False),
            ('aa.aa.', False),
            ('.aa.ee', False),
            ('', False),
        ]
        for (test, expected) in cases:
            self.assertEqual(validate_addr_spec.is_domain_valid(test), expected, test)

    def test_lq1_starts_with_quote(self):
        cases = [
            ('"aaa"', True),
            ('"', True),
            ('aaa"', False),
        ]
        for (test, expected) in cases:
            self.assertEqual(validate_addr_spec.lq1_starts_with_quote(test), expected, test)

    def test_lq2_ends_with_quote(self):
        cases = [
            ('"aaa"', True),
            ('"', True),
            ('"aaa', False),
        ]
        for (test, expected) in cases:
            self.assertEqual(validate_addr_spec.lq2_ends_with_quote(test), expected, test)

    def test_lq3_is_valid_quote_chars(self):
        cases = [
            (r'aAz0Z99', True),
            (r"!#$%&'*+-/=?", True),
            (r'^_`{|}~(),.:;<>@[]"\\', True),
            ('あ', False),
        ]
        for (test, expected) in cases:
            self.assertEqual(validate_addr_spec.lq3_is_valid_quote_chars(test), expected, test)

    def test_lq4_escape(self):
        cases = [
            (r'aAz0Z99', True),
            (r'aa\"', True),
            (r'\"\\a\"bbx', True),
            (r'"aaaa', False),
            (r'\"iii"aa', False),
            (r'xxx"xx\"a', False),
            (r'\\"', False),
            (r'\aa', False)
        ]
        for (test, expected) in cases:
            self.assertEqual(validate_addr_spec.lq4_escape(test), expected, test)

    def test_lq5_is_valid_quoted_len(self):
        cases = [
            ('', False),
            ('"', False),
            ('""', True),
            ('"a"', True),
        ]
        for (test, expected) in cases:
            self.assertEqual(validate_addr_spec.lq5_is_valid_quoted_len(test), expected, test)

    def test_is_local_quoted_valid(self):
        cases = [
            (r'aa', False),
            (r'"aaa"a', False),
            (r'"aa\!aaa\""', False),
            ('"' + r"!#$%&'*+-/=?" + '"', True),
            (r'"^_`{|}~(),.:;<>@[]\"\\"', True),
            (r'""', True),
            (r'"', False),
        ]
        for (test, expected) in cases:
            self.assertEqual(validate_addr_spec.is_local_quoted_valid(test), expected, test)
