# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import

from pingparsing import PingResult
import pytest

from .common import ping_parser
from .data import (
    PING_DEBIAN_SUCCESS,
)


class Test_PingResult(object):

    @pytest.mark.parametrize(["pingresult", "expected"], [
        [
            PingResult(PING_DEBIAN_SUCCESS, "", 0),
            {
                "destination": "google.com",
                "packet_transmit": 60,
                "packet_receive": 60,
                "packet_loss_count": 0,
                "packet_loss_rate": 0.0,
                "packet_duplicate_count": 0,
                "packet_duplicate_rate": 0,
                "rtt_min": 61.425,
                "rtt_avg": 99.731,
                "rtt_max": 212.597,
                "rtt_mdev": 27.566,
            }
        ]
    ])
    def test_normal_pingresult(self, ping_parser, pingresult, expected):
        ping_parser.parse(pingresult.stdout)
        assert ping_parser.as_dict() == expected

        ping_parser.parse(pingresult)
        assert ping_parser.as_dict() == expected
