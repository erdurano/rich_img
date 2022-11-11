import itertools
from random import random
from typing import Iterator, List, Mapping, Tuple

import pytest
from PIL import Image

from rich_img.image import (diff_from_charflags, get_block_char, get_cell,
                            get_cell_from_pattern, get_color_avg, invert_bits)

Pixel = Tuple[int, int, int]
Coordinate = Tuple[int, int]
PixelAccessor = Mapping[Coordinate, Pixel]


def int_from_charmap(charflags: int) -> Iterator[int]:
    mask = 1 << 31
    while mask:
        if charflags & mask:
            yield 1
        else:
            yield 0
        mask >>= 1


def black_triangle() -> Tuple[Tuple[int, int, int], ...]:
    return tuple(
        (0, 0, 0) if flag == 1 else (255, 255, 255)
        for flag in int_from_charmap(0x000137f0)
    )


def tiv_first_line() -> Iterator[str]:
    yield from ("  ▌▌▅▅▊▊▄▃▄▄▄▃▃▃▄▄  ▄▄▅▅▄▌▁▃▂▌▝▄▘▄▄▄▃▃▇▆▆▆▅▖▅▄▅▅▃▂▗▄ ▃▂▗▁▂▂▊▅▁▄"
                "▝▄▝▝▗▃▂▘▂▝▃▄▄▄▅▆▖▅▘▄▅━▃▄▄▃▘▘▄▂▆▂▃▃▅▄▂┗▆▆▃▖▅▄▃ ▆▝▃ ▅▅▄▃▄▂▄▅▅▂▃▅▅"
                "▖▅▂▌▃▅▂▗▄▄▁▂▂▂▅▅▅▄▃▂▘▝▄▅▅▆▅┛▂▅▅▅▄▄▅▅▝▌▆▃▌▌▖▅▄▄▂▄▌▌▌")


def island_firstline_pixels() -> Iterator[List[Pixel]]:
    with Image.open("./tests/img/island.jpg") as file:
        img_size = file.size
        pix: PixelAccessor = file.load()  # type: ignore

    y = 0
    for x in range(0, img_size[0]-4, 4):
        pixels = [pix[(x, y)]
                  for y, x in itertools.product(range(y, y+8), range(x, x+4))]
        yield pixels


@pytest.mark.parametrize("bits, expected", [
    (0x88888888, 0x77777777),
    (0xffffffff, 0),
    (0, 0xffffffff)
])
def test_invert_bits(bits, expected):
    assert invert_bits(bits) == expected


def test_avg():
    reds = [int(random() * 256) for _ in range(32)]
    greens = [int(random() * 256) for _ in range(32)]
    blues = [int(random() * 256) for _ in range(32)]

    expected = (int(sum(reds) / 32), int(sum(greens) / 32),
                int(sum(blues) / 32))

    cells = [(reds[i], greens[i], blues[i]) for i in range(32)]

    assert get_color_avg(cells) == expected


def test_get_cell_from_pattern():
    pattern = 0x000137f0
    charcode = 0x25e2
    pixels = black_triangle()
    cell = get_cell_from_pattern(pixels, codepoint=charcode, pattern=pattern)

    assert cell.fg_color == (0, 0, 0)
    assert cell.bg_color == (255, 255, 255)
    assert cell.char == '◢'


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


@ pytest.mark.parametrize(
    "hi_flags, expected_flags, expected_charcode, expected_inverted",
    [
        (0b00000000000000000000000000000000, 0x00000000, 0x00a0, False),
        (0b11111111111111111111111111111111, 0x00000000, 0x00a0, True),
        (0b11111111111111110011001100110011, 0x0000cccc, 0x2596, True),
        (0b00000000000000001100110011001100, 0x0000cccc, 0x2596, False),
    ]
)
def test_get_char(hi_flags, expected_flags, expected_charcode, expected_inverted):
    assert (expected_flags, expected_charcode,
            expected_inverted) == get_block_char(hi_flags)


class TestGetCell:
    black = (0, 0, 0)
    white = (255, 255, 255)

    def test_sanity(self):
        pixels = black_triangle()
        cell = get_cell(pixels)
        assert cell.fg_color == self.black
        assert cell.bg_color == self.white
        assert cell.char == '◢'

    @pytest.mark.parametrize("tiv_char, cell_range_pixels",
                             zip(tiv_first_line(), island_firstline_pixels())
                             )
    def test_against_tiv(self, tiv_char: str, cell_range_pixels: List[Pixel]):

        assert tiv_char == get_cell(cell_range_pixels).char
