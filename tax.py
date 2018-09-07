import math
import sys


class Tax:
    def execute(self, io_in, io_out):
        str_data = io_in.read()
        data = self._str2data(str_data)
        price_list = list(map(self.calc_price, data))
        str_price_lis = ['{}\n'.format(price) for price in price_list]
        io_out.write(''.join(str_price_lis))

    def calc_price(self, price_list):
        price_sum = sum(price_list)
        return math.floor(price_sum * 1.1 + 0.5)

    def _str2data(self, str_data):
        lines = str_data.split('\n')[:-1]  # 行末に改行があるため
        return list(map(self._line2data, lines))

    def _line2data(self, line):
        if not line:
            return []
        return list(map(int, line.split(',')))


if __name__ == '__main__':
    Tax().execute(sys.stdin, sys.stdout)
