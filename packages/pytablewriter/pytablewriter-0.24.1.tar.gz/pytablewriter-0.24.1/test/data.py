# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import
from __future__ import unicode_literals

import collections
import datetime
import itertools

from pytablewriter import EmptyTableDataError


_time = datetime.datetime(2017, 1, 1, 0, 0, 0)
_inf = float("inf")
_nan = float("nan")

header_list = ["a", "b", "c", "dd", "e"]
value_matrix = [
    ["1", 123.1, "a", "1",   1],
    [2, 2.2, "bb", "2.2", 2.2],
    [3, 3.3, "ccc", "3",   "cccc"],
]
value_matrix_with_none = [
    ["1", None, "a", "1",   None],
    [None, 2.2, None, "2.2", 2.2],
    [3, 3.3, "ccc", None,   "cccc"],
    [None, None, None, None,   None],
]

mix_header_list = [
    "i",
    "f",
    "c",
    "if",
    "ifc",
    "bool",
    "inf",
    "nan",
    "mix_num",
    "time",
]
mix_value_matrix = [
    [
        1, 1.1, "aa", 1, 1, True,
        _inf, _nan, 1.0, _time,
    ],
    [
        2, 2.2, "bbb", 2.2, 2.2, False,
        "inf", "nan", _inf, "2017-01-02 03:04:05+09:00",
    ],
    [
        3, 3.33, "cccc", -3, "ccc", "true",
        "infinity", "NAN", _nan, _time,
    ],
]

float_header_list = ["a", "b", "c"]
float_value_matrix = [
    [0.01, 0.00125, 0.0],
    [1.0, 99.9,  0.01],
    [1.2, 999999.123, 0.001],
]

value_matrix_iter = [
    [
        [1, 2, 3],
        [11, 12, 13],
    ],
    [
        [1, 2, 3],
        [11, 12, 13],
    ],
    [
        [101, 102, 103],
        [1001, 1002, 1003],
    ],
]

value_matrix_iter_1 = [
    [
        ["a b c d e f g h i jklmn", 2.1, 3],
        ["aaaaa", 12.1, 13],
    ],
    [
        ["bbb", 2, 3],
        ["cc", 12, 13],
    ],
    [
        ["a", 102, 103],
        ["", 1002, 1003],
    ],
]

Data = collections.namedtuple("Data", "table indent header value expected")
null_test_data_list = [
    Data(
        table="dummy",
        indent=0,
        header=header,
        value=value,
        expected=EmptyTableDataError)
    for header, value in itertools.product([None, [], ""], [None, [], ""])
]
