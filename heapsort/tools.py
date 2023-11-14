# 2153689

import math
import unicodedata


def insert_newlines(input_string, max_length):
    output_string = ""

    char_count = 0
    for char in input_string:
        char_count += 1

        if unicodedata.east_asian_width(char) in ['W', 'F']:
            char_count += 1

        output_string += char

        if char_count >= max_length:
            output_string += '\n'
            char_count = 0

    return output_string


def is_numeric(str: str):
    try:
        int(str)
        return True
    except:
        return False


def coordinate_calculate(arr, num, left, right, up, down):
    array = []
    height = math.ceil(math.log2(num + 1))
    dh, dw = (down - up) / (1 + height), (right - left) / 2
    h, w, n, i = dh + up, left, 1, 0
    for index, value in enumerate(arr):
        i, w = i + 1, w + dw
        array.append((value, index, w, h))
        if i == n:
            n = n * 2
            h, w, dw, i = h + dh, left, (right - left) / (n + 1), 0
    return array
