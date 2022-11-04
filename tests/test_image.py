from random import random
import pytest

from rich_img_widget.image import (diff_from_charflags, get_color_avg,
                                   get_hi_flags, get_block_char)


def test_avg():
    reds = [int(random() * 256) for _ in range(32)]
    greens = [int(random() * 256) for _ in range(32)]
    blues = [int(random() * 256) for _ in range(32)]

    expected = (int(sum(reds) / 32), int(sum(greens) / 32),
                int(sum(blues) / 32))

    cells = [(reds[i], greens[i], blues[i]) for i in range(32)]

    assert get_color_avg(cells) == expected


class TestHiLoMap:

    def test_sanity(self):

        test_cells = [(255, 255, 255) if i % 4 == 0 else (0, 0, 0)
                      for i in range(32)]

        expected_flag = 0b10001000100010001000100010001000

        assert get_hi_flags(test_cells) == expected_flag


@pytest.mark.parametrize("high_flags, charflags, expected_diff", [
    (0b00110100001001101001100100010110, 0b10010100001001101011100000010110, 4),
    (0b11011111110000011011101001001100, 0b11001111110100010011101000000101, 6),
    (0b10100011001001011111110110100110, 0b10100011001001011111110110100111, 1),
    (0b10010111100100001100001111011110, 0b10010111100100001100001111011110, 0),
    (0b00011100101110100001001111011001, 0b00011110001100100001001111011001, 3),
    (0b00000000000000000000000000000000, 0b11111111111111111111111111111111, 32)
]
)
def test_diff_from_mask(high_flags, charflags, expected_diff):

    assert diff_from_charflags(high_flags, charflags) == expected_diff


@pytest.mark.parametrize("hi_flags, expected_charcode, expected_inverted", [
    (0b11111111111111111111111111111111, 0x00a0, True),
    (0b00000000000000000000000000000000, 0x00a0, False),
    (0b00000000000000001100110011001100, 0x2596, False),
    (0b11111111111111110011001100110011, 0x2596, True)
]
)
def test_get_char(hi_flags, expected_charcode, expected_inverted):
    assert (expected_charcode, expected_inverted) == get_block_char(hi_flags)
