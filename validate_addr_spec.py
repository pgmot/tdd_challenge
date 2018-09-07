import re
import sys


def execute(io_in, io_out):
    input_lines = io_in.readlines()
    output_lines = [
        format_output(is_address_valid(line.strip()))
        for line
        in input_lines
    ]
    io_out.writelines(output_lines)


def format_output(bool_val):
    return 'ok\n' if bool_val else 'ng\n'


def is_address_valid(addr):
    if not has_at_mark(addr):
        return False
    (local_part, domain_part) = split_address(addr)
    if not is_domain_valid(domain_part):
        return False
    if is_local_quoted(local_part):
        return is_local_quoted_valid(local_part)
    else:
        return is_domain_valid(local_part)


def has_at_mark(addr):
    return '@' in addr


def split_address(addr):
    return tuple(addr.rsplit('@', 1))


def is_local_quoted(text):
    return all([
        lq1_starts_with_quote(text),
        lq2_ends_with_quote(text),
        lq5_is_valid_quoted_len(text),
    ])


# domain part --------------
def d1_is_valid_non_quote_chars(text):
    return bool(re.fullmatch(r"[0-9a-zA-Z!#$%&'*+/=?^_`{|}~.-]*", text))


def d2_not_starts_with_dot(text):
    return len(text) == 0 or text[0] != '.'


def d3_not_ends_with_dot(text):
    return len(text) == 0 or text[-1] != '.'


def d4_not_appear_double_dot(text):
    return '..' not in text


def d5_is_valid_non_quote_len(text):
    return len(text) >= 1


def is_domain_valid(text):
    return all([
        d1_is_valid_non_quote_chars(text),
        d2_not_starts_with_dot(text),
        d3_not_ends_with_dot(text),
        d4_not_appear_double_dot(text),
        d5_is_valid_non_quote_len(text),
    ])


# local quoted -------------------------------


def lq1_starts_with_quote(text):
    return len(text) >= 1 and text[0] == '"'


def lq2_ends_with_quote(text):
    return len(text) >= 1 and text[-1] == '"'


def lq3_is_valid_quote_chars(text_without_quote):
    return bool(re.fullmatch(r"[0-9a-zA-Z!#$%&'" + r'"' + r"*+-/=?^_`{|}~(),.:;<>@[\]\\]*", text_without_quote))


def lq4_escape(text_without_quote):
    if not _lq4_sub_quote(text_without_quote):
        return False
    non_quote = text_without_quote.replace(r'\"', '')
    esc_list = re.findall(r'\\+', non_quote)
    for esc in esc_list:
        if len(esc) != 2:
            return False
    return True


def _lq4_sub_quote(text_without_quote):
    last_1 = ''
    last_2 = ''
    for i in range(len(text_without_quote)):
        c = text_without_quote[i]
        if c == '"':
            if last_1 != '\\':
                return False  # " の前は \ で無ければならない
            if last_2 == '\\':
                return False  # " の前に２つ連続 \ が続いてはならない
        last_2 = last_1
        last_1 = c
    return True


def lq5_is_valid_quoted_len(text):
    return len(text) >= 2


def is_local_quoted_valid(text):
    text_without_quote = text[1:-1]
    return all([
        lq1_starts_with_quote(text),
        lq2_ends_with_quote(text),
        lq3_is_valid_quote_chars(text_without_quote),
        lq4_escape(text_without_quote),
        lq5_is_valid_quoted_len(text),
    ])


if __name__ == '__main__':
    execute(sys.stdin, sys.stdout)
