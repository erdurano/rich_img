from random import random
import pytest

from rich_img_widget.image import (diff_from_charflag, get_cell_avg,
                                   get_hi_flags)


def test_avg():
    reds = [int(random() * 256) for _ in range(32)]
    greens = [int(random() * 256) for _ in range(32)]
    blues = [int(random() * 256) for _ in range(32)]

    expected = (int(sum(reds) / 32), int(sum(greens) / 32),
                int(sum(blues) / 32))

    cells = [(reds[i], greens[i], blues[i]) for i in range(32)]

    assert get_cell_avg(cells) == expected


class TestHiLoMap:

    def test_sanity(self):

        test_cells = [(255, 255, 255) if i % 4 == 0 else (0, 0, 0)
                      for i in range(32)]

        expected_flag = 0b10001000100010001000100010001000

        assert get_hi_flags(test_cells) == expected_flag


@pytest.mark.parametrize("high_flags, masks, expected_diff", [
    (0b00110100001001101001100100010110, 0b10010100001001101011100000010110, 4),
    (0b11011111110000011011101001001100, 0b11001111110100010011101000000101, 6),
    (0b10100011001001011111110110100110, 0b10100011001001011111110110100110, 0),
    (0b10010111100100001100001111011110, 0b10010111100100001100001111011110, 0),
    (0b11001111100111101100001110111100, 0b11001111100111101100001110111100, 0),
    (0b00011100101110100001001111011001, 0b00011100101110100001001111011001, 0),
    (0b00101111101101010111100000110010, 0b00101111101101010111100000110010, 0),
    (0b11010110010101111010000000101100, 0b11010110010101111010000000101100, 0),
    (0b10100010101101001100011111001100, 0b10100010101101001100011111001100, 0),
    (0b01111011000011101001000110110001, 0b01111011000011101001000110110001, 0),
]
)
def test_diff_from_mask(high_flags, masks, expected_diff):

    assert diff_from_charflag(high_flags, masks) == expected_diff
