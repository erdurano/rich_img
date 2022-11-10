from typing import Sequence, Tuple
from typing import NamedTuple
from .block_chars import BLOCKCHARS
from collections import Counter
# from bitarray.util import int2ba, ba2int

Pixel = Tuple[int, int, int]


class RasterCell(NamedTuple):
    '''
    Represents equivalent cell to a 4 by 8 pixels region as foreground color,
    background color and character
    '''
    fg_color: Tuple[int, int, int]
    bg_color: Tuple[int, int, int]
    char: str


def get_color_avg(pixels: Sequence[Tuple[int, int, int]]) -> Tuple[int, int, int]:
    """Returns average color of a grup of pixels represented by rgb 3tuple"""
    if not pixels:
        return (0, 0, 0)
    size = len(pixels)
    red_total, green_total, blue_total = 0, 0, 0
    for red, green, blue in pixels:
        red_total += red
        green_total += green
        blue_total += blue

    return (red_total // size, green_total // size, blue_total // size)


def invert_bits(flag: int) -> int:

    for i in range(32):
        flag = flag ^ (1 << i)
    return flag


def get_split_flags(pixels: Sequence[Tuple[int, int, int]]) -> int:

    channels = tuple(zip(*pixels))
    split_r = max(channels[0]) - min(channels[0])
    split_g = max(channels[1]) - min(channels[1])
    split_b = max(channels[2]) - min(channels[2])
    split_channels = (split_r, split_b, split_g)
    max_split = max(split_channels)
    split_index = split_channels.index(max_split)
    split_value = min(channels[split_index]) + max_split/2

    split_flags = 0
    for pix in pixels:
        split_flags <<= 1
        if pix[split_index] > split_value:
            split_flags |= 1

    return split_flags


def diff_from_charflags(
        hi_flags: int,
        char_flags: int) -> int:
    '''
    Finds how many pixels' high values are different than given char_flag integer.
    with an XOR operation difference in bit flags obtained and count
    returned with int.bit_count()
    '''
    masked = hi_flags ^ char_flags
    return masked.bit_count()


def get_block_char(hi_flags: int) -> Tuple[int, int, bool]:
    """
    returns block char with closest charflag to the hi_flags of the cell and
    whether it is inverted or not
    """

    min_diff = 8
    inverted = False       # sensible default

    code = 0x2584  # lower 1/2
    flags = 0x0000ffff

    for char_flags, char_code in BLOCKCHARS.items():
        diff = diff_from_charflags(hi_flags, char_flags)
        inverse_diff = diff_from_charflags(hi_flags,
                                           invert_bits(char_flags))

        if diff < min_diff:
            code = char_code
            flags = char_flags
            inverted = False
            min_diff = diff

        if inverse_diff < min_diff:
            code = char_code
            flags = char_flags
            inverted = True
            min_diff = 32-diff

    return flags, code, inverted


def get_direct_flags(
        pixels: Sequence[Pixel],
        color_counts: list[Tuple[Pixel, int]]
) -> int:

    flags = 0
    denser_color = color_counts[0][0]
    sparser_color = color_counts[1][0] if len(
        color_counts) >= 2 else denser_color
    for pixel in pixels:
        flags <<= 1
        d1 = 0
        d2 = 0
        for index, channel in enumerate(pixel):
            d1 += (denser_color[index] - channel) ** 2
            d2 += (sparser_color[index] - channel) ** 2
        if d1 > d2:
            flags |= 1

    return flags


def get_cell_from_pattern(pixels: Sequence[Pixel],
                          codepoint: int = 0x2584,
                          pattern: int = 0x0000ffff) -> RasterCell:
    """
    Returns a raster cell from flattend pixel sequence with a
    code point with a specified pattern. Defaults to half block.
    """

    mask = 1 << 31

    fg_pixels = []
    bg_pixels = []
    for pixel in pixels:
        if mask & pattern:
            fg_pixels.append(pixel)
        else:
            bg_pixels.append(pixel)
        mask >>= 1
    fg_color = get_color_avg(fg_pixels)
    bg_color = get_color_avg(bg_pixels)

    return RasterCell(fg_color, bg_color, chr(codepoint))


def get_cell(pixels: Sequence[Tuple[int, int, int]]) -> RasterCell:

    most_2_color_counts = Counter(pixels).most_common(2)
    most2sum = sum(count[1] for count in most_2_color_counts)
    if most2sum > len(pixels) / 2:
        flags = get_direct_flags(pixels, most_2_color_counts)
        best_pattern, charcode, inverted = get_block_char(flags)
        fg_color = most_2_color_counts[-1][0]
        bg_color = most_2_color_counts[0][0] if len(
            most_2_color_counts) >= 2 else fg_color
        if inverted:
            fg_color, bg_color = bg_color, fg_color

    else:
        flags = get_split_flags(pixels)
        best_pattern, charcode, inverted = get_block_char(flags)
        mask = 1 << 31
        fg_cells = []
        bg_cells = []
        for pixel in pixels:
            if best_pattern & mask:
                fg_cells.append(pixel)
            else:
                bg_cells.append(pixel)
            mask >>= 1
        fg_color = get_color_avg(fg_cells)
        bg_color = get_color_avg(bg_cells)

    return RasterCell(fg_color, bg_color, chr(charcode))
