import io
import unittest
from tax import Tax


class TestCase(unittest.TestCase):
    def test_execute(self):
        io_in = io.StringIO('10,12\n40,16\n100,45\n\n50,50,55\n\n')
        io_out = io.StringIO()
        tax = Tax()
        tax.execute(io_in, io_out)
        io_out.seek(0)  # ポインタを0に戻す
        self.assertEqual(io_out.read(), '24\n62\n160\n0\n171\n0\n')

    def test_calc_price(self):
        tax = Tax()
        self.assertEqual(tax.calc_price([10, 12]), 24)
        self.assertEqual(tax.calc_price([40, 16]), 62)
        self.assertEqual(tax.calc_price([100, 45]), 160)
        self.assertEqual(tax.calc_price([100, 55]), 171)
        self.assertEqual(tax.calc_price([]), 0)

    def test_str2data(self):
        tax = Tax()
        str_data = '10,12\n40,16\n100,45\n\n50,50,55\n\n'
        self.assertEqual(tax._str2data(str_data), [
            [10, 12],
            [40, 16],
            [100, 45],
            [],
            [50, 50, 55],
            [],
        ])

    def test_line2data(self):
        tax = Tax()
        self.assertEqual(tax._line2data('10,12'), [10, 12])
        self.assertEqual(tax._line2data('10'), [10])
        self.assertEqual(tax._line2data(''), [])
